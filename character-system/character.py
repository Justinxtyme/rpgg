class Character:
    def __init__(self, name: str, char_class, x=0, y=0):
        self.name = name
        self.char_class = char_class
        self.equipped_armor = {
        "head": None,
        "chest": None,
        "waist": None,
        "legs": None,
        "feet": None,
        "arms": None,
        "right hand": None,
        "left hand": None,
        }
        self.equipped_weapons = {
        "right hand": None,
        "left hand": None
        }
        self.action_log = []
        self.spell_list = []
        self.status_effects = []
        # Assign default attribute values based on class
        if char_class == "Warrior":
            self.strength = 15
            self.dexterity = 10
            self.endurance = 12
            self.base_speed = 8
            self.luck = 5
            self.intelligence = 10
            self.light = 10
            self.dark = 10
            self.focus = 10
            self.presence = 12
        elif char_class == "Mage":
            self.strength = 7
            self.dexterity = 10
            self.endurance = 5
            self.base_speed = 7
            self.luck = 8
            self.intelligence = 17
            self.light = 10
            self.dark = 10
            self.focus = 15
            self.presence = 8
        elif char_class == "Rogue":
            self.strength = 10
            self.dexterity = 15
            self.endurance = 10
            self.base_speed = 12
            self.luck = 10
            self.intelligence = 10
            self.light = 10
            self.dark = 10
            self.focus = 12
            self.presence = 6
        elif char_class == "Brute":
            self.strength = 20
            self.endurance = 14
            self.dexterity = 5
            self.base_speed = 4
            self.luck = 5
            self.intelligence = 3
            self.light = 10
            self.dark = 10
            self.focus = 8
            self.presence = 14
        elif char_class == "Archer":
            self.strength = 10
            self.dexterity = 12
            self.endurance = 10
            self.base_speed = 10
            self.luck = 10
            self.intelligence = 10
            self.light = 10
            self.dark = 10
            self.focus = 13
            self.presence = 10

        else:
            # Default case for unknown class
            self.strength = 10
            self.dexterity = 10
            self.endurance = 10
            self.base_speed = 10
            self.luck = 10
            self.intelligence = 10
            self.light = 10
            self.dark = 10
            self.focus = 10
            self.presence = 10

        # Set position
        self.x = x
        self.y = y
        # Set base HP (could scale with class or attributes later)
        self.basehp = 100
        self.maxhp = (self.basehp - 10) + (self.endurance * 2)
        self.hp = self.maxhp
        self.base_mp = 100
        self.mp = (self.base_mp - 10) + (self.intelligence * 2)
        self.base_stamina = 100
        self.max_stamina = self.base_stamina + self.endurance
        self.stamina = self.max_stamina

        ## carry capacity and current weight
        self.speed = self.base_speed
        self.inventory = {"Consumables": {}, "Weapons": {},
            "Armor": {},
            "Key Items": []}
        self.base_carry_limit = 100
        self.equipped_weight = 0
        self.inventory_weight = 0
        # scaling carry limit to strength
        self.carry_limit = self.base_carry_limit * (1 + self.strength * 0.05)
        # Base values for attack and defense
        self.base_attack = 1
        self.base_defense = 1
        # Scaling attack and defense based on attributes
        self.attack = (self.base_attack + self.strength * 2 +
        self.dexterity * 1)
        self.defense = (self.base_defense + self.dexterity +
        self.get_total_armor_defense() * 1 + self.strength * 1)

    def get_total_armor_defense(self):
        return sum(piece.base_defense * piece.rarity_mod for piece
        in self.equipped_armor.values() if piece)


    def update_speed(self):
        # This function adjusts speed based on encumbrance
        if self.inventory_weight > self.carry_limit:
            excess_weight = self.inventory_weight - self.carry_limit
            # Apply a penalty (1% speed reduction per 10 units of excess weight)
            speed_penalty = (excess_weight / 10) * 0.01
            self.speed = self.base_speed - (self.base_speed * speed_penalty)
        else:
            self.speed = self.base_speed
    ### eqipping/unequipping  functions

    def equip_armor(self, armor):
        armor_type = armor.armor_type
        if self.equipped_armor[armor_type] is not None:
            print(f"You already have a {armor_type} equipped. Unequip it first.")
            return
        self.equipped_armor[armor_type] = armor
        print(f"Equipped {armor.name} on {armor_type}.")

    def unequip_armor(self, armor_type):
        if self.equipped_armor[armor_type] is None:
            print(f"No armor equipped in {armor_type}.")
            return
        removed_armor = self.equipped_armor[armor_type]         
        self.equipped_armor[armor_type] = None
        self.add_to_inventory(removed_armor)
        self.equipped_weight -= removed_armor.weight
        self.inventory_weight += removed_armor.weight
        print(f"Unequipped {removed_armor.name} from {armor_type}.")

    def add_status_effect(self, effect):
        """Adds a status effect to the character."""
        self.status_effects.append(effect)
        print(f"{self.name} is now affected by {effect.name} for {effect.duration} turns!")

    #item functions
    def equip_item(self, item_weight):
        self.equipped_weight += item_weight
       # assert for weight
        assert self.equipped_weight <= self.inventory_weight, \
         f"Equipped weight ({self.equipped_weight}) exceeds inventory weight ({self.inventory_weight})!"
        self.inventory_weight -= item_weight
        self.update_speed()
    def unequip_item(self, item_weight):
        self.equipped_weight -= item_weight
        self.inventory_weight += item_weight
        self.update_speed()

    def take_item(self, item, quantity=1):
        if isinstance(item, Consumable):  # Check if the item is a Consumable
            if item.name in self.inventory["Consumables"]:
                self.inventory["Consumables"][item.name] += quantity
                self.inventory_weight += item.weight * quantity
            else:
                self.inventory["Consumables"][item.name] = quantity
                self.inventory_weight += item.weight * quantity
        elif isinstance(item, Weapon):  # Check if the item is a Weapon
            if item.name in self.inventory["Weapons"]:
                self.inventory["Weapons"][item.name] += quantity
                self.inventory_weight += item.weight * quantity
            else:
                self.inventory["Weapons"][item.name] = quantity # Assuming weapons are stored as objects in a list
                self.inventory_weight += item.weight * quantity
        elif isinstance(item, Armor):  # If it’s Armor
             if item.name in self.inventory["Armor"]:
                 self.inventory["Armor"][item.name] += quantity
                 self.inventory_weight += item.weight * quantity       
             else:
                 self.inventory["Armor"][item.name] = quantity
                 self.inventory_weight += item.weight * quantity
        else:
            print(f"Unknown item type: {item.name}")
        self.update_speed()

    def drop_item(self, item, quantity=1):
        if isinstance(item, Consumable):
            if item.name in self.inventory["Consumables"]:
                self.inventory["Consumables"][item.name] -= quantity
                if self.inventory["Consumables"][item.name] < 1:
                    del self.inventory["Consumables"][item.name]
                self.inventory_weight -= item.weight * quantity       

            else:
                return ("you dont have this item, wtf")               
        elif isinstance(item, Weapon):  # Check if the item is a Weapon
            if item.name in self.inventory["Weapons"]:
                self.inventory["Weapons"][item.name] -= quantity
                if self.inventory["Weapons"][item.name] < 1:
                    del self.inventory["Consumables"][item.name]
                self.inventory_weight -= item.weight * quantity     

            else:
                return ("you dont have this item, wtf")
        elif isinstance(item, Armor):  # If it’s Armor
            if item.name in self.inventory["Armor"]:
                self.inventory["Armor"][item.name] -= quantity
                if self.inventory["Armor"][item.name] < 1:
                    del self.inventory["Armor"][item.name]
                self.inventory_weight -= item.weight * quantity

            else:
                return ("you dont have this item, wtf")

        elif isinstance(item, KeyItem):
            return (f"{item.name} can not be dropped!")       

        else:
            return (f"Unknown item type: {item.name}")       
        self.updatespeed()






    def drop_stack(self, item, drop_quantity):
           ##assert for positive
        assert drop_quantity > 0, f"drop_quantity must be positive, got {drop_quantity}"
        assert item.quantity >= drop_quantity, \
               f"Tried to drop {drop_quantity} but only {item.quantity} available!"
        if item.weight == 0:
            return
        item.quantity -= drop_quantity

    def log_action(self, action):
        self.action_log.append(action)

    def reset_action_log(self):
        # Reset the action log after certain number of turns or conditions
        self.action_log = []


    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense


    def get_equipped_armor(self):
        return {slot: armor.name if armor else "None" for slot, armor in self.equipped_armor.items()}

    def get_position(self):
        print((self.x, self.y))
        return (self.x, self.y)


# Example of creating different character classes
aragorn = Character(name="Aragorn", char_class="Warrior", x=0, y=0)
gandalf = Character(name="Gandalf", char_class="Mage", x=0, y=0)
zorro = Character(name="Zorro", char_class="Rogue", x=0, y=0)
buffneck = Character(name="Buff Neck", char_class="Brute", x=0, y=0)