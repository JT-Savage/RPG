"""
Status Effect System
Handles all status effects (Poison, Burn, Sleep, Berserk, etc.)
"""

def apply_status_effect(target, status_name, duration=3, potency=1.0):
    """
    Apply status effect to target

    Args:
        target: Target dict (character or enemy)
        status_name: Status effect name
        duration: Number of turns
        potency: Effect strength multiplier

    Returns:
        bool: Success
    """
    # Check if already has this status
    if has_status(target, status_name):
        # Refresh duration
        for effect in target.get('status_effects', []):
            if effect['name'] == status_name:
                effect['duration'] = max(effect['duration'], duration)
                return True

    # Add new status effect
    if 'status_effects' not in target:
        target['status_effects'] = []

    status_effect = {
        'name': status_name,
        'duration': duration,
        'potency': potency,
        'turns_elapsed': 0
    }

    target['status_effects'].append(status_effect)
    return True

def remove_status_effect(target, status_name):
    """
    Remove status effect from target

    Args:
        target: Target dict
        status_name: Status effect name

    Returns:
        bool: Success
    """
    if 'status_effects' not in target:
        return False

    original_count = len(target['status_effects'])
    target['status_effects'] = [e for e in target['status_effects'] if e['name'] != status_name]

    return len(target['status_effects']) < original_count

def has_status(target, status_name):
    """
    Check if target has status effect

    Args:
        target: Target dict
        status_name: Status effect name

    Returns:
        bool: Has status
    """
    if 'status_effects' not in target:
        return False

    return any(e['name'] == status_name for e in target['status_effects'])

def process_status_effects(target):
    """
    Process status effects at end of turn

    Args:
        target: Target dict

    Returns:
        dict: Status effect results
    """
    if 'status_effects' not in target:
        return {}

    results = {}

    effects_to_remove = []

    for effect in target['status_effects']:
        effect_name = effect['name']
        effect_result = process_single_status_effect(target, effect)

        if effect_result:
            results[effect_name] = effect_result

        # Decrement duration
        effect['duration'] -= 1

        # Mark for removal if expired
        if effect['duration'] <= 0:
            effects_to_remove.append(effect)

    # Remove expired effects
    for effect in effects_to_remove:
        target['status_effects'].remove(effect)

    return results

def process_single_status_effect(target, effect):
    """
    Process a single status effect

    Args:
        target: Target dict
        effect: Effect dict

    Returns:
        dict: Effect result
    """
    effect_name = effect['name']
    potency = effect.get('potency', 1.0)

    result = {'effect': effect_name}

    # Damage over time effects
    if effect_name == 'poison':
        damage = int(target.get('max_hp', 100) * 0.05 * potency)  # 5% max HP
        if 'hp' in target:
            target['hp'] -= damage
            target['hp'] = max(0, target['hp'])
        else:
            target['data']['hp'] -= damage
            target['data']['hp'] = max(0, target['data']['hp'])

        result['damage'] = damage

    elif effect_name == 'burn':
        damage = int(target.get('max_hp', 100) * 0.06 * potency)  # 6% max HP
        if 'hp' in target:
            target['hp'] -= damage
            target['hp'] = max(0, target['hp'])
        else:
            target['data']['hp'] -= damage
            target['data']['hp'] = max(0, target['data']['hp'])

        result['damage'] = damage
        result['can_spread'] = True  # Burn can spread

    # Stat modification effects
    elif effect_name == 'haste':
        result['speed_boost'] = True

    elif effect_name == 'slow':
        result['speed_reduction'] = True

    # Incapacitation effects
    elif effect_name == 'sleep':
        result['incapacitated'] = True

    elif effect_name == 'paralysis':
        result['incapacitated'] = True

    elif effect_name == 'freeze':
        result['incapacitated'] = True

    # Berserk (uncontrollable, attacks random targets)
    elif effect_name == 'berserk':
        result['uncontrolled'] = True

    # Confuse (attacks random targets, including allies)
    elif effect_name == 'confuse':
        result['confused'] = True

    # Silence (cannot cast spells)
    elif effect_name == 'silence':
        result['silenced'] = True

    # Blind (reduced accuracy)
    elif effect_name == 'blind':
        result['accuracy_penalty'] = 0.5

    # Defend (reduces incoming damage)
    elif effect_name == 'defend':
        result['defense_boost'] = 0.5

    # Doom (death after duration expires)
    elif effect_name == 'doom':
        if effect['duration'] <= 1:
            # Death on next turn
            result['fatal'] = True

    # Bubble (Druidess) - Silence + Prevent Attack, breaks when hit
    elif effect_name == 'bubble':
        result['silenced'] = True
        result['cannot_attack'] = True
        result['breaks_on_hit'] = True

    # Prevent Attack (Bubble component)
    elif effect_name == 'prevent_attack':
        result['cannot_attack'] = True

    return result

