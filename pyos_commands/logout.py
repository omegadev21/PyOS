def logout(vfs, state, args=None):
    # signal to main loop by setting a flag
    state["_logout"] = True