"""
Level-Up System
Handles experience, leveling, and ability learning (every 10 levels)
"""

from data.characters import LEVEL_UP_ABILITIES, get_character_stats_at_level, get_max_level

# Experience table (FF6-style curve)
EXP_TABLE = {}

def calculate_exp_for_level(level):
    """
    Calculate EXP required for a level (FF6-style curve)

    Args:
        level: Target level

    Returns:
        int: Total EXP required
    """
    if level <= 1:
        return 0

    # Exponential curve similar to FF6
    base = 16
    multiplier = level ** 3
    return int(base * multiplier * 0.8)

# Pre-calculate EXP table
for i in range(1, 100):
    EXP_TABLE[i] = calculate_exp_for_level(i)

def get_exp_to_next_level(current_level):
    """
    Get EXP required to reach next level

    Args:
        current_level: Current level

    Returns:
        int: EXP needed for next level
    """
    if current_level >= 99:
        return 0

    return EXP_TABLE.get(current_level + 1, 0) - EXP_TABLE.get(current_level, 0)

def add_experience(game_state, char_id, exp_gained):
    """
    Add experience to character and handle level-ups

    Args:
        game_state: GameState instance
        char_id: Character identifier
        exp_gained: EXP amount

    Returns:
        dict: Level-up results
    """
    char = game_state.characters.get(char_id)
    if not char:
        return None

    # Check if character is dead (Flood)
    if game_state.story_flags.get('flood_dead') and char_id == 'flood':
        return None

    # Add EXP
    char['exp'] += exp_gained

    results = {
        'char_id': char_id,
        'exp_gained': exp_gained,
        'leveled_up': False,
        'levels_gained': 0,
        'new_level': char['level'],
        'abilities_learned': [],
        'stat_increases': {}
    }

    # Check for level-up(s)
    max_level = game_state.level_caps.get(char_id, 75)

    while char['level'] < max_level:
        exp_needed = get_exp_to_next_level(char['level'])

        if char['exp'] >= exp_needed:
            # Level up!
            char['level'] += 1
            char['exp'] -= exp_needed

            results['leveled_up'] = True
            results['levels_gained'] += 1
            results['new_level'] = char['level']

            # Recalculate stats
            old_stats = char['stats'].copy()
            old_max_hp = char['max_hp']
            old_max_mp = char['max_mp']

            new_stats = get_character_stats_at_level(char_id, char['level'])
            char['max_hp'] = int(new_stats['hp'])
            char['max_mp'] = int(new_stats['mp'])
            char['stats'] = {
                'attack': int(new_stats['attack']),
                'defense': int(new_stats['defense']),
                'magic_power': int(new_stats['magic_power']),
                'spell_resistance': int(new_stats['spell_resistance']),
                'speed': int(new_stats['speed'])
            }

            # Heal by stat increase amount
            hp_increase = char['max_hp'] - old_max_hp
            mp_increase = char['max_mp'] - old_max_mp

            char['hp'] += hp_increase
            char['mp'] += mp_increase

            results['stat_increases'] = {
                'hp': hp_increase,
                'mp': mp_increase,
                'attack': char['stats']['attack'] - old_stats.get('attack', 0),
                'defense': char['stats']['defense'] - old_stats.get('defense', 0),
                'magic_power': char['stats']['magic_power'] - old_stats.get('magic_power', 0),
                'spell_resistance': char['stats']['spell_resistance'] - old_stats.get('spell_resistance', 0),
                'speed': char['stats']['speed'] - old_stats.get('speed', 0)
            }

            # Check for ability learning (every 10 levels)
            if char['level'] % 10 == 0:
                ability = learn_ability(game_state, char_id, char['level'])
                if ability:
                    results['abilities_learned'].append(ability)

        else:
            break

    return results

def learn_ability(game_state, char_id, level):
    """
    Learn ability at specific level milestone

    Args:
        game_state: GameState instance
        char_id: Character identifier
        level: Level reached

    Returns:
        dict: Ability learned
    """
    # Get character's current class
    current_class = game_state.character_classes.get(char_id)
    char_abilities = LEVEL_UP_ABILITIES.get(char_id)

    if not char_abilities:
        return None

    # Special handling for Yipp (has different ability trees)
    if char_id == 'yipp':
        yipp_alignment = game_state.story_flags.get('yipp_alignment', 'necromancer')
        char_abilities = char_abilities.get(yipp_alignment, char_abilities.get('necromancer'))

    # Get ability for this level
    ability_data = char_abilities.get(level)

    if not ability_data:
        return None

    # Check if already learned
    char = game_state.characters[char_id]
    if ability_data['name'] in char.get('learned_abilities', []):
        return None

    # Add to learned abilities
    if 'learned_abilities' not in char:
        char['learned_abilities'] = []

    char['learned_abilities'].append(ability_data['name'])

    return ability_data