def get_status_effect_description(status_name):
    """
    Get human-readable description of status effect

    Args:
        status_name: Status effect name

    Returns:
        str: Description
    """
    descriptions = {
        'poison': 'Takes damage each turn (5% max HP)',
        'burn': 'Takes fire damage each turn (6% max HP), can spread to adjacent enemies',
        'sleep': 'Cannot act until hit or duration expires',
        'paralysis': 'Cannot act',
        'freeze': 'Frozen solid, cannot act',
        'silence': 'Cannot cast spells',
        'blind': 'Accuracy reduced by 50%',
        'confuse': 'Attacks random targets including allies',
        'berserk': 'Attacks random enemies, cannot be controlled',
        'haste': 'Increased speed',
        'slow': 'Decreased speed',
        'defend': 'Takes 50% less damage',
        'doom': 'Death after countdown expires',
        'bubble': 'Silenced and cannot attack, breaks when hit'
    }

    return descriptions.get(status_name, 'Unknown status effect')

def should_skip_turn(target):
    """
    Check if target should skip turn due to status effects

    Args:
        target: Target dict

    Returns:
        bool: Should skip turn
    """
    if 'status_effects' not in target:
        return False

    for effect in target['status_effects']:
        effect_name = effect['name']

        # Incapacitation effects
        if effect_name in ['sleep', 'paralysis', 'freeze']:
            return True

    return False

def can_cast_spell(target):
    """
    Check if target can cast spells

    Args:
        target: Target dict

    Returns:
        bool: Can cast
    """
    return not has_status(target, 'silence') and not has_status(target, 'bubble')

def can_attack(target):
    """
    Check if target can attack

    Args:
        target: Target dict

    Returns:
        bool: Can attack
    """
    return not has_status(target, 'prevent_attack') and not has_status(target, 'bubble')

def get_speed_modifier(target):
    """
    Get speed modifier from status effects

    Args:
        target: Target dict

    Returns:
        float: Speed multiplier (1.0 = normal)
    """
    modifier = 1.0

    if has_status(target, 'haste'):
        modifier *= 1.5

    if has_status(target, 'slow'):
        modifier *= 0.5

    return modifier

def get_defense_modifier(target):
    """
    Get defense modifier from status effects

    Args:
        target: Target dict

    Returns:
        float: Defense multiplier (1.0 = normal)
    """
    if has_status(target, 'defend'):
        return 1.5  # 50% more defense

    return 1.0

def get_accuracy_modifier(target):
    """
    Get accuracy modifier from status effects

    Args:
        target: Target dict

    Returns:
        float: Accuracy multiplier (1.0 = normal)
    """
    if has_status(target, 'blind'):
        return 0.5  # 50% accuracy

    return 1.0

def break_bubble(target):
    """
    Break Bubble status when target is hit

    Args:
        target: Target dict
    """
    if has_status(target, 'bubble'):
        remove_status_effect(target, 'bubble')
        remove_status_effect(target, 'silence')
        remove_status_effect(target, 'prevent_attack')
