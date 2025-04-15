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