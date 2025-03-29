# ----- IMPORT LIST START -----
import random
# ----- IMPORT LIST END -----

# ----- MAP SYSTEM START -----
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
# ----- MAP SYSTEM END -----

# ----- CHARACTER SYSTEM START -----
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
# ----- CHARACTER SYSTEM END -----

# ----- WEAPON SYSTEM START -----
class Weapon:
    def __init__(self, name, weight, base_damage, rarity_mod, scaling, zone):
        self.name = name
        self.weight = weight
        self.base_damage = base_damage
        self.rarity_mod = rarity_mod
 # 'scaling' is a dictionary {"strength": 1.5, "dexterity": 0.5}
        self.scaling = scaling
# zone is an action list
        self.zone = zone
    def calculate_damage(self, character):
        scaling_damage = 0
        for attribute, factor in self.scaling.items():
            attribute_value = getattr(character, attribute, 0)
            scaling_damage += attribute_value * factor
        total_damage = (self.base_damage + scaling_damage) * self.rarity_mod
        return total_damage
## MAIN WEAPON CLASSES
class MeleeWeapon(Weapon):
    def __init__(self, name, weight, base_damage, rarity_mod, scaling, zone):
        super().__init__(name, weight, base_damage, rarity_mod, scaling, zone)
class RangedWeapon(Weapon):
    def __init__(self, name, weight, base_damage, rarity_mod, scaling, zone):
        super().__init__(name, weight, base_damage, rarity_mod, scaling, zone)

## 1ST LEVEL SUBCLASSES
class OneHandedMelee(MeleeWeapon):
    def __init__(self, name, weight, base_damage, rarity_mod, scaling, zone):
        super().__init__(name, weight, base_damage, rarity_mod, scaling, zone)
class TwoHandedMelee(MeleeWeapon):
    def __init__(self, name, weight, base_damage, rarity_mod, scaling, zone):
        super().__init__(name, weight, base_damage, rarity_mod, scaling, zone)

## 2ND LEVEL SUBCLASSES
class Dagger(OneHandedMelee):
    def __init__(self, name, weight, base_damage, rarity_mod, scaling, zone):
        super().__init__(name, weight, base_damage, rarity_mod, scaling, zone)
    def get_base_damage(self):
        return self.base_damage
    def get_rarity(self):
        return self.rarity_mod

class ShortSword(OneHandedMelee):
    def __init__(self, name, weight, base_damage, rarity_mod, scaling, zone):
        super().__init__(name, weight, base_damage, rarity_mod, scaling, zone)

class Sword(OneHandedMelee):
    def __init__(self, name, weight, base_damage, rarity_mod, scaling, zone):
        super().__init__(name, weight, base_damage, rarity_mod, scaling, zone)

class Axe(OneHandedMelee):
    def __init__(self, name, weight, base_damage, rarity_mod, scaling, zone):
        super().__init__(name, weight, base_damage, rarity_mod, scaling, zone)

class MediumSword(OneHandedMelee):
    def __init__(self, name, weight, base_damage, rarity_mod, scaling, zone):
        super().__init__(name, weight, base_damage, rarity_mod, scaling, zone)

class LongSword(TwoHandedMelee):
    def __init__(self, name, weight, base_damage, rarity_mod, scaling, zone):
        super().__init__(name, weight, base_damage, rarity_mod, scaling, zone)

class BattleAxe(TwoHandedMelee):
    def __init__(self, name, weight, base_damage, rarity_mod, scaling, zone):
        super().__init__(name, weight, base_damage, rarity_mod, scaling, zone)

class WarHammer(TwoHandedMelee):
    def __init__(self, name, weight, base_damage, rarity_mod, scaling, zone):
        super().__init__(name, weight, base_damage, rarity_mod, scaling, zone)

class ShortBow(RangedWeapon):
    def __init__(self, name, weight, base_damage, rarity_mod, scaling, zone):
        super().__init__(name, weight, base_damage, rarity_mod, scaling, zone)

class LongBow(RangedWeapon):
    def __init__(self, name, weight, base_damage, rarity_mod, scaling, zone):
        super().__init__(name, weight, base_damage, rarity_mod, scaling, zone)

