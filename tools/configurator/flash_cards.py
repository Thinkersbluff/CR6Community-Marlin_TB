import json
import os

def load_flash_cards(json_path=None):
    if json_path is None:
        json_path = os.path.join(os.path.dirname(__file__), 'flash_cards.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)