def can_level_up(game_state, char_id):
    """
    Check if character can level up

    Args:
        game_state: GameState instance
        char_id: Character identifier

    Returns:
        bool: Can level up
    """
    char = game_state.characters.get(char_id)
    if not char:
        return False

    max_level = game_state.level_caps.get(char_id, 75)

    if char['level'] >= max_level:
        return False

    exp_needed = get_exp_to_next_level(char['level'])
    return char['exp'] >= exp_needed

def get_level_progress(game_state, char_id):
    """
    Get level progress percentage

    Args:
        game_state: GameState instance
        char_id: Character identifier

    Returns:
        float: Progress (0.0 to 1.0)
    """
    char = game_state.characters.get(char_id)
    if not char:
        return 0.0

    exp_needed = get_exp_to_next_level(char['level'])
    if exp_needed == 0:
        return 1.0

    return min(1.0, char['exp'] / exp_needed)

def distribute_battle_exp(game_state, total_exp):
    """
    Distribute battle EXP to all party members

    Args:
        game_state: GameState instance
        total_exp: Total EXP to distribute

    Returns:
        dict: Results for each character
    """
    results = {}

    # All characters in party get full EXP (FF6 style)
    for char_id in game_state.active_party:
        char = game_state.characters.get(char_id)

        if char and char['hp'] > 0:  # Only alive characters
            result = add_experience(game_state, char_id, total_exp)
            if result:
                results[char_id] = result

    # Reserve party also gets EXP (but less)
    for char_id in game_state.reserve_party:
        reserve_exp = int(total_exp * 0.5)  # 50% EXP for reserves
        result = add_experience(game_state, char_id, reserve_exp)
        if result:
            result['reserve'] = True
            results[char_id] = result

    return results

def learn_spell_from_shop(game_state, char_id, spell_id):
    """
    Learn spell from magic shop

    Args:
        game_state: GameState instance
        char_id: Character identifier
        spell_id: Spell identifier

    Returns:
        bool: Success
    """
    from data.spells import can_character_learn_spell

    # Check if character can learn this spell
    current_class = game_state.character_classes.get(char_id)

    if not can_character_learn_spell(current_class, spell_id):
        return False

    char = game_state.characters.get(char_id)
    if not char:
        return False

    # Check if already learned
    if spell_id in char.get('learned_spells', []):
        return False

    # Add to learned spells
    if 'learned_spells' not in char:
        char['learned_spells'] = []

    char['learned_spells'].append(spell_id)
    return True

def get_learnable_spells(game_state, char_id):
    """
    Get list of spells character can learn

    Args:
        game_state: GameState instance
        char_id: Character identifier

    Returns:
        list: List of spell IDs
    """
    from data.spells import SPELLS, can_character_learn_spell
    from data.characters import CHARACTERS

    char_data = CHARACTERS.get(char_id)
    if not char_data:
        return []

    if not char_data.get('can_learn_magic', False):
        return []

    current_class = game_state.character_classes.get(char_id)
    char = game_state.characters.get(char_id)

    learnable = []
    for spell_id, spell_data in SPELLS.items():
        # Check if can learn
        if can_character_learn_spell(current_class, spell_id):
            # Check if not already learned
            if spell_id not in char.get('learned_spells', []):
                learnable.append(spell_id)

    return learnable

def has_learned_ability(game_state, char_id, ability_name):
    """
    Check if character has learned an ability

    Args:
        game_state: GameState instance
        char_id: Character identifier
        ability_name: Ability name

    Returns:
        bool: Has learned
    """
    char = game_state.characters.get(char_id)
    if not char:
        return False

    return ability_name in char.get('learned_abilities', [])

def get_next_ability_level(char_level):
    """
    Get next level where an ability is learned

    Args:
        char_level: Current level

    Returns:
        int: Next ability level (or None)
    """
    milestones = [10, 20, 30, 40, 50, 60, 70, 80, 90]

    for milestone in milestones:
        if char_level < milestone:
            return milestone

    return None