class CrossBow(RangedWeapon):
    def __init__(self, name, weight, base_damage, rarity_mod, scaling, zone):
        super().__init__(name, weight, base_damage, rarity_mod, scaling, zone)

##zone try
dagger_zone = {}
##weapon creation
bronze_dagger = Dagger(name="Bronze Dagger", weight=2, base_damage=8, rarity_mod=1.0, scaling={"dexterity": 1.0}, zone=None)
bronze_straight_sword = MediumSword(name="Bronze Straight Sword", weight=4, base_damage=12, rarity_mod=1.0, scaling={"dexterity": 0.4, "strength": 0.6}, zone=None)
zone_test = Dagger(name="Zone", weight=2, base_damage=10, rarity_mod=1.0, scaling={"dexterity": 1.0}, zone=dagger_zone)
print(f"Dagger {bronze_dagger.name}'s damage: {bronze_dagger.get_base_damage()} rarity: {bronze_dagger.get_rarity()}")
# ----- WEAPON SYSTEM END -----

# ----- ARMOR SYSTEM START -----
class Armor:
    def __init__(self, name, weight, armor_type, armor_class, base_defense,
        rarity_mod, attribute_bonuses):
            self.name = name
            self.weight = weight
            self.armor_type = armor_type
            self.armor_class = armor_class
            self.base_defense = base_defense
            self.rarity_mod = rarity_mod
            self.attribute_bonuses = attribute_bonuses

class LightArmor(Armor):
    def __init__(self, name, weight, armor_type, armor_class, base_defense, rarity_mod, attribute_bonuses):
        super().__init__(name, weight, armor_type, armor_class, base_defense, rarity_mod, attribute_bonuses)

leather_helm = Armor(name="Leather Helm", weight=2, armor_type="head", armor_class="light", base_defense=3, rarity_mod=1.0, attribute_bonuses=None)
leather_cuirass = Armor(name="Leather Cuirass", weight=3, armor_type="chest", armor_class="light", base_defense=5, rarity_mod=1.0, attribute_bonuses=None)
leather_boots = Armor(name="Leather Boots", weight=1, armor_type="feet", armor_class="light", base_defense=2, rarity_mod=1.0, attribute_bonuses=None)
leather_leggings= Armor(name="Leather Leggings", weight=2, armor_type="legs", armor_class="light", base_defense=3, rarity_mod=1.0, attribute_bonuses=None)
leather_vambraces = Armor(name="Leather Vambraces", weight=2, armor_type="arms", armor_class="light", base_defense=3, rarity_mod=1.0, attribute_bonuses=None)
leather_belt = Armor(name="Leather Belt", weight=1, armor_type="waist", armor_class="light", base_defense=3, rarity_mod=1.0, attribute_bonuses=None)
#equip tests
Character.equip_armor(gandalf, leather_helm)
Character.equip_armor(gandalf, leather_cuirass)
Character.equip_armor(gandalf, leather_leggings)
# Print out stats for each class
print(f"Warrior {aragorn.name}'s attack: {aragorn.get_attack()} "
      f"defense: {aragorn.get_defense()} "
      f"armor defense: {aragorn.get_total_armor_defense()} "
      f"equipped armor: {aragorn.get_equipped_armor()}")
print(f"Mage {gandalf.name}'s attack: {gandalf.get_attack()} "
      f"defense: {gandalf.get_defense()} "
      f"armor defense: {gandalf.get_total_armor_defense()}"
      f"equipped armor: {gandalf.get_equipped_armor()}")
print(f"Rogue {zorro.name}'s attack: {zorro.get_attack()} "
      f"defense: {zorro.get_defense()} "
      f"armor defense: {zorro.get_total_armor_defense()} "
      f"equipped armor: {zorro.get_equipped_armor()}")
print(f"Brute {buffneck.name}'s attack: {buffneck.get_attack()} "
      f"defense: {buffneck.get_defense()} "
      f"armor defense: {buffneck.get_total_armor_defense()} "
      f"equipped armor: {buffneck.get_equipped_armor()}")
