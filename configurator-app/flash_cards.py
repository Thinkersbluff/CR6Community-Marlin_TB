# Flash Card Data Structure for Marlin Configurator Help Tab
# Each flash card is a dictionary with fields. Empty fields are omitted from display.
# Flash Card Data Structure for Marlin Configurator Help Tab
# Loads flash cards from flash_cards.json. Empty fields are omitted from display.
import json
import os

FLASH_CARDS_PATH = os.path.join(os.path.dirname(__file__), 'flash_cards.json')

def load_flash_cards():
    with open(FLASH_CARDS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

FLASH_CARDS = load_flash_cards()

# Template for developers to add new flash cards
FLASH_CARD_TEMPLATE = {
    "id": "unique_id",
    "objective": "User objective (title)",
    "description": "Short description of what/why",
    "keywords": ["KEYWORD1", "KEYWORD2"],
    "instructions": ["Step 1", "Step 2"],
    "related_settings": ["SETTING1", "SETTING2"],
    "docs_link": "https://marlinfw.org/docs/...",
    "warnings": "Any cautions or hardware notes"
}

def get_flash_card(card_id):
    for card in FLASH_CARDS:
        if card["id"] == card_id:
            return card
    return None
