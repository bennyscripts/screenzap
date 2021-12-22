import tkinter as tk
import json
import os
import time
import getpass
import PIL
import pyautogui
import asyncio
import sys
import subprocess

from pynput import keyboard

from utils import Config
from utils import Clipboard
from utils import Notifier

def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")

  return os.path.join(base_path, relative_path)

notifier = Notifier()
uploadlog = []

index = 0
config = Config()
params = config.get_params()
addedParams = []
responseMethods = ["JSON", "Plain text"]
requestBodyTypeList = ["Form Data", "Binary"]

COMBINATIONS = [
    {keyboard.Key.cmd, keyboard.Key.shift, keyboard.KeyCode(char='9')}
]
current = set()
keyboardController = keyboard.Controller()
hotKeyPressed = False

root = tk.Tk()
root.grid_columnconfigure(0, weight=1)
root.resizable(False, False)

def execute_hotkey():
    python_path = "/opt/homebrew/bin/python3"
    try:
        if os.path.exists("utils/"):
            command = python_path + " " + resource_path("utils/screenshotter.py")
        else:
            command = python_path + " " + resource_path("screenshotter.py")
        print(command)
        subprocess.Popen(command, shell=True)     
    except Exception as e:
        notifier.send("ScreenZap", str(e))

def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute_hotkey()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener: 

    def centerWindow(window):
        window.update_idletasks()
        w = window.winfo_screenwidth()
        h = window.winfo_screenheight()
        size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        window.geometry("%dx%d+%d+%d" % (size + (x, y)))

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
            
            deleteBtn.grid(row=index+50, column=2, sticky="we", padx=(0, 10))
            label.grid(row=index+50, column=0, sticky="w", padx=(10, 0))
            entry.grid(row=index+50, column=1, sticky="w", padx=(0, 0))

            addedParams.append([key, label, entry, deleteBtn])

            newWindow.destroy() 

        if len(addedParams) >= 10:
            notifier.send("ScreenZap", "You can only add 10 parameters")
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
        requestBodyType = requestBodyTypeStringVar.get()
        responseMethod = responseMethodStringVar.get()
        responseMethodJson = responseMethodJsonEntry.get()

        for param in addedParams:
            params[param[0]] = param[2].get()

        cfg["file_fieldname"] = fileFieldName
        cfg["request"]["method"] = requestMethod
        cfg["request"]["url"] = requestUrl
        cfg["request"]["body_type"] = requestBodyType
        cfg["params"] = params
        cfg["response"]["method"] = responseMethod
        cfg["response"]["json"] = responseMethodJson

        json.dump(cfg, open(f"/Users/{username}/Library/Preferences/bennyontop.clipboarduploader/config.json", "w"), indent=4, sort_keys=False)

        root.after(1000, saveData)

    def testUpload():
        notifier.send("ScreenZap", "Test upload is disabled.")
        # imageData = open(resource_path("testimage.jpeg"), "rb").read()
        # response = uploader.upload(imageData)

        # if response:
        #     notifier.send("ScreenZap", "Test upload successful")

        #     newWindow = tk.Toplevel(root)
        #     newWindow.title("Test upload")
        #     newWindow.resizable(False, False)
        #     newWindow.grid_columnconfigure(0, weight=1)

        #     text = tk.Text(newWindow)
        #     text.grid(row=1, column=0, columnspan=3, sticky="w")
        #     text.insert(tk.END, json.dumps(response, indent=4, sort_keys=False))

        #     newWindow.mainloop()

        # else:
        #     notifier.send("ScreenZap", "Test upload failed")

    def checkResponseMethod():
        responseMethod = responseMethodStringVar.get()

        if responseMethod == "JSON":
            responseMethodJsonLabel.grid(row=8, column=0, sticky="w", padx=(10, 0))
            responseMethodJsonEntry.grid(row=8, column=1, columnspan=2, sticky="we", padx=(0, 10))
        else:
            responseMethodJsonLabel.grid_remove()
            responseMethodJsonEntry.grid_remove()

        root.after(1, checkResponseMethod)

    def checkRequestBodyType():
        requestBodyType = requestBodyTypeStringVar.get()

        if requestBodyType.lower() == "form data":
            fileFieldnameLabel.grid(row=4, column=0, sticky="w", padx=(10, 0))
            fileFieldnameEntry.grid(row=4, column=1, columnspan=2, sticky="we", padx=(0, 10))
        else:
            fileFieldnameLabel.grid_remove()
            fileFieldnameEntry.grid_remove()

        root.after(1, checkRequestBodyType)

    # header = tk.Label(root, text="ScreenZap", font="Helvetica 25 bold")
    # header.grid(row=0, column=0, columnspan=3, pady=(10, 20))

    tk.Label(root, text="Request", font="Helvetica 16 bold").grid(row=0, column=0, columnspan=3, sticky="w", pady=(10, 0), padx=(10, 0))

    testButton = tk.Button(root, text="Test Upload", command=testUpload)
    testButton.grid(row=0, column=1, sticky="e", padx=(0, 10), pady=(10, 0), columnspan=2)

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

    fileFieldnameLabel = tk.Label(root, text="File form name:")
    fileFieldnameEntry = tk.Entry(root)
    fileFieldnameEntry.insert(0, config.get_file_fieldname())

    requestBodyTypeLabel = tk.Label(root, text="Body type:")

    requestBodyTypeStringVar = tk.StringVar(root)
    requestBodyTypeStringVar.set(config.get_request()["body_type"])
    requestBodyTypeOptionMenu = tk.OptionMenu(root, requestBodyTypeStringVar, *requestBodyTypeList)

    requestBodyTypeLabel.grid(row=5, column=0, sticky="w", padx=(10, 0))
    requestBodyTypeOptionMenu.grid(row=5, column=1, columnspan=2, sticky="we", padx=(0, 10))

    tk.Label(root, text="Response", font="Helvetica 16 bold").grid(row=6, column=0, columnspan=3, sticky="w", pady=(10, 0), padx=(10, 0))

    responseMethodStringVar = tk.StringVar(root)
    responseMethodStringVar.set(config.get_response()["method"]) # default value

    responseMethodLabel = tk.Label(root, text="Response method:")
    responseMethodOptionMenu = tk.OptionMenu(root, responseMethodStringVar, *responseMethods)

    responseMethodLabel.grid(row=7, column=0, sticky="w", padx=(10, 0))
    responseMethodOptionMenu.grid(row=7, column=1, columnspan=2, sticky="we", padx=(0, 10))

    responseMethodJsonLabel = tk.Label(root, text="JSON key to copy:")
    responseMethodJsonEntry = tk.Entry(root)
    responseMethodJsonEntry.insert(0, config.get_response()["json"])

    tk.Label(root, text="Parameters", font="Helvetica 16 bold").grid(row=50, column=0, columnspan=3, sticky="w", pady=(10, 0), padx=(10, 0))

    paramsAddNewButton = tk.Button(root, text="+", command=addNewParam, width=1)
    paramsAddNewButton.grid(row=50, column=2, sticky="we", pady=(10, 0), padx=(0, 10))

    for param in params:
        if param not in addedParams:
            index += 1

            label = tk.Label(root, text=param + ":")
            entry = tk.Entry(root)
            entry.insert(0, params[param])

            deleteBtn = tk.Button(root, text="x", command=lambda: deleteParam(param), width=1)
            
            deleteBtn.grid(row=index+50, column=2, sticky="we", padx=(0, 10))
            label.grid(row=index+50, column=0, sticky="w", padx=(10, 0))
            entry.grid(row=index+50, column=1, sticky="we", padx=(0, 0))

            addedParams.append([param, label, entry, deleteBtn])

    tk.Label(root, text="").grid(row=99, column=0, columnspan=3, sticky="w")

    def on_closing():
        sys.exit()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.after(1, checkRequestBodyType)
    root.after(1, checkResponseMethod)
    # root.after(0, centerWindow(root))
    root.after(1, lambda: Clipboard().clear())
    # root.after(1, checkClipboard)
    root.after(1000, saveData)
    root.title("ScreenZap")
    root.mainloop()
    listener.join()