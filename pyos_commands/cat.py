import os
from pyos_commands.utils.utils import resolve_path, get_node

def cat(vfs, state, args=None, input_text=None, capture=False):
    """
    cat [file...]
    If input_text is provided (from pipe), prints/returns it.
    """
    args = args or []
    out = ""
    if input_text is not None:
        out += input_text
        if capture:
            return out
        else:
            print(input_text, end="")
            return

    if not args:
        msg = "cat: missing filename\n"
        if capture:
            return msg
        else:
            print(msg, end="")
            return

    for fname in args:
        path = resolve_path(vfs, state["cwd"], fname)
        node = get_node(vfs, path)
        if node is None:
            msg = f"cat: {fname}: No such file\n"
            out += msg
            if not capture:
                print(msg, end="")
            continue
        if isinstance(node, dict):
            msg = f"cat: {fname}: Is a directory\n"
            out += msg
            if not capture:
                print(msg, end="")
            continue
        # file (string)
        out += node
        if not capture:
            print(node, end="")
    return out if capture else None
