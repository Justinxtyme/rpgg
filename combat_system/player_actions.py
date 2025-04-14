import magic_system.magic
import combat_system.attacks
import items_system.items  # Ensure consumable logic is modular
from combat_system.combat import zone_menu
#from equipment import swap_weapon  # Add weapon swapping function

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
            damage = basic_attack(player, enemy, weapon)
            messages.append(f"{player.name} performs a basic attack!")
        elif choice == "2":
            damage = quick_strike(player, enemy, weapon)
            messages.append(f"{player.name} performs a quick strike!")
        elif choice == "3":
            damage = heavy_attack(player, enemy, weapon)
            messages.append(f"{player.name} performs a heavy attack!")
        elif choice == "4":
            consumable_used = use_consumable(player)
            if not consumable_used:
                continue  # Retry menu if no consumables used
            damage = 0
        elif choice == "5":
            new_weapon = swap_weapon(player)
            if not new_weapon:
                continue  # Retry menu if no weapon selected
            weapon = new_weapon  # Update current weapon
            damage = 0
        elif choice == "6":
            move_name, move_func = zone_menu(weapon)
            if not move_func:
                continue  # Retry menu if no move selected
            damage = move_func(player, enemy, weapon)
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