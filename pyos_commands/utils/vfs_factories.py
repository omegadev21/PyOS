def make_preinitialized_vfs():
    v = {
        "/": {
            "home": {
                "bob": {"docs": {}, "notes.txt": "Welcome Bob!\n"},
                "sam": {}
            },
            "etc": {"config.txt": "system=PyOS-00\nversion=0.1\n"},
            "tmp": {}
        }
    }
    v["_meta"] = {}
    v["_meta"]["/"] = {"owner": "root", "mode": "rwx"}
    v["_meta"]["/home"] = {"owner": "root", "mode": "rwx"}
    v["_meta"]["/home/bob"] = {"owner": "bob", "mode": "rwx"}
    return v

def make_scratch_vfs():
    v = {"/": {"home": {}}, "_meta": {"/": {"owner": "root", "mode": "rwx"}}}
    return v

def make_template_vfs():
    v = {
        "/": {
            "home": {},
            "etc": {},
            "tmp": {},
        }
    }

    v["_meta"] = {}
    v["_meta"]["/"] = {"owner": "root", "mode": "rwx"}
    v["_meta"]["/home"] = {"owner": "root", "mode": "rwx"}
    
    return v
