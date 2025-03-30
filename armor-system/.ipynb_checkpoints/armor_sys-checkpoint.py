class Armor:
    def __init__(self, name, weight, armor_type, armor_class, base_defense,
        rarity_mod, attribute_bonuses):
            self.name = name
            self.weight = weight
            self.armor_type = armor_type
            self.armor_class = armor_class
            self.base_defense = base_defense
            self.rarity_mod = rarity_mod
            self.attribute_bonuses = attribute_bonuses

class LightArmor(Armor):
    def __init__(self, name, weight, armor_type, armor_class, base_defense, rarity_mod, attribute_bonuses):
        super().__init__(name, weight, armor_type, armor_class, base_defense, rarity_mod, attribute_bonuses)

