"""
Enemy data with FF6-style difficulty progression
Includes enemy stats, abilities, and spawn mechanics
"""

# Enemy definitions
ENEMIES = {
    # Early Game - Tutorial/Warren
    'infected_kobold_weak': {
        'name': 'Infected Kobold',
        'level': 1,
        'hp': 15,
        'mp': 0,
        'attack': 8,
        'defense': 5,
        'magic_power': 0,
        'spell_resistance': 3,
        'speed': 10,
        'exp_reward': 5,
        'gil_reward': 10,
        'resistances': {},
        'weaknesses': {'holy': 1.5},
        'type': 'undead',
        'abilities': ['weak_scratch'],
        'description': 'A kobold infected with the necromantic plague',
        'sprite': 'infected_kobold_1'
    },

    'skeleton': {
        'name': 'Skeleton',
        'level': 3,
        'hp': 25,
        'mp': 0,
        'attack': 12,
        'defense': 8,
        'magic_power': 0,
        'spell_resistance': 5,
        'speed': 8,
        'exp_reward': 10,
        'gil_reward': 20,
        'resistances': {'dark': 0.5},
        'weaknesses': {'holy': 2.0},
        'type': 'undead',
        'abilities': ['slash'],
        'description': 'Animated skeleton warrior',
        'sprite': 'skeleton'
    },

    # Wildlife - Pre-Fungal Removal
    'fungal_deer': {
        'name': 'Fungal Deer',
        'level': 4,
        'hp': 35,
        'mp': 5,
        'attack': 14,
        'defense': 10,
        'magic_power': 8,
        'spell_resistance': 8,
        'speed': 12,
        'exp_reward': 15,
        'gil_reward': 25,
        'resistances': {},
        'weaknesses': {'fire': 1.5},
        'type': 'wildlife_fungal',
        'abilities': ['ram', 'spore_cloud'],
        'learnable_by_iris': True,
        'removed_after': 'jerod_house_explosion',
        'description': 'Wildlife infected with fungal undead',
        'sprite': 'fungal_deer'
    },

    # Surface Enemies
    'lycanthrope': {
        'name': 'Lycanthrope',
        'level': 5,
        'hp': 50,
        'mp': 0,
        'attack': 18,
        'defense': 12,
        'magic_power': 0,
        'spell_resistance': 10,
        'speed': 15,
        'exp_reward': 25,
        'gil_reward': 40,
        'resistances': {},
        'weaknesses': {'fire': 1.3},
        'type': 'beast',
        'abilities': ['claw_attack', 'howl'],
        'description': 'Fierce werewolf creature',
        'sprite': 'lycanthrope'
    },

    'bandit': {
        'name': 'Bandit',
        'level': 4,
        'hp': 40,
        'mp': 0,
        'attack': 16,
        'defense': 11,
        'magic_power': 0,
        'spell_resistance': 8,
        'speed': 13,
        'exp_reward': 20,
        'gil_reward': 60,
        'resistances': {},
        'weaknesses': {},
        'type': 'human',
        'abilities': ['slash', 'steal'],
        'description': 'Common highway bandit',
        'sprite': 'bandit'
    },

    # Post-Imperial Warren Escape - Infected Kobolds Dominate
    'infected_kobold': {
        'name': 'Infected Kobold',
        'level': 6,
        'hp': 55,
        'mp': 0,
        'attack': 20,
        'defense': 14,
        'magic_power': 0,
        'spell_resistance': 10,
        'speed': 14,
        'exp_reward': 30,
        'gil_reward': 35,
        'resistances': {},
        'weaknesses': {'holy': 1.5, 'fire': 1.3},
        'type': 'undead',
        'abilities': ['bite', 'scratch', 'infection_cloud'],
        'spawn_rate_post_imperial': 0.70,  # 70% of encounters
        'description': 'Kobold infected with necromantic plague',
        'sprite': 'infected_kobold'
    },

    'infected_kobold_strong': {
        'name': 'Infected Kobold Warrior',
        'level': 8,
        'hp': 80,
        'mp': 0,
        'attack': 26,
        'defense': 18,
        'magic_power': 0,
        'spell_resistance': 12,
        'speed': 16,
        'exp_reward': 45,
        'gil_reward': 50,
        'resistances': {},
        'weaknesses': {'holy': 1.5, 'fire': 1.3},
        'type': 'undead',
        'abilities': ['heavy_slash', 'infection_cloud', 'rally'],
        'spawn_rate_post_imperial': 0.30,  # Appears with regular infected kobolds
        'description': 'Stronger infected kobold warrior',
        'sprite': 'infected_kobold_warrior'
    },

    # Undead Lands Enemies
    'zombie_orc': {
        'name': 'Zombie Orc',
        'level': 7,
        'hp': 90,
        'mp': 0,
        'attack': 28,
        'defense': 20,
        'magic_power': 0,
        'spell_resistance': 14,
        'speed': 8,
        'exp_reward': 50,
        'gil_reward': 60,
        'resistances': {'physical': 0.1},
        'weaknesses': {'holy': 2.0, 'fire': 1.5},
        'type': 'undead',
        'abilities': ['smash', 'roar'],
        'description': 'Reanimated orc warrior',
        'sprite': 'zombie_orc'
    },

    'wraith': {
        'name': 'Wraith',
        'level': 9,
        'hp': 70,
        'mp': 20,
        'attack': 24,
        'defense': 15,
        'magic_power': 18,
        'spell_resistance': 20,
        'speed': 18,
        'exp_reward': 60,
        'gil_reward': 70,
        'resistances': {'physical': 0.5, 'dark': 0.5},
        'weaknesses': {'holy': 2.5},
        'type': 'undead',
        'abilities': ['life_drain', 'curse', 'shadow_touch'],
        'description': 'Ghostly undead creature',
        'sprite': 'wraith'
    },

    # Mid-Game Enemies
    'cultist': {
        'name': 'Cultist',
        'level': 10,
        'hp': 100,
        'mp': 30,
        'attack': 22,
        'defense': 18,
        'magic_power': 24,
        'spell_resistance': 22,
        'speed': 15,
        'exp_reward': 80,
        'gil_reward': 90,
        'resistances': {'dark': 0.3},
        'weaknesses': {'holy': 1.8},
        'type': 'human',
        'abilities': ['dark_bolt', 'curse', 'poison'],
        'description': 'Follower of the necromancer',
        'sprite': 'cultist'
    },

    'infected_kobold_mage': {
        'name': 'Infected Kobold Mage',
        'level': 11,
        'hp': 85,
        'mp': 40,
        'attack': 18,
        'defense': 16,
        'magic_power': 28,
        'spell_resistance': 24,
        'speed': 17,
        'exp_reward': 90,
        'gil_reward': 80,
        'resistances': {},
        'weaknesses': {'holy': 1.5},
        'type': 'undead',
        'abilities': ['fire', 'blizzard', 'infection_bolt'],
        'spawn_rate_post_imperial': 0.20,
        'description': 'Infected kobold with magical abilities',
        'sprite': 'infected_kobold_mage'
    },

    # Desert Region - Difficulty Spike
    'desert_infected_kobold': {
        'name': 'Desert Infected Kobold',
        'level': 18,
        'hp': 250,
        'mp': 0,
        'attack': 55,
        'defense': 40,
        'magic_power': 0,
        'spell_resistance': 35,
        'speed': 28,
        'exp_reward': 200,
        'gil_reward': 150,
        'resistances': {'fire': 0.3},
        'weaknesses': {'holy': 1.5, 'ice': 1.3},
        'type': 'undead',
        'abilities': ['double_slash', 'infection_cloud', 'sand_blind'],
        'spawn_rate_desert': 0.50,
        'description': 'Infected kobold adapted to desert',
        'sprite': 'desert_infected_kobold'
    },

    'sand_wraith': {
        'name': 'Sand Wraith',
        'level': 20,
        'hp': 280,
        'mp': 60,
        'attack': 50,
        'defense': 38,
        'magic_power': 52,
        'spell_resistance': 50,
        'speed': 32,
        'exp_reward': 250,
        'gil_reward': 180,
        'resistances': {'physical': 0.5, 'dark': 0.5, 'wind': 0.5},
        'weaknesses': {'holy': 2.5, 'water': 1.5},
        'type': 'undead',
        'abilities': ['sandstorm', 'life_drain', 'curse', 'shadow_strike'],
        'spawn_rate_desert': 0.30,
        'description': 'Powerful desert spirit',
        'sprite': 'sand_wraith'
    },

    'bone_dragon': {
        'name': 'Bone Dragon',
        'level': 22,
        'hp': 400,
        'mp': 50,
        'attack': 65,
        'defense': 50,
        'magic_power': 45,
        'spell_resistance': 45,
        'speed': 25,
        'exp_reward': 350,
        'gil_reward': 250,
        'resistances': {'physical': 0.3, 'dark': 0.5},
        'weaknesses': {'holy': 2.0},
        'type': 'undead_dragon',
        'abilities': ['bone_breath', 'tail_swipe', 'roar'],
        'spawn_rate_desert': 0.10,
        'description': 'Skeletal dragon remains',
        'sprite': 'bone_dragon'
    },

    # Endgame - Catacombs
    'elite_cultist': {
        'name': 'Elite Cultist',
        'level': 25,
        'hp': 550,
        'mp': 100,
        'attack': 70,
        'defense': 60,
        'magic_power': 75,
        'spell_resistance': 70,
        'speed': 35,
        'exp_reward': 500,
        'gil_reward': 400,
        'resistances': {'dark': 0.5},
        'weaknesses': {'holy': 2.0},
        'type': 'human',
        'abilities': ['fira', 'blizzara', 'thundara', 'death_coil', 'curse'],
        'description': 'High-ranking cultist',
        'sprite': 'elite_cultist'
    },

    'death_knight': {
        'name': 'Death Knight',
        'level': 27,
        'hp': 700,
        'mp': 80,
        'attack': 85,
        'defense': 75,
        'magic_power': 60,
        'spell_resistance': 65,
        'speed': 30,
        'exp_reward': 600,
        'gil_reward': 500,
        'resistances': {'physical': 0.3, 'dark': 0.5, 'holy': 0.3},
        'weaknesses': {},
        'type': 'undead',
        'abilities': ['death_strike', 'dark_wave', 'summon_skeleton', 'heavy_slash'],
        'description': 'Powerful undead knight',
        'sprite': 'death_knight_enemy'
    },

    # Lost Characters as Zombies (Final Battle)
    'zombie_cookie': {
        'name': 'Zombie Cookie',
        'level': 30,
        'hp': 800,
        'mp': 50,
        'attack': 60,
        'defense': 65,
        'magic_power': 70,
        'spell_resistance': 60,
        'speed': 35,
        'exp_reward': 0,
        'gil_reward': 0,
        'resistances': {},
        'weaknesses': {'holy': 1.5},
        'type': 'undead_ally',
        'abilities': ['sandstorm', 'poison', 'entangle'],
        'appears_if': 'cookie_not_recruited',
        'description': 'Your lost ally, turned undead',
        'sprite': 'zombie_cookie'
    },

    'zombie_iris': {
        'name': 'Zombie Iris',
        'level': 30,
        'hp': 850,
        'mp': 0,
        'attack': 80,
        'defense': 60,
        'magic_power': 0,
        'spell_resistance': 50,
        'speed': 45,
        'exp_reward': 0,
        'gil_reward': 0,
        'resistances': {},
        'weaknesses': {'holy': 1.5},
        'type': 'undead_ally',
        'abilities': ['triple_claw', 'wild_strike'],
        'appears_if': 'iris_not_recruited',
        'description': 'Your lost ally, turned undead',
        'sprite': 'zombie_iris'
    },

    'zombie_fritzzit': {
        'name': 'Zombie Fritzzit',
        'level': 30,
        'hp': 750,
        'mp': 0,
        'attack': 90,
        'defense': 55,
        'magic_power': 0,
        'spell_resistance': 45,
        'speed': 50,
        'exp_reward': 0,
        'gil_reward': 0,
        'resistances': {},
        'weaknesses': {'holy': 1.5},
        'type': 'undead_ally',
        'abilities': ['headshot', 'explosive_shot'],
        'appears_if': 'fritzzit_not_recruited',
        'description': 'Your lost ally, turned undead',
        'sprite': 'zombie_fritzzit'
    },

    'zombie_crankpot': {
        'name': 'Zombie Crankpot',
        'level': 30,
        'hp': 700,
        'mp': 80,
        'attack': 50,
        'defense': 50,
        'magic_power': 85,
        'spell_resistance': 70,
        'speed': 40,
        'exp_reward': 0,
        'gil_reward': 0,
        'resistances': {'fire': 0.5},
        'weaknesses': {'holy': 1.5, 'ice': 1.3},
        'type': 'undead_ally',
        'abilities': ['firaga', 'inferno', 'burn_touch'],
        'appears_if': 'crankpot_not_recruited',
        'description': 'Your lost ally, turned undead',
        'sprite': 'zombie_crankpot'
    },

    'zombie_yipp': {
        'name': 'Zombie Yipp',
        'level': 30,
        'hp': 680,
        'mp': 90,
        'attack': 48,
        'defense': 48,
        'magic_power': 80,
        'spell_resistance': 75,
        'speed': 42,
        'exp_reward': 0,
        'gil_reward': 0,
        'resistances': {'dark': 0.5},
        'weaknesses': {'holy': 1.5},
        'type': 'undead_ally',
        'abilities': ['death_coil', 'curse', 'summon_zombie'],
        'appears_if': 'yipp_not_recruited',
        'description': 'Your lost ally, turned undead',
        'sprite': 'zombie_yipp'
    }
}

