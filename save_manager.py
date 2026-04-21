import json
import os

SAVE_DIR = os.path.join(os.path.expanduser("~"), ".click_a_duck")
SAVE_FILE = os.path.join(SAVE_DIR, "save.json")
CLOUD_FILENAME = "save.json"

def save_game(data, steam=None):
    os.makedirs(SAVE_DIR, exist_ok=True)

    json_str = json.dumps(data, indent=4)
    
    # Save locally
    with open(SAVE_FILE, "w") as save_file:
        save_file.write(json_str)

    # Save to Steam Cloud
    if steam and steam.initialized:
        steam.write_cloud_file(CLOUD_FILENAME, json_str.encode('utf-8'))

def load_game(default_data, steam=None):
    # Try Steam Cloud first
    if steam and steam.initialized:
        cloud_bytes = steam.read_cloud_file(CLOUD_FILENAME)
        if cloud_bytes:
            try:
                cloud_data = json.loads(cloud_bytes.decode('utf-8'))
                print("[Save] Loaded from Steam Cloud")
                # Also write it locally so local and cloud stay in sync
                os.makedirs(SAVE_DIR, exist_ok=True)
                with open(SAVE_FILE, "w") as f:
                    json.dump(cloud_data, f, indent=4)
                return cloud_data
            except (json.JSONDecodeError, UnicodeDecodeError):
                print("[Save] Steam Cloud save corrupted, falling back to local")

    # Fall back to local save
    if not os.path.exists(SAVE_FILE):
        save_game(default_data, steam)
        return default_data.copy()

    try:
        with open(SAVE_FILE, "r") as save_file:
            print("[Save] Loaded from local file")
            return json.load(save_file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("ERROR: Save file corrupted, resetting.")
        return default_data.copy()