# ----- ARMOR SYSTEM END -----

# ----- ITEM SYSTEM START -----
class Item:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
class Consumable(Item):
    def __init__(self, name, weight, effect):
        super().__init__(name, weight)
        self.effect = effect  # This should be a callable

    def use(self, target):
        # Call the effect function on the target
        print(f"{target.name} used {self.name}!")
        self.effect(target)
        target.inventory["Consumables"][self.name] -= 1
        if target.inventory["Consumables"][self.name] == 0:
            del target.inventory["Consumables"][self.name]
class KeyItem(Item):
    def __init__(self, name, weight, effect):
        super().__init__(name, weight)
        self.effect = effect
# ----- ITEM SYSTEM END -----

# ----- EFFECT SYSTEM START -----
def minor_heal(target):
    heal_amount = int(target.maxhp / 5)
    target.hp = min(target.hp + heal_amount, 100)
    print(f"{target.name} healed for {heal_amount} HP (HP is now {target.hp}).")

def normal_heal(target):
    heal_amount = int(target.maxhp / 3)
    target.hp = min(target.hp + heal_amount, 100)
    print(f"{target.name} healed for {heal_amount} HP (HP is now {target.hp}).")

def strong_heal(target):
    heal_amount = int(target.maxhp / 2)
    target.hp = min(target.hp + heal_amount, 100)
    print(f"{target.name} healed for {heal_amount} HP (HP is now {target.hp}).")

def minor_strength(target):
    # Example: temporarily increase strength by 5 (implementation left to you)
    target.strength += 10
    print(f"{target.name}'s strength increased by 10!")
    # You might want to add logic to remove the buff later

def fire_burst(caster, target):
    damage = 10 + (caster.intelligence * 1.2)
    return damage
def void_burst(caster, target):
    damage = 10 + (caster.intelligence * 1.2) + (caster.dark * 1.2) / 2
    return damage

## status effects
class StatusEffect:
    def __init__(self, name, duration, effect_func, blocks_action=False):
        self.name = name
        self.duration = duration  # Number of turns effect lasts
        self.effect_func = effect_func  # Function applied each turn
        self.blocks_action = blocks_action  # Whether it prevents the character from acting

    def tick_effect(self, character):
        """Process the effect for this turn and decrement duration."""
        self.effect_func(character)  # Apply the effect (e.g., damage, stun message)
        self.duration -= 1  # Reduce duration after processing

    def is_expired(self):
        return self.duration <= 0

    def __str__(self):
        return f"{self.name} (Duration: {self.duration})"
# ----- EFFECT SYSTEM END -----
# Creating consumables:
weak_health_potion = Consumable(name="Weak Health Potion", weight=0.3, effect=minor_heal)
health_potion = Consumable(name="Health Potion", weight=0.3, effect=normal_heal)
potent_health_potion = Consumable(name="Potent Health Potion", weight=0.6, effect=strong_heal)
strength_elixir = Consumable(name="Strength Elixir", weight=0.5, effect=minor_strength)


consumable_objects = {
    "Weak Health Potion": weak_health_potion,
    "Health Potion": health_potion,
    "Potent Health Potion": potent_health_potion,
    "Strength Elixir": strength_elixir

}

buffneck.inventory["Consumables"][weak_health_potion.name] = 3
gandalf.inventory["Consumables"][weak_health_potion.name] = 3
gandalf.inventory["Consumables"][strength_elixir.name] = 3
gandalf.equipped_weapons["right hand"] = zone_test

#STATUS EFFECTS 
stun = StatusEffect("Stun", duration=1, effect_func=lambda char: restrict_action(char, stun), blocks_action=True)
hold = StatusEffect("Hold", duration=2, effect_func=lambda char: restrict_action(char, hold), blocks_action=True)
fear = StatusEffect("Fear", duration=3, effect_func=lambda char: restrict_action(char, fear), blocks_action=True)
poison = StatusEffect("Poison", duration=3, effect_func=lambda char: poison_damage(char, poison), blocks_action=False)

# ----- MAGIC SYSTEM START -----
class Magic:
    def __init__(self, name, magic_type,):
        self.name = name

