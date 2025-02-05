import json  # type: ignore
import os  # type: ignore


class MessageLoader:
    def __init__(self, file_path=None):  # type: ignore
        if file_path is None:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_path, "config", "messages.json")

        with open(file_path, "r", encoding="utf-8") as file:
            self.messages = json.load(file)

    def get(self, category, key):
        return self.messages.get(category, {}).get(key, f"{key} mesajı bulunamadı.")
