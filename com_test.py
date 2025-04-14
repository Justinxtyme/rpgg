from char_system.char import Character
from combat_system import combat
from init.database_loader import Weapons

#combat testing
# Create your character instance (Gandalf) from your character module.
gandalf = Character("Gandalf", "Mage", 0, 0)
buffneck = Character("BuffNeck", "Brute", 0, 0)

combat.combat_loop(gandalf, buffneck, 
