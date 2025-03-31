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
# Creating consumables:
weak_health_potion = Consumable(name="Weak Health Potion", weight=0.3, effect=minor_heal)
health_potion = Consumable(name="Health Potion", weight=0.3, effect=normal_heal)
potent_health_potion = Consumable(name="Potent Health Potion", weight=0.6, effect=strong_heal)
strength_elixir = Consumable(name="Strength Elixir", weight=0.5, effect=minor_strength)
consumable_objects = {
    "Weak Health Potion": weak_health_potion,
    "Health Potion": health_potion,
    "Potent Health Potion": potent_health_potion,
    "Strength Elixir": strength_elixir

}