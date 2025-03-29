class Item:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
class Consumable(Item):
    def __init__(self, name, weight, effect):
        super().__init__(name, weight)
        self.effect = effect  # This should be a callable

    def use(self, target):
        # Call the effect function on the target
        print(f"{target.name} used {self.name}!")
        self.effect(target)
        target.inventory["Consumables"][self.name] -= 1
        if target.inventory["Consumables"][self.name] == 0:
            del target.inventory["Consumables"][self.name]
class KeyItem(Item):
    def __init__(self, name, weight, effect):
        super().__init__(name, weight)
        self.effect = effect
class CraftingMaterial(Item):
    def __init__(self, name, weight):
        super().__init__(name, weight)
consumable_objects = {
    "Weak Health Potion": weak_health_potion,
    "Health Potion": health_potion,
    "Potent Health Potion": potent_health_potion,
    "Strength Elixir": strength_elixir

}