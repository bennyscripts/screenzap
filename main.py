import tkinter as tk
import json
import os
import getpass

from utils.resource_path import resource_path
from utils import Config
from utils import Clipboard
from utils import Notifier
from utils import Uploader

notifier = Notifier()
uploader = Uploader()
uploadlog = []

index = 0
config = Config()
params = config.get_params()
addedParams = []

root = tk.Tk()
root.grid_columnconfigure(0, weight=1)

def checkClipboard():
    clipboard = Clipboard()

    if clipboard.get_png():
        imageData = clipboard.get_png()
        response = uploader.upload(imageData)

        notifier.send("Clipboard Uploader", "URL copied to clipboard")
        clipboard.set_text(response['url'])

        uploadlog.append(response['url'])

    root.after(1, checkClipboard)

def addNewParam():
    def addParam(key, value):
        global params, index, addedParams
        params[key] = value

        index += 1

        if key == "" or value == "": newWindow.destroy()

        label = tk.Label(root, text=key + ":")
        entry = tk.Entry(root)
        entry.insert(0, value)

        deleteBtn = tk.Button(root, text="x", command=lambda: deleteParam(key), width=1)
        
        deleteBtn.grid(row=index+5, column=2, sticky="e", padx=(0, 10))
        label.grid(row=index+5, column=0, sticky="w", padx=(10, 0))
        entry.grid(row=index+5, column=1, sticky="w", padx=(0, 0))

        addedParams.append([key, label, entry, deleteBtn])

        newWindow.destroy() 

    if len(addedParams) >= 10:
        notifier.send("Clipboard Uploader", "You can only add 10 parameters")
    else: 
        newWindow = tk.Toplevel(root)
        newWindow.title("Add new parameter")
        newWindow.resizable(False, False)

        tk.Label(newWindow, text="Parameter name:").grid(row=0, column=0, sticky="w", padx=(10, 0), pady=(10, 0))
        paramNameEntry = tk.Entry(newWindow)
        paramNameEntry.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=(10, 0))

        tk.Label(newWindow, text="Parameter value:").grid(row=1, column=0, sticky="w", padx=(10, 0))
        paramValueEntry = tk.Entry(newWindow)
        paramValueEntry.grid(row=1, column=1, sticky="w", padx=(0, 10))

        addBtn = tk.Button(newWindow, text="Add", command=lambda: addParam(paramNameEntry.get(), paramValueEntry.get())).grid(row=2, column=1, sticky="e", padx=(0, 10), pady=(0, 10))

        newWindow.mainloop()

def deleteParam(parameter):
    global index, params, addedParams

    index -= 1

    del params[parameter]
    for param in addedParams:
        if param[0] == parameter:
            param[1].destroy()
            param[2].destroy()
            param[3].destroy()
            addedParams.remove(param)
            break

def saveData():
    username = getpass.getuser()
    cfg = json.load(open(f"/Users/{username}/Library/Preferences/bennyontop.clipboarduploader/config.json"))
    fileFieldName = fileFieldnameEntry.get()
    requestMethod = requestMethodEntry.get()
    requestUrl = requestUrlEntry.get()

    for param in addedParams:
        params[param[0]] = param[2].get()

    cfg["file_fieldname"] = fileFieldName
    cfg["request"]["method"] = requestMethod
    cfg["request"]["url"] = requestUrl
    cfg["params"] = params

    json.dump(cfg, open(f"/Users/{username}/Library/Preferences/bennyontop.clipboarduploader/config.json", "w"), indent=4, sort_keys=False)

    root.after(1000, saveData)

header = tk.Label(root, text="Clipboard Uploader", font="Helvetica 25 bold")
header.grid(row=0, column=0, columnspan=3, pady=(10, 20))

requestUrlLabel = tk.Label(root, text="Request url:")
requestUrlEntry = tk.Entry(root)
requestUrlEntry.insert(0, config.get_request()["url"])

requestUrlLabel.grid(row=2, column=0, sticky="w", padx=(10, 0))
requestUrlEntry.grid(row=2, column=1, columnspan=2, sticky="we", padx=(0, 10))

requestMethodLabel = tk.Label(root, text="Request method:")
requestMethodEntry = tk.Entry(root)
requestMethodEntry.insert(0, config.get_request()["method"])

requestMethodLabel.grid(row=3, column=0, sticky="w", padx=(10, 0))
requestMethodEntry.grid(row=3, column=1, columnspan=2, sticky="we", padx=(0, 10))

fileFieldnameLabel = tk.Label(root, text="File field name:")
fileFieldnameEntry = tk.Entry(root)
fileFieldnameEntry.insert(0, config.get_file_fieldname())

fileFieldnameLabel.grid(row=4, column=0, sticky="w", padx=(10, 0))
fileFieldnameEntry.grid(row=4, column=1, columnspan=2, sticky="we", padx=(0, 10))

tk.Label(root, text="Parameters", font="Helvetica 16 bold").grid(row=5, column=0, columnspan=3, sticky="w", pady=(10, 0), padx=(10, 0))

paramsAddNewButton = tk.Button(root, text="+", command=addNewParam, width=1)
paramsAddNewButton.grid(row=5, column=2, sticky="e", pady=(10, 0), padx=(0, 10))

for param in params:
    if param not in addedParams:
        index += 1

        label = tk.Label(root, text=param + ":")
        entry = tk.Entry(root)
        entry.insert(0, params[param])

        deleteBtn = tk.Button(root, text="x", command=lambda: deleteParam(param), width=1)
        
        deleteBtn.grid(row=index+5, column=2, sticky="e", padx=(0, 10))
        label.grid(row=index+5, column=0, sticky="w", padx=(10, 0))
        entry.grid(row=index+5, column=1, sticky="w", padx=(0, 0))

        addedParams.append([param, label, entry, deleteBtn])

tk.Label(root, text="").grid(row=99, column=0, columnspan=3, sticky="w", pady=(0, 10))

root.after(1, lambda: Clipboard().clear())
root.after(1, checkClipboard)
root.after(1000, saveData)
root.title("Clipboard Uploader")
root.mainloop()
