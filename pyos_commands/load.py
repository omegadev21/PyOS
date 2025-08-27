from pyos_commands.utils.utils import load_vfs
def load(vfs, state, args=None):
    args = args or []
    path = args[0] if args else "pyos_vfs.json"
    try:
        new = load_vfs(path)
        # mutate existing vfs in-place: clear and update
        vfs.clear()
        vfs.update(new)
        print(f"VFS loaded from {path}")
    except Exception as e:
        print(f"load: error: {e}")