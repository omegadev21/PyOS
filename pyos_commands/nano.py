import os
import tempfile
from getpass import getpass
from pyos_commands.utils.utils import resolve_path, get_node, write_file, read_file, set_meta, ensure_dir

def _system_editor():
    ed = os.environ.get("EDITOR")
    if ed:
        return ed
    if os.name == "nt":
        return "notepad"
    # prefer nano if available, otherwise vi
    for cand in ("nano", "vi", "vim"):
        if shutil.which(cand):
            return cand
    return None

import shutil
def nano(vfs, state, args=None, capture=False):
    args = args or []
    if not args:
        msg = "nano: missing filename\n"
        if capture: return msg
        print(msg, end=""); return
    fname = args[0]
    path = resolve_path(vfs, state["cwd"], fname)
    existing = None
    try:
        existing = read_file(vfs, path)
    except IsADirectoryError:
        msg = f"nano: {fname}: Is a directory\n"
        if capture: return msg
        print(msg, end=""); return
    # write to temp file
    fd, tmp = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    with open(tmp, "w", encoding="utf-8") as f:
        if existing:
            f.write(existing)
    editor = _system_editor()
    if editor:
        # use system editor
        os.system(f"{editor} {tmp}")
    else:
        # fallback simple line editor
        print("No system editor found. Using inline editor. End with a single '.' on a new line.")
        with open(tmp, "w", encoding="utf-8") as f:
            while True:
                try:
                    line = input()
                except EOFError:
                    break
                if line == ".":
                    break
                f.write(line + "\n")
    # read temp and store
    with open(tmp, "r", encoding="utf-8") as f:
        data = f.read()
    try:
        write_file(vfs, path, data, owner=state.get("user","root"))
        set_meta(vfs, path, owner=state.get("user","root"))
    except Exception:
        # create parent dirs then write
        parent = "/" + "/".join(path.strip("/").split("/")[:-1]) if "/" in path.strip("/") else "/"
        if parent != "/":
            ensure_dir(vfs, parent)
        write_file(vfs, path, data, owner=state.get("user","root"))
        set_meta(vfs, path, owner=state.get("user","root"))
    os.remove(tmp)
    if capture: return ""
    return
