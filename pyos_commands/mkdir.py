import os
from pyos_commands.utils.utils import resolve_path, get_node, set_node, ensure_dir

def mkdir(vfs, state, args=None):
    args = args or []
    if not args:
        print("mkdir: missing operand")
        return
    path = resolve_path(vfs, state["cwd"], args[0])
    # ensure parent exists
    parent = "/" + "/".join(path.strip("/").split("/")[:-1]) if "/" in path.strip("/") else "/"
    if parent != "/":
        try:
            ensure_dir(vfs, parent)  # ensure parents exist
        except Exception as e:
            print(f"mkdir: {e}")
            return
    # check exists
    if get_node(vfs, path) is not None:
        print(f"mkdir: cannot create directory '{args[0]}': File exists")
        return
    # create dir
    set_node(vfs, path, {})
