import time
from pyos_commands.utils.utils import resolve_path, get_node, get_meta, list_dir

def _fmt_time(ts):
    try:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
    except Exception:
        return str(ts)

def _size_of_node(vfs, path, node):
    if isinstance(node, str):
        return len(node)
    # simple directory size = number of entries
    return len(node) if isinstance(node, dict) else 0

def ls(vfs, state, args=None, capture=False):
    args = args or []
    show_all = "-a" in args
    long = "-l" in args
    # find path argument (first non-flag)
    path_arg = None
    for a in args:
        if not a.startswith("-"):
            path_arg = a
            break
    path = resolve_path(vfs, state["cwd"], path_arg) if path_arg else state["cwd"]
    node = get_node(vfs, path)
    if node is None:
        msg = f"ls: cannot access '{path_arg or path}': No such file or directory\n"
        if capture: return msg
        print(msg, end=""); return
    if not isinstance(node, dict):
        name = path.strip("/").split("/")[-1] or "/"
        if long:
            meta = get_meta(vfs, path)
            owner = meta.get("owner","")
            mode = meta.get("mode","")
            mtime = _fmt_time(meta.get("mtime",0))
            out = f"{mode:5} {owner:8} {_size_of_node(vfs,path,node):8} {mtime} {name}\n"
        else:
            out = name + "\n"
        if capture: return out
        print(out, end=""); return

    items = list(node.keys())
    if not show_all:
        items = [i for i in items if not i.startswith(".") and not get_meta(vfs, (path.rstrip("/")+"/"+i).replace("//","/")).get("hidden", False)]
    # for consistent ordering, sort directories first
    dirs = []
    files = []
    for i in items:
        child = node[i]
        if isinstance(child, dict):
            dirs.append(i)
        else:
            files.append(i)
    ordered = sorted(dirs) + sorted(files)
    out_lines = []
    for name in ordered:
        full = (path.rstrip("/") + "/" + name).replace("//","/")
        meta = get_meta(vfs, full)
        owner = meta.get("owner","")
        mode = meta.get("mode","")
        mtime = _fmt_time(meta.get("mtime",0))
        child = node.get(name)
        size = _size_of_node(vfs, full, child)
        if long:
            out_lines.append(f"{mode:5} {owner:8} {size:8} {mtime} {name}")
        else:
            out_lines.append(name)
    out = (" ".join(out_lines) + ("\n" if out_lines else ""))
    if capture: return out
    print(out, end=""); return
