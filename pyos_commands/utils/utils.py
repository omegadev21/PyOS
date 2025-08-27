import os
import json
import time

def _split_path(path):
    if path == "/":
        return []
    return [p for p in path.strip("/").split("/") if p]

def resolve_path(vfs, cwd, path):
    if not path:
        return cwd
    if path.startswith("/"):
        parts = _split_path(path)
    else:
        parts = _split_path(cwd) + _split_path(path)
    stack = []
    for p in parts:
        if p == ".":
            continue
        if p == "..":
            if stack:
                stack.pop()
            continue
        stack.append(p)
    return "/" + "/".join(stack) if stack else "/"

def _ensure_meta_root(vfs):
    if "_meta" not in vfs:
        vfs["_meta"] = {}

def get_node(vfs, path):
    if path == "/":
        return vfs["/"]
    node = vfs["/"]
    for part in _split_path(path):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node

def set_node(vfs, path, value):
    if path == "/":
        raise KeyError("Cannot overwrite root")
    parts = _split_path(path)
    parent = vfs["/"]
    for p in parts[:-1]:
        if p not in parent or not isinstance(parent[p], dict):
            raise KeyError("Parent directory does not exist")
        parent = parent[p]
    parent[parts[-1]] = value
    # set mtime metadata
    _ensure_meta_root(vfs)
    meta = vfs["_meta"].get(path, {})
    meta.setdefault("ctime", time.time())
    meta["mtime"] = time.time()
    vfs["_meta"][path] = meta

def ensure_dir(vfs, path):
    node = vfs["/"]
    built = []
    for part in _split_path(path):
        built.append(part)
        if part not in node:
            node[part] = {}
            # init metadata
            ppath = "/" + "/".join(built)
            _ensure_meta_root(vfs)
            vfs["_meta"].setdefault(ppath, {"owner": "root", "mode": "rwx", "ctime": time.time(), "mtime": time.time()})
        elif not isinstance(node[part], dict):
            raise KeyError(f"Not a directory: {path}")
        node = node[part]

def remove_node(vfs, path):
    if path == "/":
        raise KeyError("Cannot remove root")
    parts = _split_path(path)
    parent = vfs["/"]
    for p in parts[:-1]:
        if p not in parent or not isinstance(parent[p], dict):
            raise KeyError("Parent directory does not exist")
        parent = parent[p]
    if parts[-1] not in parent:
        raise KeyError("No such file or directory")
    del parent[parts[-1]]
    # remove metadata
    _ensure_meta_root(vfs)
    if path in vfs["_meta"]:
        del vfs["_meta"][path]
    # also remove any child metadata (if directory)
    keys_to_del = [k for k in list(vfs["_meta"].keys()) if k.startswith(path.rstrip("/") + "/")]
    for k in keys_to_del:
        del vfs["_meta"][k]

def set_meta(vfs, path, owner=None, mode=None, hidden=None, ctime=None, mtime=None):
    _ensure_meta_root(vfs)
    meta = vfs["_meta"].get(path, {})
    if owner is not None:
        meta["owner"] = owner
    if mode is not None:
        meta["mode"] = mode
    if hidden is not None:
        meta["hidden"] = bool(hidden)
    if ctime is not None:
        meta["ctime"] = ctime
    if mtime is not None:
        meta["mtime"] = mtime
    vfs["_meta"][path] = meta

def get_meta(vfs, path):
    _ensure_meta_root(vfs)
    return vfs["_meta"].get(path, {})

def read_file(vfs, path):
    node = get_node(vfs, path)
    if node is None:
        return None
    if isinstance(node, dict):
        raise IsADirectoryError(path)
    return node

def write_file(vfs, path, content, owner=None):
    parent = "/" + "/".join(path.strip("/").split("/")[:-1]) if "/" in path.strip("/") else "/"
    if parent != "/":
        ensure_dir(vfs, parent)
    set_node(vfs, path, content)
    _ensure_meta_root(vfs)
    meta = vfs["_meta"].get(path, {})
    if owner:
        meta["owner"] = owner
    meta["mtime"] = time.time()
    meta.setdefault("ctime", time.time())
    vfs["_meta"][path] = meta

def list_dir(vfs, path, show_all=False):
    node = get_node(vfs, path)
    if node is None:
        raise FileNotFoundError(path)
    if not isinstance(node, dict):
        return [path.strip("/").split("/")[-1] or "/"]
    items = list(node.keys())
    if not show_all:
        out = []
        for name in items:
            full = (path.rstrip("/") + "/" + name).replace("//", "/")
            meta = get_meta(vfs, full)
            if name.startswith(".") or meta.get("hidden"):
                continue
            out.append(name)
        return out
    return items

def save_vfs(vfs, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(vfs, f, indent=2, ensure_ascii=False)

def load_vfs(path):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)