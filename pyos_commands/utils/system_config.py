from pyos_commands.utils.vfs_factories import make_preinitialized_vfs, make_scratch_vfs, make_template_vfs

msg ="""
Welcome To PyOS (Shell/Python 3.13.0)

 * Documentation:     https://website.com
 * Management:        https://website.com
 * Support:           https://website.com

0 Updates can be applied immediately
"""
msg2 ="""
Welcome To PyOS (Shell/Python 3.13.0)

 * Documentation:     https://website.com
 * Management:        https://website.com
 * Support:           https://website.com
"""
msg3 = """
PyOS (Shell/Python 3.13.0)
"""
msg4 =r"""
╔════════════════════════════════╗
║        Welcome to PyOS         ║
╚════════════════════════════════╝
"""

msg5 = """
PyOS (Shell Version 0.01)
"""

current_state = {"cwd": "/"}
AUTO_SAVE_PATH = "system_files/pyos_vfs.json"
SYSTEM_NAME = "PyOS-01"
OS_NAME = "PyOS"

VFS_MODE = "template" # or preinit or template

if VFS_MODE == "preinit":
    VFS = make_preinitialized_vfs()
elif VFS_MODE == "template":
    VFS = make_template_vfs()
else:
    VFS = make_scratch_vfs()

