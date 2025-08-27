from pyos_commands.utils.utils import resolve_path, get_node, set_node, ensure_dir, set_meta, read_file
import time

def touch(vfs, state, args=None, capture=False):
    args = args or []
    if not args:
        msg = "touch: missing file operand\n"
        if capture: return msg
        print(msg, end=""); return
    path = resolve_path(vfs, state["cwd"], args[0])
    parent = "/" + "/".join(path.strip("/").split("/")[:-1]) if "/" in path.strip("/") else "/"
    if parent != "/":
        ensure_dir(vfs, parent)
    node = get_node(vfs, path)
    now = time.time()
    if node is None:
        set_node(vfs, path, "")  # create empty file
        set_meta(vfs, path, ctime=now, mtime=now, owner=state.get("user","root"))
    else:
        # update mtime
        set_meta(vfs, path, mtime=now)
    if capture:
        return ""
