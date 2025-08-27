from pyos_commands.utils.utils import get_meta, set_meta, get_node

def chmod(vfs, state, args=None):
    args = args or []
    if len(args) < 2:
        print("chmod: missing operand")
        return
    mode = args[0]
    path = args[1]
    from pyos_commands.utils.utils import resolve_path
    full = resolve_path(vfs, state["cwd"], path)
    node = get_node(vfs, full)
    if node is None:
        print(f"chmod: cannot access '{path}': No such file or directory")
        return
    set_meta(vfs, full, mode=mode)