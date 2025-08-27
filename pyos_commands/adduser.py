from getpass import getpass
from pyos_commands.utils.utils import ensure_dir, set_meta
from pyos_commands.utils.userdb import add_user, get_user, list_users, set_sudo

def adduser(vfs, state, args=None, capture=False):
    args = args or []
    sudo = False
    if not args:
        msg = "adduser: missing username\n"
        if capture: return msg
        print(msg, end=""); return
    if args[0] == "--sudo":
        sudo = True
        if len(args) < 2:
            msg = "adduser: missing username\n"
            if capture: return msg
            print(msg, end=""); return
        username = args[1]
    else:
        username = args[0]
    if get_user(username):
        msg = f"adduser: user '{username}' already exists\n"
        if capture: return msg
        print(msg, end=""); return
    pwd = getpass(f"Password for {username}: ")
    pwd2 = getpass(f"Confirm password for {username}: ")
    if pwd != pwd2:
        msg = "adduser: passwords do not match\n"
        if capture: return msg
        print(msg, end=""); return
    add_user(username, pwd, sudo=sudo)
    # create home dir in VFS
    home = f"/home/{username}"
    ensure_dir(vfs, "/home")
    ensure_dir(vfs, home)
    set_meta(vfs, home, owner=username, mode="rwx")
    msg = f"User {username} created with home {home} (sudo={sudo})\n"
    if capture: return msg
    print(msg, end=""); return
