#GENERAL EFFFECT FUNCTIONS
def restrict_action(character, effect):
    """Prevents the character from taking action for a turn."""
    print(f"{character.name} is affected by {effect.name}!")
    return False  # Indicates that the action is blocked

def poison_damage(character, effect):
    damage = 10
    character.hp -= damage
    print(f"{character.name} is affected by {effect.name} and takes damage!")


def process_status_effects(character):
    # Remove expired effects before applying new ones
    character.status_effects = [effect for effect in character.status_effects if not effect.is_expired()]

    for effect in character.status_effects[:]:  
        effect.tick_effect(character)
effect_map = {
    "Stun": "stunned",
    "Fear": "in a state of fear",
}     