class Divination(Magic):
    def __init__(self, name, magic_type, mp_cost, effect):
        super().__init__(name, magic_type)
        self.mp_cost = mp_cost
        self.effect = effect
class Sorcery(Magic):
    def __init__(self, name, magic_type, mp_cost, effect):
        super().__init__(name, magic_type)
        self.mp_cost = mp_cost
        self.effect = effect

class Pyromancy(Magic):
    def __init__(self, name, magic_type, mp_cost, effect):
        super().__init__(name, magic_type)
        self.mp_cost = mp_cost
        self.effect = effect

class BloodMagic(Magic):
    def __init__(self, name, magic_type, mp_cost, effect):
        super().__init__(name, magic_type)
        self.mp_cost = mp_cost
        self.effect = effect

minor_blessing = Divination(name="Minor Blessing", magic_type="Divination", mp_cost=20, effect=normal_heal)
fire_blast = Pyromancy(name="Fire Blast", magic_type="Pyromancy", mp_cost=20, effect=fire_burst)
# ----- MAGIC SYSTEM END -----

# ----- MOVEMENT SYSTEM START -----
def move_entity(entity, dx, dy, world_map):
    new_x = entity.x + dx
    new_y = entity.y + dy
    # Check if the new position is within the map bounds
    if 0 <= new_y < len(world_map) and 0 <= new_x < len(world_map[0]):
        tile = world_map[new_y][new_x]   
        if tile.passable:  # Only move if tile is not blocked
            entity.x = new_x
            entity.y = new_y
            print(f"{entity.name} moved to ({new_x}, {new_y})")
        else:
            print(f"{entity.name} can't move there! {tile.terrain} is not passable.")
    else:
        print(f"{entity.name} can't move out of bounds!")
# ----- MOVEMENT SYSTEM END -----

# ----- COMBAT SYSTEM START -----
def dagger_one(attacker, defender, weapon):
    # Perhaps quick strikes have a slight bonus to accuracy or speed but do less damage.
    messages = []
    raw_damage = weapon.calculate_damage(attacker) * 10 # 20% less damage
    roll = random.random()
    if roll < 0.9:
        fire_damage = fire_burst(attacker, defender)
        total_damage = raw_damage + fire_damage
        messages.append(f"{attacker.name} deals {fire_damage:.2f} fire damage to {defender.name}.")
    else:
        total_damage = raw_damage  # Normal damage

    multiplier = 100 / (100 + defender.get_defense())
    attacker.stamina -= 15
    return max(total_damage * multiplier, 1)

def dagger_two(attacker, defender, weapon):
    # Perhaps quick strikes have a slight bonus to accuracy or speed but do less damage.
    raw_damage = weapon.calculate_damage(attacker) * 1.0  # 20% less damage
    multiplier = 100 / (100 + defender.get_defense())
    roll = random.random()  # gives a value between 0 and 1
    if roll < 0.9:
        void_damage = void_burst(attacker, defender)
        total_damage = raw_damage + void_damage

    else:
        total_damage = raw_damage  # Nor
    attacker.stamina -= 15
    return max(total_damage * multiplier, 1)

def dagger_three(attacker, defender, weapon):
    # Perhaps quick strikes have a slight bonus to accuracy or speed but do less damage.
    raw_damage = weapon.calculate_damage(attacker) * 1.0  # 20% less damage
    multiplier = 100 / (100 + defender.get_defense())
    roll = random.random()  # gives a value between 0 and 1
    if roll < 0.9:
        defender.status_effects.append(StatusEffect("Stun", 1, lambda char: restrict_action(char, stun), blocks_action=True))
        print(f"Stun applied! {defender.name}'s status effects: {[effect.name for effect in defender.status_effects]}")
        total_damage = raw_damage

    else:
        total_damage = raw_damage  # Nor
    attacker.stamina -= 15
    return max(total_damage * multiplier, 1)
dagger_zone.update({"Dagger 1": dagger_one,"Dagger 2": dagger_two,"Dagger 3": dagger_three})

