from pyos_commands.utils.utils import get_meta, set_meta, get_node, resolve_path, _split_path

def _recursive_chown(vfs, path, owner):
    node = get_node(vfs, path)
    if node is None:
        return
    set_meta(vfs, path, owner=owner)
    if isinstance(node, dict):
        for name in node.keys():
            child = (path.rstrip("/") + "/" + name).replace("//","/")
            _recursive_chown(vfs, child, owner)

def chown(vfs, state, args=None, capture=False):
    args = args or []
    if not args or len(args) < 2:
        msg = "chown: missing operand\n"
        if capture: return msg
        print(msg, end=""); return
    recursive = False
    if args[0] == "-R":
        recursive = True
        args = args[1:]
    owner = args[0]
    path = args[1]
    full = resolve_path(vfs, state["cwd"], path)
    node = get_node(vfs, full)
    if node is None:
        msg = f"chown: cannot access '{path}': No such file or directory\n"
        if capture: return msg
        print(msg, end=""); return
    if recursive:
        _recursive_chown(vfs, full, owner)
    else:
        set_meta(vfs, full, owner=owner)
    if capture: return ""
