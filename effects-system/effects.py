def minor_heal(target):
    heal_amount = int(target.maxhp / 5)
    target.hp = min(target.hp + heal_amount, 100)
    print(f"{target.name} healed for {heal_amount} HP (HP is now {target.hp}).")

def normal_heal(target):
    heal_amount = int(target.maxhp / 3)
    target.hp = min(target.hp + heal_amount, 100)
    print(f"{target.name} healed for {heal_amount} HP (HP is now {target.hp}).")

def strong_heal(target):
    heal_amount = int(target.maxhp / 2)
    target.hp = min(target.hp + heal_amount, 100)
    print(f"{target.name} healed for {heal_amount} HP (HP is now {target.hp}).")

def minor_strength(target):
    # Example: temporarily increase strength by 5 (implementation left to you)
    target.strength += 10
    print(f"{target.name}'s strength increased by 10!")
    # You might want to add logic to remove the buff later

def fire_burst(caster, target):
    damage = 10 + (caster.intelligence * 1.2)
    return damage
def void_burst(caster, target):
    damage = 10 + (caster.intelligence * 1.2) + (caster.dark * 1.2) / 2
    return damage

## status effects
class StatusEffect:
    def __init__(self, name, duration, effect_func, blocks_action=False):
        self.name = name
        self.duration = duration  # Number of turns effect lasts
        self.effect_func = effect_func  # Function applied each turn
        self.blocks_action = blocks_action  # Whether it prevents the character from acting

    def tick_effect(self, character):
        """Process the effect for this turn and decrement duration."""
        self.effect_func(character)  # Apply the effect (e.g., damage, stun message)
        self.duration -= 1  # Reduce duration after processing

    def is_expired(self):
        return self.duration <= 0

    def __str__(self):
        return f"{self.name} (Duration: {self.duration})"
#STATUS EFFECTS 
stun = StatusEffect("Stun", duration=1, effect_func=lambda char: restrict_action(char, stun), blocks_action=True)
hold = StatusEffect("Hold", duration=2, effect_func=lambda char: restrict_action(char, hold), blocks_action=True)
fear = StatusEffect("Fear", duration=3, effect_func=lambda char: restrict_action(char, fear), blocks_action=True)
poison = StatusEffect("Poison", duration=3, effect_func=lambda char: poison_damage(char, poison), blocks_action=False)