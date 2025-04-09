import json



def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)



def load_character_classes(file_path):
    try:
        with open(file_path, 'r') as file:
            character_classes = json.load(file)
        return character_classes
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: File {file_path} contains invalid JSON.")
        return {}
# Load databases
CHARACTERS = load_json("databases/characters.json")
WEAPONS = load_json("databases/weapons.json")
ARMOR = load_json("databases/armor.json")
ITEMS = load_json("databases/items.json")
MAGIC = load_json("databases/magic.json")
LOCATIONS = load_json("databases/locations.json")
# Make sure this runs when imported
if __name__ == "__main__":
    print("Databases loaded.")
    
    