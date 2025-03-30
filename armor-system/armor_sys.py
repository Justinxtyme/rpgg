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

leather_helm = Armor(name="Leather Helm", weight=2, armor_type="head", armor_class="light", base_defense=3, rarity_mod=1.0, attribute_bonuses=None)
leather_cuirass = Armor(name="Leather Cuirass", weight=3, armor_type="chest", armor_class="light", base_defense=5, rarity_mod=1.0, attribute_bonuses=None)
leather_boots = Armor(name="Leather Boots", weight=1, armor_type="feet", armor_class="light", base_defense=2, rarity_mod=1.0, attribute_bonuses=None)
leather_leggings= Armor(name="Leather Leggings", weight=2, armor_type="legs", armor_class="light", base_defense=3, rarity_mod=1.0, attribute_bonuses=None)
leather_vambraces = Armor(name="Leather Vambraces", weight=2, armor_type="arms", armor_class="light", base_defense=3, rarity_mod=1.0, attribute_bonuses=None)
leather_belt = Armor(name="Leather Belt", weight=1, armor_type="waist", armor_class="light", base_defense=3, rarity_mod=1.0, attribute_bonuses=None)
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

