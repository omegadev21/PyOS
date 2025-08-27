import os

from pyos_commands.ls import ls
from pyos_commands.cd import cd
from pyos_commands.rm import rm
from pyos_commands.cat import cat
from pyos_commands.pwd import pwd
# from pyos_commands.man import man
from pyos_commands.sudo import sudo
from pyos_commands.echo import echo
from pyos_commands.save import save
from pyos_commands.load import load
from pyos_commands.stat import stat
from pyos_commands.nano import nano
from pyos_commands.mkdir import mkdir
from pyos_commands.touch import touch
from pyos_commands.chown import chown
from pyos_commands.chmod import chmod
from pyos_commands.whoami import whoami
from pyos_commands.help import help_cmd
from pyos_commands.logout import logout
from pyos_commands.passwd import passwd
from pyos_commands.adduser import adduser
from pyos_commands.clear import clear_cmd
from pyos_commands.history import history_cmd
from pyos_commands.installer import install_cmd
from pyos_commands.removeuser import removeuser

MAN_DIR = os.path.join(os.path.dirname(__file__), "man_pages")

def man(vfs=None, state=None, args=None, capture=False):
    if not args:
        print("man: missing command name")
        return
    cmd = args[0]
    man_file = os.path.join(MAN_DIR, f"{cmd}.txt")
    if os.path.exists(man_file):
        with open(man_file, "r") as f:
            print(f.read())
    else:
        print(f"No manual entry for {cmd}")

COMMANDS = {
    "echo": echo,
    "cat": cat,
    "ls": ls,
    "cd": cd,
    "mkdir": mkdir,
    "rm": rm,
    "touch": touch,
    "clear": clear_cmd,
    "history": history_cmd,
    "help": help_cmd,
    "pwd": pwd,
    "whoami": whoami,
    "logout": logout,
    "man": man,
    "chown": chown,
    "chmod": chmod,
    "save": save,
    "load": load,
    "adduser" : adduser,
    "stat": stat,
    "passwd": passwd,
    "sudo": sudo,
    "removeuser": removeuser, 
    "nano": nano, 
}

# "install": install_cmd, dosent work
