import os
from pyos_commands.utils.utils import resolve_path, get_node, set_node, ensure_dir

def echo(vfs, state, args=None, capture=False):
    """
    echo [ -n ] TEXT... [ > file ] [ >> file ]
    If capture=True, returns the output string instead of printing.
    """
    args = args or []
    if not args:
        out = "\n"
        if capture:
            return out
        else:
            print(out, end="")
            return

    newline = True
    parts = list(args)
    if parts and parts[0] == "-n":
        newline = False
        parts = parts[1:]

    # detect redirection
    if ">" in parts or ">>" in parts:
        if ">>" in parts:
            idx = parts.index(">>")
            filename = parts[idx + 1] if idx + 1 < len(parts) else None
            content = " ".join(parts[:idx])
            if not filename:
                msg = "echo: missing filename for >>\n"
                if capture:
                    return msg
                else:
                    print(msg, end="")
                    return
            target_path = resolve_path(vfs, state["cwd"], filename)
            # ensure parent dirs exist if filename contains directories
            parent = "/" + "/".join(target_path.strip("/").split("/")[:-1]) if "/" in target_path.strip("/") else "/"
            if parent != "/":
                ensure_dir(vfs, parent)
            existing = get_node(vfs, target_path)
            if existing is None:
                set_node(vfs, target_path, (content + ("" if not newline else "\n")))
            else:
                if isinstance(existing, dict):
                    msg = f"echo: {filename}: Is a directory\n"
                    if capture:
                        return msg
                    else:
                        print(msg, end="")
                        return
                set_node(vfs, target_path, existing + content + ("" if not newline else "\n"))
            return "" if capture else None
        else:  # ">"
            idx = parts.index(">")
            filename = parts[idx + 1] if idx + 1 < len(parts) else None
            content = " ".join(parts[:idx])
            if not filename:
                msg = "echo: missing filename for >\n"
                if capture:
                    return msg
                else:
                    print(msg, end="")
                    return
            target_path = resolve_path(vfs, state["cwd"], filename)
            parent = "/" + "/".join(target_path.strip("/").split("/")[:-1]) if "/" in target_path.strip("/") else "/"
            if parent != "/":
                ensure_dir(vfs, parent)
            set_node(vfs, target_path, content + ("" if not newline else "\n"))
            return "" if capture else None

    text = " ".join(parts) + ("" if not newline else "\n")
    if capture:
        return text
    else:
        print(text, end="")
        return
