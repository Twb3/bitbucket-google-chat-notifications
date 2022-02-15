import requests
from json import dumps
import logging


logger = logging.getLogger("bbgc")


class Api:

    version = "v1"
    base_url = "https://chat.googleapis.com"

    def __init__(self, space: str, key: str, token: str) -> None:
        self.space = space
        self.key = key
        self.token = token
        self.url = self.__form_url()

    def __form_url(self) -> str:
        return self.base_url + "/" + self.version + "/spaces/" + \
            self.space + "/messages?key=" + self.key + "&token=" + self.token

    def send_message(self, message: dict) -> requests.models.Response:
        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
        request = requests.post(
            self.url,
            data=dumps(message),
            headers=message_headers)
        return request


class MessageCreator:

    message_header = {
        "title": "Bitbucket",
        "imageUrl": "https://pbs.twimg.com/profile_images/1026981625291190272/35O2KIRX_400x400.jpg"
    }

    def __init__(self) -> None:
        self.message = dict()
        self.cards = list()
        self.sections = list()
        self.widgets = list()

    def add_text_paragraph_widget(self, text: str) -> None:
        text_paragraph_widget = {
            "textParagraph": {
                "text": text
            }
        }
        self.widgets.append(text_paragraph_widget)

    def add_text_button_widget(self, button_text: str, button_url: str) -> None:
        text_button_widget = {
            "buttons": [
                {
                    "textButton": {
                        "text": button_text,
                        "onClick": {
                            "openLink": {
                                "url": button_url
                            }
                        }
                    }
                }
            ]
        }
        self.widgets.append(text_button_widget)

    def create_message(self) -> dict:
        self.sections.append({'widgets': self.widgets})
        self.cards.append({'sections': self.sections})
        self.message['cards'] = self.cards
        self.cards[0]['header'] = self.message_header
        return self.message
