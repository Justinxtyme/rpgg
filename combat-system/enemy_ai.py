def enemy_choose_action(enemy, health):
    # Options: 'basic', 'quick', 'heavy'
    actions = ['basic', 'quick', 'heavy']
    min_hp = enemy.maxhp / 3
    if weak_health_potion.name in enemy.inventory["Consumables"] and enemy.inventory["Consumables"][weak_health_potion.name] > 0:
        if enemy.hp <= min_hp and "potion used" not in enemy.action_log:
            enemy.log_action("potion used")
            return 'heal'
        else:
            enemy.action_log = []
            return random.choice(actions)
    else:
        return random.choice(actions)
        enemy.action_log = []


def enemy_turn(enemy, player, enemy_weapon):
    messages = []
    for effect in enemy.status_effects:
        if effect.blocks_action:
            effect_name = effect_map.get(effect.name, effect.name)
            print(f"{enemy.name} is {effect_name} and cannot act!")
            return messages  # Prevent further actions

    action = enemy_choose_action(enemy, enemy.hp)
    if action == 'basic':
        damage = basic_attack(enemy, player, enemy_weapon)
        messages.append(f"{enemy.name} performs a basic attack!")
    elif action == 'quick':
        damage = quick_strike(enemy, player, enemy_weapon)
        messages.append(f"{enemy.name} performs a quick strike!")
    elif action == 'heavy':
        damage = heavy_attack(enemy, player, enemy_weapon)
        messages.append(f"{enemy.name} performs a heavy attack!")
    elif action == 'heal':
        Consumable.use(weak_health_potion, enemy)
       # messages.append(f"{enemy.name} uses a potion!")
        damage = 0

    player.hp -= damage
    if damage > 0:
        messages.append(f"{player.name} takes {damage:.2f} damage!")
    messages.append(f"{player.name} has {player.hp:.2f} HP left!")
    for message in messages:
        print(message)
    return messages