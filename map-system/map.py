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
        for row in location_data["world_map"]
    ]

    return world
# Uncomment this when ready to use a file-based map 
# world_map = load_map("map.txt") 