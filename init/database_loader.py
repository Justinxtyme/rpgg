import json



def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

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
    
    