import subprocess

class Notifier:
    def __init__(self):
        self.cmd = '''
on run argv
  display notification (item 2 of argv) with title (item 1 of argv)
end run
'''

    def send(self, title, text):
        subprocess.call(['osascript', '-e', self.cmd, title, text])