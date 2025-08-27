def help_cmd(vfs, state, args=None, capture=False):
    commands = {
        "echo": "Prints text. Supports -n, >, >> and works with pipes.",
        "help":"Displays this help message",
        "cat": "Show file(s) contents.",
        "ls": "List directory contents (use -a to show hidden, -l for long).",
        "cd": "Change directory.",
        "pwd": "Print current working directory.",
        "whoami": "Print current logged in user.",
        "mkdir": "Create directory.",
        "rm": "Remove file or directory.",
        "touch": "Create an empty file or update timestamp.",
        "stat": "Show metadata (owner, mode, times).",
        "chmod": "Set mode string.",
        "chown": "Set owner.",
        "adduser": "Create user (supports --sudo).",
        "passwd": "Change password.",
        "save": "Save VFS to file.",
        "load": "Load VFS from file.",
        "man": "Show manual page for TOPIC. Use 'man -k keyword' to search.",
        "history": "Show command history.",
        "!n": "Replay history command number n.",
        "sudo": "Run a command as root (prompts for password if needed).",
        "logout": "Log out to login prompt.",
        "removeuser": "delete a user and their home directory",
        "exit": "Exit the PyOS shell.",
    }
    print("Available commands:")
    for k, v in commands.items():
        print(f"  {k:13} - {v}")
