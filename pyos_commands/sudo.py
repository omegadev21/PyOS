import time
from getpass import getpass
from pyos_commands.utils.global_cmds import cmds
from pyos_commands.utils.userdb import verify_user, get_user

def sudo(vfs, state, args=None, capture=False):
    args = args or []
    if not args:
        msg = "sudo: missing command\n"
        return msg if capture else print(msg, end="")

    user = state.get("user")
    u = get_user(user)
    if not u or not u["sudo"]:
        msg = f"sudo: {user} is not in the sudoers file\n"
        return msg if capture else print(msg, end="")

    # check cached auth
    now = time.time()
    if state.get("_sudo_auth_time") and now - state["_sudo_auth_time"] < 300:
        pass  # still valid
    else:
        pwd = getpass(f"[sudo] password for {user}: ")
        if not verify_user(user, pwd):
            msg = "Sorry, try again.\n"
            return msg if capture else print(msg, end="")
        state["_sudo_auth_time"] = now

    # Run command as root
    cmd = args[0]
    cmd_args = args[1:]
    func = cmds.get(cmd)
    if not func:
        msg = f"sudo: {cmd}: command not found\n"
        return msg if capture else print(msg, end="")

    return func(vfs, {**state, "user": "root", "is_root": True}, cmd_args, capture=capture)