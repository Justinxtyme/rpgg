from init.database_loader import ARMOR
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


#equip tests
Character.equip_armor(gandalf, leather_helm)
Character.equip_armor(gandalf, leather_cuirass)
Character.equip_armor(gandalf, leather_leggings)
# Print out stats for each class
print(f"Warrior {aragorn.name}'s attack: {aragorn.get_attack()} "
      f"defense: {aragorn.get_defense()} "
      f"armor defense: {aragorn.get_total_armor_defense()} "
      f"equipped armor: {aragorn.get_equipped_armor()}")
print(f"Mage {gandalf.name}'s attack: {gandalf.get_attack()} "
      f"defense: {gandalf.get_defense()} "
      f"armor defense: {gandalf.get_total_armor_defense()}"
      f"equipped armor: {gandalf.get_equipped_armor()}")
print(f"Rogue {zorro.name}'s attack: {zorro.get_attack()} "
      f"defense: {zorro.get_defense()} "
      f"armor defense: {zorro.get_total_armor_defense()} "
      f"equipped armor: {zorro.get_equipped_armor()}")
print(f"Brute {buffneck.name}'s attack: {buffneck.get_attack()} "
      f"defense: {buffneck.get_defense()} "
      f"armor defense: {buffneck.get_total_armor_defense()} "
      f"equipped armor: {buffneck.get_equipped_armor()}")

