import os

def history_cmd(vfs, state, args=None, capture=False):
    history = state.get("history", [])
    out = ""
    for i, cmd in enumerate(history, 1):
        line = f"{i}  {cmd}\n"
        out += line
        if not capture:
            print(line, end="")
    return out if capture else None