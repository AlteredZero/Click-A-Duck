import json
import os

SAVE_DIR = os.path.join(os.path.expanduser("~"), ".click_a_duck")
SAVE_FILE = os.path.join(SAVE_DIR, "save.json")

def save_game(data):
    os.makedirs(SAVE_DIR, exist_ok=True)

    with open(SAVE_FILE, "w") as save_file:
        json.dump(data, save_file, indent=4)

def load_game(default_data):
    if not os.path.exists(SAVE_FILE):
        save_game(default_data)
        return default_data.copy()

    try:
        with open(SAVE_FILE, "r") as save_file:
            return json.load(save_file)

    except (FileNotFoundError, json.JSONDecodeError):
        print("ERROR: Save file corrupted, resetting.")
        return default_data.copy()