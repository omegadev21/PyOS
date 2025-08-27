def whoami(vfs, state, args=None, capture=False):
    out = state.get("user", "") + ("\n")
    if capture:
        return out
    else:
        print(out, end="")
