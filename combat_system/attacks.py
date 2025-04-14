dagger_zone = {}
def dagger_one(attacker, defender, weapon):
    # Perhaps quick strikes have a slight bonus to accuracy or speed but do less damage.
    messages = []
    raw_damage = weapon.calculate_damage(attacker) * 10 # 20% less damage
    roll = random.random()
    if roll < 0.9:
        fire_damage = fire_burst(attacker, defender)
        total_damage = raw_damage + fire_damage
        messages.append(f"{attacker.name} deals {fire_damage:.2f} fire damage to {defender.name}.")
    else:
        total_damage = raw_damage  # Normal damage

    multiplier = 100 / (100 + defender.get_defense())
    attacker.stamina -= 15
    return max(total_damage * multiplier, 1)

def dagger_two(attacker, defender, weapon):
    # Perhaps quick strikes have a slight bonus to accuracy or speed but do less damage.
    raw_damage = weapon.calculate_damage(attacker) * 1.0  # 20% less damage
    multiplier = 100 / (100 + defender.get_defense())
    roll = random.random()  # gives a value between 0 and 1
    if roll < 0.9:
        void_damage = void_burst(attacker, defender)
        total_damage = raw_damage + void_damage

    else:
        total_damage = raw_damage  # Nor
    attacker.stamina -= 15
    return max(total_damage * multiplier, 1)

def dagger_three(attacker, defender, weapon):
    # Perhaps quick strikes have a slight bonus to accuracy or speed but do less damage.
    raw_damage = weapon.calculate_damage(attacker) * 1.0  # 20% less damage
    multiplier = 100 / (100 + defender.get_defense())
    roll = random.random()  # gives a value between 0 and 1
    if roll < 0.9:
        defender.status_effects.append(StatusEffect("Stun", 1, lambda char: restrict_action(char, stun), blocks_action=True))
        print(f"Stun applied! {defender.name}'s status effects: {[effect.name for effect in defender.status_effects]}")
        total_damage = raw_damage

    else:
        total_damage = raw_damage  # Nor
    attacker.stamina -= 15
    return max(total_damage * multiplier, 1)
dagger_zone.update({"Dagger 1": dagger_one,"Dagger 2": dagger_two,"Dagger 3": dagger_three})

def basic_attack(attacker, defender, weapon):
      # Step 1: Compute raw damage using the weapon's calculate_damage() method.
      raw_damage = weapon.calculate_damage(attacker)

      # Step 2: Get the defender's defense.
      defense = defender.get_defense()

      # Step 3: Compute a damage multiplier.
      # This formula can be tweaked: higher defense reduces more damage.
      damage_multiplier = 100 / (100 + defense)

      # Step 4: Compute the total damage dealt.
      total_damage = raw_damage * damage_multiplier

      # Ensure damage doesn't drop below 1 (or some other minimum value)
      total_damage = max(total_damage, 1)
      attacker.stamina -= 15
      return total_damage

def quick_strike(attacker, defender, weapon):
    # Perhaps quick strikes have a slight bonus to accuracy or speed but do less damage.
    raw_damage = weapon.calculate_damage(attacker) * 0.8  # 20% less damage
    multiplier = 100 / (100 + defender.get_defense())
    attacker.stamina -= 15
    return max(raw_damage * multiplier, 1)

def heavy_attack(attacker, defender, weapon):
    # Heavy attacks do more damage but may have a penalty like reduced hit chance.
    raw_damage = weapon.calculate_damage(attacker) * 1.2  # 20% extra damage
    multiplier = 100 / (100 + defender.get_defense())
    attacker.stamina -= 20
    return max(raw_damage * multiplier, 1)
    