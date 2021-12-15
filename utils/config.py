import json
import os
import getpass

from .resource_path import resource_path

def checkForConfig():
    username = getpass.getuser()
    if not os.path.isdir(f"/Users/{username}/Library/Preferences/bennyontop.clipboarduploader/"): os.system(f"mkdir /Users/{username}/Library/Preferences/bennyontop.clipboarduploader/")
    if not os.path.isfile(f"/Users/{username}/Library/Preferences/bennyontop.clipboarduploader/config.json"): 
        os.system(f"touch /Users/{username}/Library/Preferences/bennyontop.clipboarduploader/config.json")
        with open(f"/Users/{username}/Library/Preferences/bennyontop.clipboarduploader/config.json", "w") as f: json.dump({}, f)
    cfg = json.load(open(f"/Users/{username}/Library/Preferences/bennyontop.clipboarduploader/config.json"))
    if "file_fieldname" not in cfg: cfg["file_fieldname"] = ""
    if "request" not in cfg: cfg["request"] = {"method": "", "url": ""}
    if "params" not in cfg: cfg["params"] = {}
    json.dump(cfg, open(f"/Users/{username}/Library/Preferences/bennyontop.clipboarduploader/config.json", "w"), indent=4, sort_keys=False)

class Config:
    def __init__(self):
        checkForConfig()
        self.config = json.load(open(resource_path(f"/Users/{getpass.getuser()}/Library/Preferences/bennyontop.clipboarduploader/config.json")))

    def get_file_fieldname(self):
        return self.config['file_fieldname']

    def get_request(self):
        return self.config['request']
    
    def get_params(self):
        return self.config['params']