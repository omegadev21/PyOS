from pyos_commands.utils.userdb import set_password, get_user, verify_user

def passwd(vfs, state, args=None, capture=False):
    args = args or []
    user = state.get("user")
    if args and state.get("user") == "root":
        # root can change other users' passwords: passwd username
        target = args[0]
    else:
        target = user
    if not target:
        msg = "passwd: no user\n"
        if capture: return msg
        print(msg, end=""); return

    entry = get_user(target)
    if entry is None:
        msg = f"passwd: user '{target}' does not exist\n"
        if capture: return msg
        print(msg, end=""); return
    from getpass import getpass
    # if not root and changing another user, require current password
    if state.get("user") != "root" and target == user:
        cur = getpass("Current password: ")
        if not verify_user(user, cur):
            msg = "passwd: authentication failure\n"
            if capture: return msg
            print(msg, end=""); return
    new1 = getpass("New password: ")
    new2 = getpass("Retype new password: ")


    if new1 != new2:
        msg = "passwd: passwords do not match\n"
        if capture: return msg
        print(msg, end=""); return
    set_password(user,new1)
    msg = "passwd: password updated\n"
    if capture: return msg
    print(msg, end="")
