class Character:
    def __init__(self, name: str, char_class: str, x=0, y=0):
        # Load character type attributes
        character_classes = load_character_classes("databases/character_classes.json")

        if char_class not in character_classes:
            raise ValueError(f"Unknown character class: {char_class}")

        char_attributes = character_types[char_class]

        # Basic initialization
        self.name = name
        self.char_class = char_class
        self.x = x
        self.y = y

        # Assign attributes dynamically
        for attr, value in char_attributes.items():
            setattr(self, attr, value)

        # Additional attributes
        self.equipped_armor = {
            "head": None, "chest": None, "waist": None,
            "legs": None, "feet": None, "arms": None,
            "right hand": None, "left hand": None
        }
        self.equipped_weapons = {
            "right hand": None,
            "left hand": None
        }
        self.action_log = []
        self.spell_list = []
        self.status_effects = []

        # Derived attributes
        self.basehp = 100
        self.maxhp = (self.basehp - 10) + (self.endurance * 2)
        self.hp = self.maxhp
        self.base_mp = 100
        self.mp = (self.base_mp - 10) + (self.intelligence * 2)
        self.base_stamina = 100
        self.max_stamina = self.base_stamina + self.endurance
        self.stamina = self.max_stamina

        # Inventory and weight
        self.inventory = {"Consumables": {}, "Weapons": {}, "Armor": {}, "Key Items": []}
        self.base_carry_limit = 100
        self.equipped_weight = 0
        self.inventory_weight = 0
        self.carry_limit = self.base_carry_limit * (1 + self.strength * 0.05)

        # Attack and defense scaling
        self.base_attack = 1
        self.base_defense = 1
        self.attack = (self.base_attack + self.strength * 2 + self.dexterity * 1)
        self.defense = (self.base_defense + self.dexterity + self.strength + self.get_total_armor_defense())

    def get_total_armor_defense(self):
        """Calculate total defense from equipped armor."""
        # Logic for calculating armor defense (stub)
        return sum(armor["defense"] for armor in self.equipped_armor.values() if armor is not None)