# Boss definitions
BOSSES = {
    'jerod_fungal_hive': {
        'name': 'Jerod - Fungal Hive',
        'level': 12,
        'hp': 1200,
        'mp': 100,
        'attack': 40,
        'defense': 35,
        'magic_power': 45,
        'spell_resistance': 40,
        'speed': 20,
        'exp_reward': 1000,
        'gil_reward': 1500,
        'resistances': {'poison': 1.0},
        'weaknesses': {'fire': 2.0},
        'type': 'boss',
        'abilities': ['spore_explosion', 'infect', 'tentacle_grab', 'regenerate'],
        'phases': [
            {'hp_threshold': 1.0, 'abilities': ['spore_explosion', 'infect']},
            {'hp_threshold': 0.5, 'abilities': ['spore_explosion', 'infect', 'tentacle_grab', 'regenerate']}
        ],
        'explodes_on_defeat': True,
        'removes_fungal_enemies': True,
        'description': 'Jerod transformed into a fungal hive',
        'sprite': 'jerod_boss'
    },

    'black_dragon': {
        'name': 'Undead Black Dragon',
        'level': 22,
        'hp': 3500,
        'mp': 150,
        'attack': 80,
        'defense': 70,
        'magic_power': 75,
        'spell_resistance': 65,
        'speed': 35,
        'exp_reward': 3000,
        'gil_reward': 3000,
        'resistances': {'dark': 0.5, 'physical': 0.2},
        'weaknesses': {'holy': 1.8},
        'type': 'boss_dragon',
        'abilities': ['dark_breath', 'claw_swipe', 'tail_whip', 'death_gaze'],
        'phases': [
            {'hp_threshold': 1.0, 'abilities': ['dark_breath', 'claw_swipe']},
            {'hp_threshold': 0.7, 'abilities': ['dark_breath', 'claw_swipe', 'tail_whip']},
            {'hp_threshold': 0.3, 'abilities': ['dark_breath', 'claw_swipe', 'tail_whip', 'death_gaze']}
        ],
        'required_before': 'second_dragon_unlocks',
        'description': 'First of the undead dragons',
        'sprite': 'black_dragon_boss'
    },

    'undead_dragon_magic_resistant': {
        'name': 'Undead Dragon - Ancient',
        'level': 24,
        'hp': 4000,
        'mp': 200,
        'attack': 85,
        'defense': 75,
        'magic_power': 90,
        'spell_resistance': 100,  # Magic resistant
        'speed': 38,
        'exp_reward': 3500,
        'gil_reward': 3500,
        'resistances': {'dark': 0.5, 'magical': 0.5},  # High magic resistance
        'weaknesses': {'holy': 1.5, 'physical': 1.2},  # Weak to physical
        'type': 'boss_dragon',
        'abilities': ['ancient_breath', 'wing_buffet', 'dragon_roar', 'meteor_swarm'],
        'phases': [
            {'hp_threshold': 1.0, 'abilities': ['ancient_breath', 'wing_buffet']},
            {'hp_threshold': 0.6, 'abilities': ['ancient_breath', 'wing_buffet', 'dragon_roar']},
            {'hp_threshold': 0.3, 'abilities': ['ancient_breath', 'wing_buffet', 'dragon_roar', 'meteor_swarm']}
        ],
        'flood_dies_after': True,  # Flood dies in cutscene after this boss
        'description': 'Second dragon - highly magic resistant',
        'sprite': 'ancient_dragon_boss'
    },

    'necromancer_lich': {
        'name': 'Ancient Dragonborn Lich',
        'level': 35,
        'hp': 8000,
        'mp': 500,
        'attack': 95,
        'defense': 90,
        'magic_power': 120,
        'spell_resistance': 110,
        'speed': 45,
        'exp_reward': 10000,
        'gil_reward': 10000,
        'resistances': {'dark': 0.5, 'physical': 0.3, 'ice': 0.5},
        'weaknesses': {'holy': 2.0},
        'type': 'boss_final',
        'abilities': ['ultimate_dark', 'meteor', 'death', 'life_drain', 'summon_undead'],
        'phases': [
            {'hp_threshold': 1.0, 'abilities': ['ultimate_dark', 'life_drain']},
            {'hp_threshold': 0.7, 'abilities': ['ultimate_dark', 'meteor', 'life_drain', 'summon_undead']},
            {'hp_threshold': 0.4, 'abilities': ['ultimate_dark', 'meteor', 'death', 'life_drain', 'summon_undead']},
            {'hp_threshold': 0.2, 'abilities': ['ultimate_dark', 'meteor', 'death', 'life_drain', 'summon_undead'], 'rage_mode': True}
        ],
        'yipp_vampire_joins': True,  # If Yipp is Vampire, he fights with Lich
        'lost_characters_as_zombies': True,
        'description': 'The ancient necromancer behind the plague',
        'sprite': 'lich_boss'
    },

    'double_infected_kella': {
        'name': 'Queen Kella - Double Infected',
        'level': 38,
        'hp': 10000,
        'mp': 400,
        'attack': 110,
        'defense': 100,
        'magic_power': 130,
        'spell_resistance': 120,
        'speed': 55,
        'exp_reward': 15000,
        'gil_reward': 15000,
        'resistances': {'dark': 0.5, 'poison': 1.0, 'physical': 0.3},
        'weaknesses': {'holy': 2.5, 'fire': 1.5},
        'type': 'boss_secret',
        'abilities': ['queens_wrath', 'infection_wave', 'spore_cloud', 'double_strike', 'regenerate'],
        'phases': [
            {'hp_threshold': 1.0, 'abilities': ['queens_wrath', 'infection_wave']},
            {'hp_threshold': 0.6, 'abilities': ['queens_wrath', 'infection_wave', 'spore_cloud', 'double_strike']},
            {'hp_threshold': 0.3, 'abilities': ['queens_wrath', 'infection_wave', 'spore_cloud', 'double_strike', 'regenerate']}
        ],
        'appears_if': 'cure_not_found',
        'bad_ending_route': True,
        'description': 'Kella transformed by dual infection',
        'sprite': 'kella_boss'
    },

    'infected_red_dragon': {
        'name': 'Infected Red Dragon',
        'level': 40,
        'hp': 12000,
        'mp': 300,
        'attack': 125,
        'defense': 110,
        'magic_power': 110,
        'spell_resistance': 100,
        'speed': 50,
        'exp_reward': 20000,
        'gil_reward': 20000,
        'resistances': {'fire': 0.5, 'dark': 0.5, 'physical': 0.3},
        'weaknesses': {'holy': 2.0, 'ice': 1.8},
        'type': 'boss_secret',
        'abilities': ['inferno_breath', 'meteor_storm', 'dragon_claw', 'wing_gust', 'enrage'],
        'phases': [
            {'hp_threshold': 1.0, 'abilities': ['inferno_breath', 'dragon_claw']},
            {'hp_threshold': 0.7, 'abilities': ['inferno_breath', 'meteor_storm', 'dragon_claw']},
            {'hp_threshold': 0.5, 'abilities': ['inferno_breath', 'meteor_storm', 'dragon_claw', 'wing_gust']},
            {'hp_threshold': 0.25, 'abilities': ['inferno_breath', 'meteor_storm', 'dragon_claw', 'wing_gust', 'enrage'], 'rage_mode': True}
        ],
        'fights_with': 'double_infected_kella',
        'appears_if': 'cure_not_found',
        'bad_ending_route': True,
        'description': 'Red dragon weakened by infection',
        'sprite': 'red_dragon_boss'
    },

    'captain_donald': {
        'name': 'Slaver Captain Donald',
        'level': 35,
        'hp': 7500,
        'mp': 100,
        'attack': 105,
        'defense': 95,
        'magic_power': 60,
        'spell_resistance': 85,
        'speed': 50,
        'exp_reward': 12000,
        'gil_reward': 15000,
        'resistances': {},
        'weaknesses': {},
        'type': 'boss_secret',
        'abilities': ['captains_strike', 'whip_crack', 'command_slaves', 'dirty_fighting'],
        'phases': [
            {'hp_threshold': 1.0, 'abilities': ['captains_strike', 'whip_crack']},
            {'hp_threshold': 0.5, 'abilities': ['captains_strike', 'whip_crack', 'command_slaves', 'dirty_fighting']}
        ],
        'post_credits_only': True,
        'best_ending_requirement': True,
        'description': 'Ruthless slaver captain',
        'sprite': 'donald_boss'
    }
}

