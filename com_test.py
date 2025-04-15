from char_system.char import Character
from combat_system import combat

#combat testing
# Create your character instance (Gandalf) from your character module.
gandalf = Character("Gandalf", "Mage", 0, 0)
buffneck = Character("BuffNeck", "Brute", 0, 0)
bronze_dagger = Dagger(name="Bronze Dagger", weight=2, base_damage=8, rarity_mod=1.0, scaling={"dexterity": 1.0}, zone=None)
bronze_straight_sword = MediumSword(name="Bronze Straight Sword", weight=4, base_damage=12, rarity_mod=1.0, scaling={"dexterity": 0.4, "strength": 0.6}, zone=None)

combat.combat_loop(gandalf, buffneck, bronze_straight_sword, bronze_dagger)