def basic_attack(attacker, defender, weapon):
      # Step 1: Compute raw damage using the weapon's calculate_damage() method.
      raw_damage = weapon.calculate_damage(attacker)

      # Step 2: Get the defender's defense.
      defense = defender.get_defense()

      # Step 3: Compute a damage multiplier.
      # This formula can be tweaked: higher defense reduces more damage.
      damage_multiplier = 100 / (100 + defense)

      # Step 4: Compute the total damage dealt.
      total_damage = raw_damage * damage_multiplier

      # Ensure damage doesn't drop below 1 (or some other minimum value)
      total_damage = max(total_damage, 1)
      attacker.stamina -= 15
      return total_damage

def quick_strike(attacker, defender, weapon):
    # Perhaps quick strikes have a slight bonus to accuracy or speed but do less damage.
    raw_damage = weapon.calculate_damage(attacker) * 0.8  # 20% less damage
    multiplier = 100 / (100 + defender.get_defense())
    attacker.stamina -= 15
    return max(raw_damage * multiplier, 1)

def heavy_attack(attacker, defender, weapon):
    # Heavy attacks do more damage but may have a penalty like reduced hit chance.
    raw_damage = weapon.calculate_damage(attacker) * 1.2  # 20% extra damage
    multiplier = 100 / (100 + defender.get_defense())
    attacker.stamina -= 20
    return max(raw_damage * multiplier, 1)

# ZONE MENU SETUP
def zone_menu(weapon):
    if not weapon.zone:
        print("This weapon has no special moves.")
        return None
    moves = list(weapon.zone.items())  # List of (move_name, move_function) tuples
    print("Special Moves:")
    for i, (move_name, _) in enumerate(moves, start=1):
        print(f"{i}. {move_name}")
    choice = input("Enter the number of the special move to use (or press Enter to cancel): ")
    if choice.strip() == "":
        return None
    try:
        index = int(choice) - 1
        if index < 0 or index >= len(moves):
            print("Invalid selection.")
            return None
        return moves[index] # Return the function for the chosen move
    except ValueError:
        print("Invalid input.")
        return None
#GENERAL EFFFECT FUNCTIONS
def restrict_action(character, effect):
    """Prevents the character from taking action for a turn."""
    print(f"{character.name} is affected by {effect.name}!")
    return False  # Indicates that the action is blocked

def poison_damage(character, effect):
    damage = 10
    character.hp -= damage
    print(f"{character.name} is affected by {effect.name} and takes damage!")


def process_status_effects(character):
    # Remove expired effects before applying new ones
    character.status_effects = [effect for effect in character.status_effects if not effect.is_expired()]

    for effect in character.status_effects[:]:  
        effect.tick_effect(character)
effect_map = {
    "Stun": "stunned",
    "Fear": "in a state of fear",
}     
# enemy combat logic
def enemy_choose_action(enemy, health):
    # Options: 'basic', 'quick', 'heavy'
    actions = ['basic', 'quick', 'heavy']
    min_hp = enemy.maxhp / 3
    if weak_health_potion.name in enemy.inventory["Consumables"] and enemy.inventory["Consumables"][weak_health_potion.name] > 0:
        if enemy.hp <= min_hp and "potion used" not in enemy.action_log:
            enemy.log_action("potion used")
            return 'heal'
        else:
            enemy.action_log = []
            return random.choice(actions)
    else:
        return random.choice(actions)
        enemy.action_log = []


def enemy_turn(enemy, player, enemy_weapon):
    messages = []
    for effect in enemy.status_effects:
        if effect.blocks_action:
            effect_name = effect_map.get(effect.name, effect.name)
            print(f"{enemy.name} is {effect_name} and cannot act!")
            return messages  # Prevent further actions

    action = enemy_choose_action(enemy, enemy.hp)
    if action == 'basic':
        damage = basic_attack(enemy, player, enemy_weapon)
        messages.append(f"{enemy.name} performs a basic attack!")
    elif action == 'quick':
        damage = quick_strike(enemy, player, enemy_weapon)
        messages.append(f"{enemy.name} performs a quick strike!")
    elif action == 'heavy':
        damage = heavy_attack(enemy, player, enemy_weapon)
        messages.append(f"{enemy.name} performs a heavy attack!")
    elif action == 'heal':
        Consumable.use(weak_health_potion, enemy)
       # messages.append(f"{enemy.name} uses a potion!")
        damage = 0

    player.hp -= damage
    if damage > 0:
        messages.append(f"{player.name} takes {damage:.2f} damage!")
    messages.append(f"{player.name} has {player.hp:.2f} HP left!")
    for message in messages:
        print(message)
    return messages

