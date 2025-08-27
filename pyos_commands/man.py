import os

MAN_DIR = os.path.join(os.path.dirname(__file__), "man_pages")


MAN_PAGES = {
    "echo": "echo [ -n ] TEXT... [ > file ] [ >> file ]\nPrint text. Supports -n and simple redirection.",
    "cat": "cat FILE...\nDisplay file contents.",
    "ls": "ls [ -a ] [-l] [path]\nList directory contents (use -a to show hidden, -l for long).",
    "cd": "cd [path]\nChange directory (relative or absolute).",
    "pwd": "pwd\nPrint current working directory.",
    "whoami": "whoami\nPrint current logged in user.",
    "mkdir": "mkdir DIR\nCreate a directory.",
    "rm": "rm [-r] [-f] PATH\nRemove file or directory recursively if -r present.",
    "touch": "touch FILE\nCreate empty file or update mtime.",
    "chmod": "chmod MODE PATH\nSet simple mode string (e.g. rwx).",
    "chown": "chown [-R] OWNER PATH\nSet owner for path (recursive with -R).",
    "save": "save FILE\nSave the VFS to a JSON file.",
    "load": "load FILE\nLoad the VFS JSON file (replaces current VFS).",
    "history": "history\nShow command history.",
    "adduser": "adduser [--sudo] USERNAME\nCreate a new user and home directory.",
    "passwd": "passwd [USERNAME]\nChange password (root may change others).",
    "stat": "stat FILE\nShow metadata for a file or dir.",
    "sudo": "sudo COMMAND\nRun a command as root (prompts for password if needed).",
    "man": "man TOPIC\nShow manual page for TOPIC. Use 'man -k keyword' to search.",
}

def old_man(vfs, state, args=None, capture=False):
    args = args or []
    if not args:
        msg = "man: missing topic\n"
        if capture: return msg
        print(msg, end=""); return
    if args[0] == "-k":
        if len(args) < 2:
            msg = "man: -k requires a keyword\n"
            if capture: return msg
            print(msg, end=""); return
        kw = args[1].lower()
        matches = []
        for k, p in MAN_PAGES.items():
            if kw in k.lower() or kw in p.lower():
                matches.append(f"{k} - {p.splitlines()[0]}")
        out = ("\n".join(matches) + ("\n" if matches else "No matches\n"))
        if capture: return out
        print(out, end=""); return
    topic = args[0]
    page = MAN_PAGES.get(topic)
    if not page:
        msg = f"man: no entry for {topic}\n"
        if capture: return msg
        print(msg, end=""); return
    out = page + "\n"
    if capture: return out
    print(out, end="")

def man(vfs=None, state=None, args=None, capture=False):
    if not args:
        print("man: missing command name")
        return
    cmd = args[0]
    man_file = os.path.join(MAN_DIR, f"{cmd}.txt")
    if os.path.exists(man_file):
        with open(man_file, "r") as f:
            print(f.read())
    else:
        print(f"No manual entry for {cmd}")

    if not args:
        print("man: missing command name")
        return
    cmd = args[0]
    man_file = os.path.join(MAN_DIR, f"{cmd}.txt")
    if os.path.exists(man_file):
        with open(man_file, "r") as f:
            print(f.read())
    else:
        print(f"No manual entry for {cmd}")