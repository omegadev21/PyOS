import os
from pyos_commands.utils.utils import resolve_path, get_node

def cd(vfs, state, args=None):
    """
    cd [path]
    Updates state['cwd'] (VFS-aware). Enforces root jail.
    """
    args = args or []
    if not args:
        # go to user's home if available, else root
        user = state.get("user")
        home_path = f"/home/{user}" if user else "/"
        # if user is root, home is "/"
        if user == "root":
            state["cwd"] = "/"
        else:
            # if home exists
            if get_node(vfs, home_path) is not None:
                state["cwd"] = home_path
            else:
                state["cwd"] = "/"
        return

    path = args[0]
    new_path = resolve_path(vfs, state["cwd"], path)
    node = get_node(vfs, new_path)
    if node is None:
        print(f"cd: {path}: No such file or directory")
        return
    if not isinstance(node, dict):
        print(f"cd: {path}: Not a directory")
        return
    # update cwd
    state["cwd"] = new_path
