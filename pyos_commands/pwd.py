def pwd(vfs, state, args=None, capture=False):
    out = state.get("cwd", "/") + ("\n")
    if capture:
        return out
    else:
        print(out, end="")