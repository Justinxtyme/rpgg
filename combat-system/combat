dagger_zone = {}
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