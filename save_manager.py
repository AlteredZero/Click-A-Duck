import json
import os

save_file_dir = "data/save.json"

def save_game(data):
    os.makedirs("data", exist_ok=True)
    with open(save_file_dir, "w") as save_file:
        json.dump(data, save_file, indent=4)

def load_game(default_data):
    if not os.path.exists(save_file_dir):
        save_game(default_data)
        return default_data.copy()
    try:
        with open(save_file_dir) as save_file:
            loaded_data = json.load(save_file)
            return loaded_data
    except (FileNotFoundError, json.JSONDecodeError):
        print("ERROR: Data File Not Found, using default data.")
        return default_data.copy()