import requests
import utils

class Uploader:
    def __init__(self):
        pass
    
    def upload(self, file_bytes):
        self.config = utils.Config()
        self.file_fieldname = self.config.get_file_fieldname()
        self.request = self.config.get_request()
        self.params = self.config.get_params()

        response = requests.request(
            self.request["method"].upper(),
            self.request["url"],
            data=self.params,
            files=[(self.file_fieldname, ("image.png", file_bytes, "image/png"))],
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 RuxitSynthetic/1.0 v5415322336337471423 t4721495622219173133 ath1fb31b7a altpriv cvcv=2 smf=0"
            }
        )

        return response.json()
