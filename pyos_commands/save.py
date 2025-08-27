from pyos_commands.utils.utils import save_vfs
def save(vfs, state, args=None):
    args = args or []
    path = args[0] if args else "pyos_vfs.json"
    try:
        save_vfs(vfs, path)
        print(f"VFS saved to {path}")
    except Exception as e:
        print(f"save: error: {e}")