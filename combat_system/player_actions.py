import magic_system.magic as magic
import combat_system.attacks as attacks
import items_system.items  # Ensure consumable logic is modular
import combat_system.use_item as use_item
from combat_system.zone import zone_menu
#from equipment import swap_weapon  # Add weapon swapping function
dagger_zone = {}
dagger_zone.update({"Dagger 1": dagger_one,"Dagger 2": dagger_two,"Dagger 3": dagger_three})

def player_turn(player, enemy, weapon):
    """Handles the player's turn and actions."""
    while True:
        print("Choose an action:")
        print("1. Basic Attack")
        print("2. Quick Strike")
        print("3. Heavy Slash")
        print("4. Use Item")
        print("5. Swap Weapon")
        print("6. Zone")
        choice = input("Enter your choice: ")
        messages = []

        if choice == "1":
            damage = attacks.basic_attack(player, enemy, weapon)
            messages.append(f"{player.name} performs a basic attack!")
        elif choice == "2":
            damage = attacks.quick_strike(player, enemy, weapon)
            messages.append(f"{player.name} performs a quick strike!")
        elif choice == "3":
            damage = attacks.heavy_attack(player, enemy, weapon)
            messages.append(f"{player.name} performs a heavy attack!")
        elif choice == "4":
            consumable_used = use_item.use_consumable(player)
            if not consumable_used:
                continue  # Retry menu if no consumables used
            damage = 0
        # work in progress for choice 5
        elif choice == "5":
            #new_weapon = swap_weapon(player)
            #if not new_weapon:
            continue  # Retry menu if no weapon selected
            #weapon = new_weapon  # Update current weapon
            damage = 0
        elif choice == "6":
            if weapon.zone == None:
                print("This weapon doesnt have zone.")
                continue
            else:
                move_name, move_func = zone_menu(weapon)
                if move_func is None:  # Check if no valid move was selected
                    print("No valid move selected.")
                    continue  # Return to menu selection
            
                damage = move_func(player, enemy, weapon)  # Execute the selected move
                messages.append(f"{player.name} uses {move_name}!")
        else:
            print("Invalid choice. Try again!")
            continue  # Re-prompt if input is invalid

        # Apply damage and update enemy's HP
        enemy.hp = max(enemy.hp - damage, 0)
        if damage > 0:
            messages.append(f"{player.name} deals {damage:.2f} damage to {enemy.name}.")
        messages.append(f"{enemy.name} has {enemy.hp:.2f} HP left!")

        # Print messages
        for message in messages:
            print(message)

        # Regenerate enemy stamina at the end of player turn
        enemy.stamina += round(enemy.max_stamina * 0.08)

        return damage