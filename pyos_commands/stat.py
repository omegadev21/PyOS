import time
from pyos_commands.utils.utils import resolve_path, get_node, get_meta

def _fmt_time(ts):
    try:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
    except Exception:
        return str(ts)

def stat(vfs, state, args=None, capture=False):
    args = args or []
    if not args:
        msg = "stat: missing operand\n"
        if capture: return msg
        print(msg, end=""); return

    out = ""
    for a in args:
        path = resolve_path(vfs, state["cwd"], a)
        node = get_node(vfs, path)
        if node is None:
            line = f"stat: cannot stat '{a}': No such file or directory\n"
            out += line
            if not capture: print(line, end="")
            continue
        meta = get_meta(vfs, path)
        owner = meta.get("owner","")
        mode = meta.get("mode","")
        ctime = _fmt_time(meta.get("ctime",0))
        mtime = _fmt_time(meta.get("mtime",0))
        size = len(node) if isinstance(node, str) else sum(len(get_node(vfs, (path.rstrip('/') + '/' + k).replace('//','/')) or "") for k in node) if isinstance(node, dict) else 0
        t = "directory" if isinstance(node, dict) else "file"
        line = (f"  File: {path}\n"
                f"  Type: {t}\n"
                f"  Size: {size}\n"
                f"  Owner: {owner}\n"
                f"  Mode: {mode}\n"
                f"  Ctime: {ctime}\n"
                f"  Mtime: {mtime}\n")
        out += line
        if not capture:
            print(line, end="")
    return out if capture else None
