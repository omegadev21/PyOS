import sys
from pyos_commands.utils.userdb import remove_user, get_user
from pyos_commands.utils.utils import resolve_path, get_node, remove_node

def _confirm(prompt):
    ans = input(prompt + " [y/N]: ").strip().lower()
    return ans in ("y", "yes")

def _recursive_remove(vfs, path):
    node = get_node(vfs, path)
    if node is None:
        raise FileNotFoundError(path)
    if isinstance(node, dict):
        for name in list(node.keys()):
            child = (path.rstrip("/") + "/" + name).replace("//","/")
            _recursive_remove(vfs, child)
    remove_node(vfs, path)

def rm(vfs, state, args=None, capture=False):
    args = args or []
    if not args:
        msg = "rm: missing operand\n"
        if capture: return msg
        print(msg, end=""); return
    recursive = "-r" in args or "-R" in args
    force = "-f" in args
    targets = [a for a in args if not a.startswith("-")]
    out = ""
    for t in targets:
        path = resolve_path(vfs, state["cwd"], t)
        node = get_node(vfs, path)
        if node is None:
            msg = f"rm: cannot remove '{t}': No such file or directory\n"
            out += msg
            if not capture: print(msg, end=""); continue
        # special: if removing a user home dir directly, remove user too
        if path.startswith("/home/") and path.count("/") == 2:
            username = path.split("/")[2]
            # confirm
            if not force:
                ok = _confirm(f"rm: this will delete user '{username}' and their home. Continue?")
                if not ok:
                    msg = f"rm: skipped '{t}'\n"
                    out += msg
                    if not capture: print(msg, end=""); continue
            # delete vfs node(s)
            try:
                if isinstance(node, dict):
                    if recursive:
                        _recursive_remove(vfs, path)
                    else:
                        # remove directory directly
                        remove_node(vfs, path)
                else:
                    remove_node(vfs, path)
            except Exception as e:
                msg = f"rm: error removing '{t}': {e}\n"
                out += msg
                if not capture: print(msg, end=""); continue
            # then remove user from DB
            try:
                remove_user(username)
            except Exception:
                pass
            msg = f"rm: removed user {username} and home {path}\n"
            out += msg
            if not capture: print(msg, end=""); continue
        # normal removal
        if isinstance(node, dict) and not recursive:
            msg = f"rm: cannot remove '{t}': Is a directory (use -r)\n"
            out += msg
            if not capture: print(msg, end=""); continue
        if isinstance(node, dict) and recursive and not force:
            ok = _confirm(f"rm: descend into directory '{t}' and remove recursively?")
            if not ok:
                msg = f"rm: skipped '{t}'\n"
                out += msg
                if not capture: print(msg, end=""); continue
        try:
            if isinstance(node, dict):
                _recursive_remove(vfs, path)
            else:
                remove_node(vfs, path)
        except Exception as e:
            msg = f"rm: error removing '{t}': {e}\n"
            out += msg
            if not capture: print(msg, end="")
    if capture: return out
