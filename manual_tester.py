import requests
import json


class Generator:
    def __init__(self, uid, password, link):
        self.id = uid
        self.password = password
        self.link = link

    def generate_id(self):
        request_json = json.dumps({'userid': self.id, 'pass': self.password})
        image_request = requests.post(self.link, request_json)
        print(image_request.status_code)


new_generator = Generator("k1517600", "ktJN6475!", "http://b9ce2d99f04a.ngrok.io/GenerateID")
new_generator.generate_id()
