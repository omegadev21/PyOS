import os
import time
import json
import shutil
import threading
import importlib.util
import urllib.request
import zipfile, requests
from urllib.parse import urljoin

# Configure these to match your update server
VERSION_FILE = "version.json"
UPDATE_BASE = "http://localhost:8080/pyos-server/"  # <<-- set to your real server
VERSION_FILE = "version.json"  # should contain {"version":"1.0.2", "files":[...]}
CHECK_INTERVAL = 60  # seconds between checks
PACKAGES_DIR = os.path.join(os.path.dirname(__file__), "pyos_commands")
MAN_DIR = os.path.join(os.path.dirname(__file__), "man_pages")

# global state (set by import)
_update_state = {"last_checked": None, "available": None}

def _fetch_json(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return None

def _download_file(url, dest):
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    with urllib.request.urlopen(url, timeout=15) as resp:
        data = resp.read()
    with open(dest, "wb") as f:
        f.write(data)

# def install_package(name, dest="."):
#     pkg_url = urljoin(UPDATE_BASE, f"packages/{name}.json")
#     pkg = _fetch_json(pkg_url)
#     if not pkg:
#         return f"install: package '{name}' not found\n"

#     results = []
#     for f in pkg.get("files", []):
#         rel = f["path"]
#         url = urljoin(UPDATE_BASE, f["url"])
#         try:
#             _download_file(url, os.path.join(dest, rel))
#             results.append(f"{rel}: ok")
#         except Exception as e:
#             results.append(f"{rel}: error {e}")
#     return "Installed package: " + name + "\n" + "\n".join(results) + "\n"

def _fetch_version_info():
    try:
        url = urljoin(UPDATE_BASE, VERSION_FILE)
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data)
    except Exception:
        return None

def scanner_thread(notify_fn):
    while True:
        info = _fetch_version_info()
        _update_state["last_checked"] = time.time()
        if info:
            remote_version = info.get("version")
            if _update_state.get("current_version") != remote_version:
                _update_state["available"] = info
                notify_fn(f"Update available: {remote_version}")
        time.sleep(CHECK_INTERVAL)

def start_scanner(notify_fn):
    t = threading.Thread(target=scanner_thread, args=(notify_fn,), daemon=True)
    t.start()
    return t

def install_from_info(info, apply=True, dest="."):
    """
    Install/update from JSON manifest:
      info = {"version": "...", "files": [{"path": "...", "url": "..."}]}
    """
    results = []
    for f in info.get("files", []):
        rel = f.get("path")
        url = urljoin(UPDATE_BASE, f.get("url", rel))
        try:
            outpath = os.path.join(dest, rel)
            os.makedirs(os.path.dirname(outpath) or ".", exist_ok=True)
            with urllib.request.urlopen(url, timeout=15) as resp:
                data = resp.read()
            if apply:
                with open(outpath, "wb") as fh:
                    fh.write(data)
            results.append((rel, "ok"))
        except Exception as e:
            results.append((rel, f"error: {e}"))
    return results

def install_update(dest="."):
    info = _fetch_json(urljoin(UPDATE_BASE, VERSION_FILE))
    if not info:
        return "install: failed to fetch update info\n"

    results = []
    for f in info.get("files", []):
        rel = f["path"]
        url = urljoin(UPDATE_BASE, f["url"])
        try:
            _download_file(url, os.path.join(dest, rel))
            results.append(f"{rel}: ok")
        except Exception as e:
            results.append(f"{rel}: error {e}")
    return "Applied full update\n" + "\n".join(results) + "\n"

def load_command_from_file(filepath, name):
    """Dynamically load a command module and return it."""
    spec = importlib.util.spec_from_file_location(name, filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def install_package(pkg):
    url = urljoin(UPDATE_BASE, f"packages/{pkg}")
    print(f"Fetching package from {url}...")
    try:
        # Download package
        resp = requests.get(url, timeout=15)
        pkg_file = f"/tmp/{pkg}.zip"
        with open(pkg_file, "wb") as f:
            f.write(resp.content)

        # Extract package into a temp folder
        extract_dir = f"/tmp/{pkg}_extracted"
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        with zipfile.ZipFile(pkg_file, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # Move bin/ files into pyos_commands/
        bin_dir = os.path.join(extract_dir, "bin")
        if os.path.exists(bin_dir):
            for file in os.listdir(bin_dir):
                src = os.path.join(bin_dir, file)
                dest = os.path.join(PACKAGES_DIR, file)
                shutil.copy(src, dest)

                # Register dynamically in cmds_mapper
                if file.endswith(".py"):
                    cmd_name = file.replace(".py", "")
                    mod = load_command_from_file(dest, cmd_name)
                    if hasattr(mod, "run"):
                        import pyos_commands.utils.cmds_mapper as cmds_mapper
                        cmds_mapper.COMMANDS[cmd_name] = mod.run

        # Move man_pages/ into global man_pages/
        man_pkg_dir = os.path.join(extract_dir, "man_pages")
        if os.path.exists(man_pkg_dir):
            for file in os.listdir(man_pkg_dir):
                shutil.copy(os.path.join(man_pkg_dir, file), MAN_DIR)

        return f"Package '{pkg}' installed successfully and loaded.\n"
    except Exception as e:
        return f"install: failed to install {pkg}: {e}\n"

def install_cmd(vfs=None, state=None, args=None, capture=False):
    args = args or []
    if not args:
        msg = "install: missing arguments\n"
        return msg if capture else print(msg, end="")

    if args[0] in ("--update", "-u"):
        msg = install_update()
    else:
        msg = install_package(args[0])

    if capture:
        return msg
    print(msg, end="")