# Encounter tables by region
ENCOUNTER_TABLES = {
    'tutorial_warren': {
        'enemies': ['infected_kobold_weak'],
        'encounter_rate': 0.15,
        'max_group_size': 3
    },

    'surface_forest': {
        'enemies': ['lycanthrope', 'bandit', 'skeleton'],
        'encounter_rate': 0.20,
        'max_group_size': 4
    },

    'undead_lands': {
        'enemies': ['skeleton', 'zombie_orc', 'wraith', 'infected_kobold'],
        'encounter_rate': 0.25,
        'max_group_size': 4
    },

    'post_imperial_warren': {
        'enemies': {
            'infected_kobold': 0.50,  # 50%
            'infected_kobold_strong': 0.20,  # 20%
            'infected_kobold_mage': 0.10,  # 10%
            'skeleton': 0.10,  # 10%
            'wraith': 0.10  # 10%
        },
        'encounter_rate': 0.30,
        'max_group_size': 5,
        'note': 'Infected kobolds dominate spawns'
    },

    'desert_region': {
        'enemies': {
            'desert_infected_kobold': 0.35,  # 35%
            'infected_kobold_strong': 0.15,  # 15%
            'sand_wraith': 0.20,  # 20%
            'bone_dragon': 0.05,  # 5%
            'cultist': 0.15,  # 15%
            'death_knight': 0.10  # 10%
        },
        'encounter_rate': 0.35,  # Higher encounter rate
        'max_group_size': 4,
        'note': 'Difficulty spike - FF6 style progression'
    },

    'catacombs': {
        'enemies': {
            'elite_cultist': 0.40,
            'death_knight': 0.30,
            'infected_kobold_strong': 0.20,
            'wraith': 0.10
        },
        'encounter_rate': 0.40,
        'max_group_size': 3,
        'note': 'Endgame difficulty'
    }
}

