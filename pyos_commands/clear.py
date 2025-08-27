import os

def clear_cmd(vfs, state, args=None):
    """
    Mimics the clear command.
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
