import tkinter as tk
import pyautogui
import PIL
import os

from contextlib import suppress
from notifier import Notifier
from clipboard import Clipboard
from uploader import Uploader

notifier = Notifier()
uploader = Uploader()

def uploadscreenshot():
    clipboard = Clipboard()
    screenshotData = open('croppedScreenshot.png', 'rb').read()
    response = uploader.upload(screenshotData)

    if response:
        notifier.send("ScreenZap", "URL copied to clipboard")
        clipboard.set_text(response)
    else:
        notifier.send("ScreenZap", "Something went wrong")

    try:
        os.remove('croppedScreenshot.png')
        os.remove("screenshot.png")
    except:
        pass

    exit()

def cropscreenshot(x, y, w, h):
    y += 30
    screenshot = PIL.Image.open('screenshot.png')
    croppedScreenshot = screenshot.crop((x, y, x + w, y + h))
    croppedScreenshot.save('croppedScreenshot.png')

def takescreenshot():
    myScreenshot = pyautogui.screenshot()
    screenWidth, screenHeight = pyautogui.size()
    myScreenshot.thumbnail((screenWidth, screenHeight))
    myScreenshot.save('screenshot.png')
    
def close(event):
    with suppress(Exception): os.remove('croppedScreenshot.png')
    with suppress(Exception): os.remove("screenshot.png")

    exit()

class GrabWindow:
    def __init__(self, master):
        self.root = tk.Toplevel(master)
        self.root.title('Screenshot Grabber')
        self.root.attributes('-alpha', 0.25)
        self.root.attributes('-topmost', True)
        self.root.bind("<Return>", self.on_enter)
        self.root.bind("<Escape>", close)

        self.root.mainloop()

    def on_enter(self, event):
        width = event.widget.winfo_width()
        height = event.widget.winfo_height()
        x = event.widget.winfo_x()
        y = event.widget.winfo_y()

        cropscreenshot(x, y, width, height)
        uploadscreenshot()

class MainWindow:
    def __init__(self):
        takescreenshot()
        self.root = tk.Tk()
        self.screenshot = tk.PhotoImage(file='screenshot.png')

        self.root.attributes("-fullscreen", True)
        self.root.configure(background='black')

        self.label = tk.Label(self.root, image=self.screenshot)
        self.label.pack()

        self.root.bind('<Escape>', close)
        self.root.after(0, GrabWindow(self.root))

        self.root.mainloop()

def run():
    MainWindow()

if __name__ == '__main__':
    run()