# combat loop
def combat_loop(attacker, defender, attacker_weapon, defender_weapon):
    print(f"{defender.name} has challenged {attacker.name}!")
    turn = 1
    while attacker.hp > 0 and defender.hp > 0:
        process_status_effects(attacker) 
        process_status_effects(defender) 

        if turn % 2 != 0:  # Player's turn
            main_loop = True
            while main_loop:
                messages = []
                print("Choose an action:")
                print("1. Basic Attack")
                print("2. Quick Strike")
                print("3. Heavy Slash")
                print("4. Use Item")
                print("5. Swap Weapon")
                print("6. Zone")
                choice = input("Enter your choice: ")

                if choice == "1":
                    damage = basic_attack(attacker, defender, attacker_weapon)
                    messages.append(f"{attacker.name} does a basic attack!")
                elif choice == "2":
                    damage = quick_strike(attacker, defender, attacker_weapon)
                    messages.append(f"{attacker.name} does a quick strike!")
                elif choice == "3":
                    damage = heavy_attack(attacker, defender, attacker_weapon)
                    messages.append(f"{attacker.name} does a heavy attack!")
                elif choice == "4":
                    item_used = False
                    while True:
                        consumable_names = list(attacker.inventory["Consumables"].keys())
                        if not consumable_names:
                            print("No consumables available!")
                            break

                        print("Available consumables:")
                        for i, name in enumerate(consumable_names, start=1):
                            qty = attacker.inventory["Consumables"][name]
                            print(f"{i}. {name} (Quantity: {qty})")

                        con_choice = input("Enter the number of the consumable to use: ")
                        try:
                            index = int(con_choice) - 1
                            if index < 0 or index >= len(consumable_names):
                                print("Invalid selection.")
                                continue

                            chosen_name = consumable_names[index]
                            chosen_item = consumable_objects[chosen_name] 
                            chosen_item.use(attacker)

                            damage = 0 
                            item_used = True   
                            break
                        except ValueError:
                            print("Invalid input.")
                            continue
                    if not item_used:
                        continue
                    damage = 0

                elif choice == '6':
                    move_name, move_func = zone_menu(attacker_weapon)
                    if move_func is None:
                        continue  # Cancel and re-prompt menu
                    damage = move_func(attacker, defender, attacker.equipped_weapons["right hand"]) 
                    print(f"{attacker.name} uses {move_name}!")

                defender.hp -= damage
                defender.hp = max(defender.hp, 0)

                if damage > 0:
                    messages.append(f"{attacker.name} deals {damage:.2f} damage to {defender.name}.")
                messages.append(f"{defender.name} has {defender.hp:.2f} HP left!")

                for message in messages:
                    print(message)

                main_loop = False

            # Enemy regains stamina at the end of attacker's turn (except first attack)
            if turn > 1:
                defender.stamina += round(defender.max_stamina * 0.08)

        else:  # Enemy's turn
            enemy_turn(defender, attacker, defender_weapon)

            # Attacker regains stamina at the end of enemy's turn
            attacker.stamina += round(attacker.max_stamina * 0.08)

        turn += 1

        print(f"{attacker.name} has {attacker.stamina} stamina left.")

    # End of combat
    if attacker.hp <= 0 and defender.hp <= 0:
        print("Both combatants have fallen!")
    elif attacker.hp <= 0:
        print(f"{attacker.name} has been defeated!")
    else:
        print(f"{defender.name} has been defeated!")
# ----- COMBAT SYSTEM END -----
combat_loop(gandalf, buffneck, gandalf.equipped_weapons["right hand"], bronze_dagger)