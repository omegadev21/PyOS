import shlex
from pyos_commands.utils.utils import resolve_path
from pyos_commands.utils.cmds_mapper import COMMANDS
from pyos_commands.utils.system_config import VFS, current_state
from prompt_toolkit.completion import Completer, Completion


def _split_path_for_completion(path):
    return [p for p in path.strip("/").split("/") if p] if path != "/" else []

def _complete_path(prefix, cwd):
    from pyos_commands.utils.utils import list_dir as _list_dir, get_node as _get_node

    if prefix.startswith("/"):
        base = "/"
        rest = prefix[1:]
    else:
        base = cwd
        rest = prefix

    if "/" in rest:
        dirpart, last = rest.rsplit("/", 1)
        dirpath = resolve_path(VFS, base, dirpart or "")
    else:
        dirpath = resolve_path(VFS, base, "")
        last = rest

    try:
        items = _list_dir(VFS, dirpath, show_all=True)
    except Exception:
        items = []

    matches = []
    for it in items:
        if it.startswith(last):
            full = (dirpath.rstrip("/") + "/" + it).replace("//", "/")
            node = _get_node(VFS, full)
            display = it + ("/" if isinstance(node, dict) else "")
            if prefix.startswith("/"):
                matches.append((dirpath.rstrip("/") + "/" + display).replace("//", "/"))
            else:
                matches.append(display)

    dirs = [m for m in matches if m.endswith("/")]
    files = [m for m in matches if not m.endswith("/")]
    return dirs + files

class PyOSCompleter(Completer):
    def get_completions(self, document, complete_event):
        buffer = document.text_before_cursor
        try:
            parts = shlex.split(buffer)
        except Exception:
            parts = buffer.split()

        text = document.get_word_under_cursor()

        if not parts or (len(parts) == 1 and not buffer.endswith(" ")):
            # completing a command
            options = [c for c in list(COMMANDS.keys()) + ["exit", "!"] if c.startswith(text)]
        else:
            # completing a path
            options = _complete_path(text, current_state.get("cwd", "/"))

        for option in options:
            yield Completion(option, start_position=-len(text))
