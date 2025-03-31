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
def load_map_from_string(map_string): 
    terrain_mapping = { 
        "G": ("grass", True), 
        "W": ("water", False), 
        "M": ("mountain", False), 
        "F": ("forest", True) 
    } 
    world = [] 
    for line in map_string.strip().split("\n"): 
        row = [Tile(*terrain_mapping[char]) for char in line.strip()] 
        world.append(row) 
    return world 
# Load the map from string 
world_map = load_map_from_string(map_data) 

"""""FOR FILE MAP"""
def load_map(file_path): 
    terrain_mapping = { 
        "G": ("grass", True), 
        "W": ("water", False), 
        "M": ("mountain", False), 
        "F": ("forest", True) 
    } 
    world = [] 
    with open(file_path, "r") as file: 
        for line in file: 
            row = [Tile(*terrain_mapping[char]) for char in line.strip()] 
            world.append(row) 
    return world 
# Uncomment this when ready to use a file-based map 
# world_map = load_map("map.txt") 