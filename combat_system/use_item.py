consumable_objects = [
    "Weak Health Potion",
    "Health Potion",
    "Potent Health Potion",
    "Strength Elixir"
]

def use_consumable(character):
    consumable_names = list(character.inventory["Consumables"].keys())
    if not consumable_names:
        print("No consumables available!")
        return False

    print("Available consumables:")
    for i, name in enumerate(consumable_names, start=1):
        qty = character.inventory["Consumables"][name]
        print(f"{i}. {name} (Quantity: {qty})")

    choice = input("Enter the number of the consumable to use: ")
    try:
        index = int(choice) - 1
        if index < 0 or index >= len(consumable_names):
            print("Invalid selection.")
            return False
        chosen_name = consumable_names[index]
        chosen_item = consumable_objects[chosen_name]
        chosen_item.use(character)
        print(f"{character.name} used {chosen_name}.")
        return True
    except (ValueError, IndexError):
        print("Invalid input.")
        return False