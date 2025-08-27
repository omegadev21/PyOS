from pyos_commands.utils.userdb import get_user, remove_user
from pyos_commands.utils.utils import resolve_path, get_node, remove_node

def removeuser(vfs, state, args=None, capture=False):
    args = args or []
    if not args:
        msg = "removeuser: missing username\n"
        if capture: return msg
        print(msg, end=""); return
    username = args[0]
    u = get_user(username)
    if not u:
        msg = f"removeuser: user '{username}' does not exist\n"
        if capture: return msg
        print(msg, end=""); return
    # remove home dir
    home = f"/home/{username}"
    node = get_node(vfs, home)
    if node is not None:
        try:
            remove_node(vfs, home)
        except Exception as e:
            msg = f"removeuser: failed removing home dir: {e}\n"
            if capture: return msg
            print(msg, end=""); return
    remove_user(username)
    msg = f"User {username} removed and home {home} deleted (if present)\n"
    if capture: return msg
    print(msg, end=""); return
