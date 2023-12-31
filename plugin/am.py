import requests
import keyring

from py_youtube import Data as yt_data
from flox import Flox

KEYRING_SERVICE = "AM"
KEYRING_API_KEY_NAME = "api_key"


class AmazingMarvin(Flox):
    def __init__(self):
        super().__init__()
        self.api_key = keyring.get_password(KEYRING_SERVICE, KEYRING_API_KEY_NAME)
        if self.api_key:
            self.url = "https://serv.amazingmarvin.com/api/"
            self.headers = {"X-API-Token": self.api_key}
            self.session = requests.Session()
            self.session.headers.update(self.headers)
            self.api_key_avail = True

    def query(self, query):
        if self.api_key:
            self.add_item(
                title="Create task",
                subtitle="Create a task for inbox",
                method=self.create_task,
                parameters=[query],
                score=90
            )
            self.add_item(
                title="Create task with YT Link",
                subtitle="Create a task for inbox (Transform Information from YouTube Link)",
                method=self.create_task,
                parameters=[query, True],
                score=90
            )
            self.add_item(
                title="Remove API-Key",
                subtitle="",
                method=self.set_api_key,
                parameters=[""],
                score=0
            )
        else:
            self.add_item(
                title="Set API-Key to => {}".format(query),
                subtitle="please type your API-Key in and click enter",
                method=self.set_api_key(query),
                parameters=[query]
            )
        return

    def context_menu(self, data):
        self.add_item(
            title=data,
            subtitle=data
        )

    @staticmethod
    def set_api_key(api_key):
        keyring.set_password(KEYRING_SERVICE, KEYRING_API_KEY_NAME, api_key)

    def create_task(self, title, yt_link=False):
        if yt_link:
            new_title = ""
            for item in title.split():
                if "www.youtube.com" in item:
                    youtube_data = yt_data(item).data()
                    new_title += "'{}' ({}) @YouTube ".format(youtube_data["title"], item)
                else:
                    new_title += "{} ".format(item)
            title = new_title
        endpoint = "addTask"
        url = "{}{}".format(self.url, endpoint)
        data = {
            "title": title
        }
        res = self.session.post(url, json=data)
        self.show_msg("{} created = {}".format(title, res.status_code), "{}".format(res.text))


if __name__ == "__main__":
    amazing_marvin = AmazingMarvin()
    amazing_marvin.run()
