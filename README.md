# PyOS 🐚

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
login: bob
PyOS-O1 Password: ***********

Welcome To PyOS (Shell/Python 3.13.0)

 * Documentation:     https://website.com
 * Management:        https://website.com
 * Support:           https://website.com

welcome, bob!

bob@PyOS-01:~$ echo "Hello World"
Hello World

bob@PyOS-01:~$ sudo cat /etc/config.txt
system=PyOS-01
version=01
```

Exit with:

```bash
exit
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
