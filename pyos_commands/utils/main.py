import os
import time
import shlex
from getpass import getpass
from prompt_toolkit import PromptSession
from pyos_commands.utils.cmds_mapper import COMMANDS
from pyos_commands.utils.completer import PyOSCompleter
from pyos_commands.installer import start_scanner, _update_state
from pyos_commands.utils.userdb import verify_user, make_db, DB_PATH, get_user
from pyos_commands.utils.utils import save_vfs, load_vfs, get_node, ensure_dir, _ensure_meta_root
from pyos_commands.utils.system_config import VFS, SYSTEM_NAME, AUTO_SAVE_PATH, msg, msg2 ,msg3, msg4, msg5, OS_NAME

stop = False

session = PromptSession(completer=PyOSCompleter())

# --- prompt formatting & completion ---------------------------------------
def format_prompt(username, system_name, cwd, home_dir, is_root=False):
    if is_root:
        symbol = "#"
        path_display = cwd if cwd != "/" else "/"
        return f"{username}@{system_name}:{path_display}{symbol} "
    # non-root
    if cwd == home_dir:
        path_display = "~"
    elif home_dir != "/" and cwd.startswith(home_dir + "/"):
        path_display = "~" + cwd[len(home_dir):]
    else:
        path_display = cwd
    symbol = "$"
    return f"{username}@{system_name}:{path_display}{symbol} "

# --- command parsing & runner + utility functions--------------------------
def parse_command_simple(seg):
    try:
        return shlex.split(seg)
    except Exception:
        return seg.split()

def run_command(line, state):
    line = line.strip()
    if not line:
        return None
    # history replay !n
    if line.startswith("!"):
        try:
            idx = int(line[1:]) - 1
            hist = state.get("history", [])
            if 0 <= idx < len(hist):
                print(f"Replaying: {hist[idx]}")
                return run_command(hist[idx], state)
            else:
                print(f"{line}: event not found")
                return None
        except ValueError:
            print(f"{line}: invalid history reference")
            return None

    # Split pipeline respecting simple quoting
    pipeline = []
    buf = ""
    quote = None
    for ch in line:
        if ch in ("'", '"'):
            if quote is None:
                quote = ch
            elif quote == ch:
                quote = None
            buf += ch
        elif ch == "|" and quote is None:
            pipeline.append(buf.strip()); buf = ""
        else:
            buf += ch
    if buf.strip(): pipeline.append(buf.strip())

    input_text = None
    for i, seg in enumerate(pipeline):
        last = (i == len(pipeline) - 1)
        parts = parse_command_simple(seg)
        if not parts:
            continue
        cmd = parts[0]
        args = parts[1:]

        # built-in exit
        if cmd == "exit":
            return "EXIT"

        # special cd
        if cmd == "cd":
            COMMANDS["cd"](VFS, state, args)
            input_text = ""
            continue

        # history special
        if cmd == "history":
            res = COMMANDS["history"](VFS, state, args, capture=not last)
            input_text = res
            continue

        # sudo wrapper
        if cmd == "sudo":
            res = COMMANDS["sudo"](VFS, state, args, capture=not last)
            if isinstance(res, dict) and res.get("run_as_root"):
                wrapped = res.get("cmd_parts", [])
                if not wrapped:
                    if last: print("sudo: missing command")
                    input_text = ""
                    continue
                # run wrapped command as root
                saved_user = state["user"]
                state["user"] = "root"
                state["_sudo_active"] = True
                wrapped_line = " ".join(wrapped)
                inner_res = run_command(wrapped_line, state)
                state["user"] = saved_user
                state["_sudo_active"] = False
                input_text = inner_res
                continue
            else:
                input_text = res
                continue

        if cmd not in COMMANDS:
            msg = f"Command not found: {cmd}\n"
            if last:
                print(msg, end="")
            input_text = msg if not last else None
            continue

        capture = not last
        if cmd == "echo":
            res = COMMANDS["echo"](VFS, state, args, capture=capture)
        elif cmd == "cat":
            res = COMMANDS["cat"](VFS, state, args, input_text=input_text, capture=capture)
        else:
            try:
                res = COMMANDS[cmd](VFS, state, args, capture=capture)
            except TypeError:
                # command may not support capture param
                res = COMMANDS[cmd](VFS, state, args)
        input_text = res

        if state.get("_logout"):
            return "_LOGOUT_"
        
        if state.get("_update_msg"):
            print(f"\n[UPDATE] {state.pop('_update_msg')}\n")

    return input_text

def slow_print(text, delay=0.05):
    """Print text slowly like a typewriter effect"""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def banner():
    print(msg4)

# --- shell & login --------------------------------------------------------
def pyos_shell(user):
    is_root = (user == "root")
    home_dir = "/" if is_root else f"/home/{user}"
    if not is_root:
        if get_node(VFS, "/home") is None:
            ensure_dir(VFS, "/home")
        if get_node(VFS, home_dir) is None:
            ensure_dir(VFS, home_dir)
    _ensure_meta_root(VFS)
    state = {"user": user, "cwd": "/" if is_root else home_dir, "history": [], "_logout": False, "_sudo_active": False}
    global current_state
    current_state = state

    while True:
        prompt = format_prompt(user, SYSTEM_NAME, state["cwd"], home_dir, is_root=is_root)
        try:
            line = session.prompt(prompt)
        except (KeyboardInterrupt, EOFError):
            print()
            break
        if not line.strip():
            continue
        state["history"].append(line)
        res = run_command(line, state)
        if res == "EXIT":
            try:
                global stop
                save_vfs(VFS, AUTO_SAVE_PATH)
                stop = True
            except Exception:
                pass
            break
        if res == "_LOGOUT_":
            state["_logout"] = False
            print()
            break

def login_loop():
    # print(f"{SYSTEM_NAME} PyOS (VFS mode)\n")
    attempts = 0

    slow_print("Please log in to continue...\n", delay=0.08)

    while True:
        username = input(f"{OS_NAME} Username: ").strip()
        password = getpass(f"{OS_NAME} Password: ")

        u = get_user(username)
        if not u:
            print("No such user")
            continue

        if verify_user(username, password):
            slow_print(msg5)
            slow_print(f"Welcome back, {username}!\n")

            pyos_shell(username)
            if stop == True:
                break
            else:
                continue


        else:
            attempts += 1
            print("Login incorrect\n")
            if attempts >= 5:
                slow_print("Too many failed attempts.")
                break

def main():
    print("pyos version 0.01")
    banner()

    if not os.path.exists(DB_PATH):
        make_db()

    if os.path.exists(AUTO_SAVE_PATH):
        try:
            new = load_vfs(AUTO_SAVE_PATH)
            VFS.clear(); VFS.update(new)
            # print(f"Loaded VFS from {AUTO_SAVE_PATH}\n")
        except Exception:
            pass

    # Start background update scanner
    def _notify(msg):
        print(f"\n[UPDATE] {msg}\n")
    start_scanner(_notify)

    login_loop()
