# PyOS

**PyOS** is a virtual operating system shell written in Python.
It simulates a Unix-like shell environment with a **virtual filesystem**, **user authentication**, and **command execution**.

---

## ✨ Features

- **Virtual File System (VFS)**
  - Preinitialized or scratch mode.
  - Auto-save to `pyos_vfs.json`.

- **SQLite User Database**
  - Users stored in `users.db`.
  - Passwords hashed with **bcrypt**.
  - Secure login with attempt limits.

- **User Management**
  - Built-in **root** superuser.
  - Sudo support for elevated commands.
  - Customizable per-user home directories (`/home/{username}`).

- **Command Execution**
  - Built-in commands: `cd`, `cat`, `echo`, `history`, `exit`, etc.
  - Pipelines with `|`.
  - `sudo` wrapper for root-level execution.
  - Tab autocompletion for commands and file paths.

---

## 🔑 Default User

| Username | Password     | Notes           |
|----------|--------------|-----------------|
| `root`   | `toor`       | Superuser       |

⚠️ **Change the default passwords immediately** after setup for security.

---

## 🚀 Getting Started

### Requirements
- Python 3.9+
- A Linux, Windows or Mac Operating system
---

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/your-username/pyos.git
cd pyos
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

(Other dependencies like `os`, `json`, `sqlite3`, `hashlib` are part of Python’s standard library.)

### 3. Run PyOS

```bash
python3 PyOS.py
```

---

## 📘 Example Session

```text
pyos version 0.01

╔════════════════════════════════╗
║        Welcome to PyOS         ║
╚════════════════════════════════╝

Please log in to continue...

PyOS Username: root
PyOS Password: ***********

PyOS (Shell Version 0.01)

Welcome back, root!

root@PyOS-01:~$ echo "Hello World"
Hello World

root@PyOS-01:~$ sudo cat /etc/config.txt
system=PyOS-01
version=01
```

Exit with:

```bash
exit
```
run help to get a list of commands:
```bash
help
```
---

## ⚡ Roadmap

* Expand command set (`mv`, `cp`, `ssh`, etc.)
* Add a package manager.
* Advanced permission system.
* Optional GUI front-end.

---
## 📝Note

* If you happen to come across any errors, unexpected behavior, or potential loopholes, please don’t hesitate to let me know. Your feedback is greatly appreciated, as it helps me identify and resolve issues more quickly, ensuring a smoother and more reliable experience for everyone.
---

## 📜 License

* [MIT License](LICENSE)
