from char_system.char import Character
from combat_system.combat import combat_loop
import weapons_system.weapons as ws
from combat_system.player_actions import dagger_zone
#dagger_zone.update({"Dagger 1": dagger_one,"Dagger 2": dagger_two,"Dagger 3": dagger_three})
#combat testing
# Create your character instance (Gandalf) from your character module.
gandalf = Character("Gandalf", "Mage", 0, 0)
buffneck = Character("BuffNeck", "Brute", 0, 0)
bronze_dagger = ws.Dagger(name="Bronze Dagger", weight=2, base_damage=8, rarity_mod=1.0, scaling={"dexterity": 1.0}, zone=dagger_zone)
bronze_straight_sword = ws.MediumSword(name="Bronze Straight Sword", weight=4, base_damage=12, rarity_mod=1.0, scaling={"dexterity": 0.4, "strength": 0.6}, zone=None)
gandalf.inventory["Consumables"]["Weak Health Potion"] = 3
print(gandalf.inventory["Consumables"])
combat_loop(gandalf, buffneck, bronze_dagger, bronze_straight_sword)
