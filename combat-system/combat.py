from effects import effects

dagger_zone = {}

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

# combat loop
def combat_loop(attacker, defender, attacker_weapon, defender_weapon):
    print(f"{defender.name} has challenged {attacker.name}!")
    turn = 1
    while attacker.hp > 0 and defender.hp > 0:
        process_status_effects(attacker) 
        process_status_effects(defender) 

        if turn % 2 != 0:  # Player's turn
            player_turn(attacker, defender, attacker_weapon)

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