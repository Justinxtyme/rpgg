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