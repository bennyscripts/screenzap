import requests
import urllib.parse

from config import Config

class Uploader:
    def __init__(self):
        pass
    
    def upload(self, file_bytes):
        self.config = Config()
        self.file_fieldname = self.config.get_file_fieldname()
        self.request = self.config.get_request()
        self.params = self.config.get_params()
        self.urlArgs = urllib.parse.urlencode(self.params)
        self.userAgent = "ShareX/13.6.1"

        if self.request["body_type"].lower() == "binary":
            response = requests.request(
                self.request["method"].upper(),
                self.request["url"] + "?" + self.urlArgs,
                data=file_bytes,
                headers={"User-Agent": self.userAgent, "Content-Type": "image/png"}
            )
        elif self.request["body_type"].lower() == "form data":
            response = requests.request(
                self.request["method"].upper(),
                self.request["url"],
                data=self.params,
                files=[(self.file_fieldname, ("image.png", file_bytes, "image/png"))],
                headers={"User-Agent": self.userAgent}
            )

        if str(response.status_code)[0] == "2":
            if self.config.get_response()["method"].upper() == "JSON":
                return response.json()[self.config.get_response()["json"]]
            else:
                return response.text
        return False