# Enemy spawn modifications based on story events
SPAWN_MODIFICATIONS = {
    'fungal_enemies_removed': {
        'trigger': 'jerod_house_explosion',
        'removes_enemies': ['fungal_deer'],
        'description': 'Fungal wildlife removed after Jerod boss fight'
    },

    'infected_kobolds_dominate': {
        'trigger': 'imperial_warren_escape',
        'modifies_spawn_rates': {
            'infected_kobold': 0.70,
            'infected_kobold_strong': 0.30
        },
        'description': 'Infected kobolds become dominant after warren escape'
    },

    'desert_mixed_undead': {
        'trigger': 'enter_desert',
        'spawn_balance': '50_50_kobolds_other_undead',
        'description': 'Desert has balanced undead encounters'
    }
}

def get_enemy_stats(enemy_id):
    """Get enemy stats by ID"""
    return ENEMIES.get(enemy_id) or BOSSES.get(enemy_id)

def get_encounter_table(region, story_flags=None):
    """
    Get encounter table for a region with story modifications

    Args:
        region: Region identifier
        story_flags: Dict of story flags to check modifications

    Returns:
        Dict with enemy spawn data
    """
    table = ENCOUNTER_TABLES.get(region, {})

    if not story_flags:
        return table

    # Apply story modifications
    modified_table = table.copy()

    # Check for fungal enemy removal
    if story_flags.get('jerod_house_explosion'):
        if isinstance(modified_table.get('enemies'), list):
            modified_table['enemies'] = [e for e in modified_table['enemies'] if e != 'fungal_deer']

    # Check for infected kobold spawn rate increase
    if story_flags.get('imperial_warren_escape') and region == 'post_imperial_warren':
        # Already in table definition
        pass

    return modified_table
