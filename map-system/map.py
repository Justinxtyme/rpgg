class Tile:
    def __init__(self, terrain, passable=True):
        self.terrain = terrain
        self.passable = passable

    def __str__(self):
        return self.terrain
"""For String Map"""
map_data = """ 
GGGGGGGGGG
GGGGGGGGGG
GGGGGGGGGG
GGGGGGGGGG
GGGGGGGGGG
""" 
def load_location(file_path, location_name):
    with open(file_path, "r") as file:
        locations_data = json.load(file)
    
    if location_name not in locations_data["locations"]:
        raise ValueError(f"Location '{location_name}' not found!")

    location_data = locations_data["locations"][location_name]
    terrain_mapping = location_data["terrain_mapping"]

    world = [
        [Tile(**terrain_mapping[char]) for char in row]
        for row in location_data["area_map"]
    ]

    return world
# Load specific locations
town_one_map = load_location("databases/locations.json", "town_one")
town_two_map = load_location("databases/locations.json", "town_two")

# Print the terrain of a tile in town_one
print(town_one_map[1][1].terrain)  # Output: "forest"