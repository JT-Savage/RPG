"""
Location Data
All game locations, NPCs, and triggers
"""

LOCATIONS = {
    # === Tutorial Area ===

    'tutorial_warren': {
        'name': 'Kobold Warren (Tutorial)',
        'description': 'A dark underground warren where kobolds once worked.',
        'spawn_position': [20, 100],
        'fast_travel': False,
        'encounter_rate': 0.15,
        'encounter_table': 'tutorial_warren'
    },

    # === Surface World ===

    'surface_forest': {
        'name': 'Forest Path',
        'description': 'A peaceful forest near the warren entrance.',
        'spawn_position': [128, 200],
        'fast_travel': True,
        'encounter_rate': 0.20,
        'encounter_table': 'surface_forest',
        'requires_flag': 'warren_escaped'
    },

    # === Imperial City ===

    'imperial_city': {
        'name': 'Imperial City',
        'description': 'The grand capital of the Empire.',
        'spawn_position': [128, 180],
        'fast_travel': True,
        'encounter_rate': 0.0,  # No encounters in city
        'requires_flag': 'warren_escaped'
    },

    'imperial_city_inn': {
        'name': 'Imperial Inn',
        'description': 'A cozy inn where travelers rest.',
        'spawn_position': [128, 112],
        'fast_travel': False,
        'encounter_rate': 0.0,
        'parent_location': 'imperial_city'
    },

    'imperial_magic_shop': {
        'name': 'Imperial Magic Shop',
        'description': 'Spells and magical items for sale.',
        'spawn_position': [128, 112],
        'fast_travel': False,
        'encounter_rate': 0.0,
        'parent_location': 'imperial_city'
    },

    'imperial_weapon_shop': {
        'name': 'Imperial Weapon & Armor',
        'description': 'The finest weapons and armor in the Empire.',
        'spawn_position': [128, 112],
        'fast_travel': False,
        'encounter_rate': 0.0,
        'parent_location': 'imperial_city'
    },

    'imperial_cathedral': {
        'name': 'Cathedral',
        'description': 'A holy place of healing and prayer.',
        'spawn_position': [128, 112],
        'fast_travel': False,
        'encounter_rate': 0.0,
        'parent_location': 'imperial_city'
    },

    # === Post-Warren ===

    'post_imperial_warren': {
        'name': 'Infected Warren',
        'description': 'The warren has been overrun by infected kobolds.',
        'spawn_position': [128, 112],
        'fast_travel': True,
        'encounter_rate': 0.30,
        'encounter_table': 'post_imperial_warren',
        'requires_flag': 'kobolds_released'
    },

    # === Undead Lands ===

    'undead_lands': {
        'name': 'Undead Lands',
        'description': 'A cursed land filled with undead creatures.',
        'spawn_position': [128, 112],
        'fast_travel': True,
        'encounter_rate': 0.25,
        'encounter_table': 'undead_lands',
        'requires_flag': 'imperial_city_visited'
    },

    # === Army Camp ===

    'army_camp': {
        'name': 'Imperial Army Camp',
        'description': 'A military encampment preparing for battle.',
        'spawn_position': [128, 112],
        'fast_travel': True,
        'encounter_rate': 0.0
    },

    # === Desert Region ===

    'desert_region': {
        'name': 'Deep Desert',
        'description': 'An endless desert hiding dark secrets.',
        'spawn_position': [128, 112],
        'fast_travel': True,
        'encounter_rate': 0.25,
        'encounter_table': 'desert_region',
        'requires_flag': 'desert_entered'
    },

    'desert_outpost': {
        'name': 'Desert Outpost',
        'description': 'A small trading post in the desert.',
        'spawn_position': [128, 112],
        'fast_travel': True,
        'encounter_rate': 0.0,
        'parent_location': 'desert_region'
    },

    # === Dungeons ===

    'catacombs': {
        'name': 'Catacombs',
        'description': 'Ancient underground tombs.',
        'spawn_position': [20, 20],
        'fast_travel': False,
        'encounter_rate': 0.30,
        'encounter_table': 'catacombs'
    },

    'jerod_house': {
        'name': 'Jerod\'s House',
        'description': 'A suspicious house on the outskirts.',
        'spawn_position': [128, 180],
        'fast_travel': False,
        'encounter_rate': 0.20
    },

    'capitol_ruins': {
        'name': 'Capitol Ruins',
        'description': 'The fallen capitol, now in ruins.',
        'spawn_position': [128, 112],
        'fast_travel': True,
        'encounter_rate': 0.25,
        'requires_flag': 'desert_entered'
    },

    # === Final Area ===

    'necromancer_sanctum': {
        'name': 'Necromancer\'s Sanctum',
        'description': 'The source of the undead plague.',
        'spawn_position': [128, 20],
        'fast_travel': False,
        'encounter_rate': 0.30,
        'requires_flag': 'desert_entered'
    },

    # === Post-Game ===

    'slaver_ship': {
        'name': 'Slaver Ship',
        'description': 'Captain Donald\'s ship.',
        'spawn_position': [128, 112],
        'fast_travel': False,
        'encounter_rate': 0.0,
        'requires_flag': 'game_completed'
    }
}

# Location NPCs
LOCATION_NPCS = {
    'imperial_city': {
        'guard_1': {
            'name': 'Guard',
            'position': [60, 100],
            'dialogue_id': 'guard_generic',
            'sprite': 'guard'
        },
        'magic_shop_owner': {
            'name': 'Mage',
            'position': [180, 100],
            'shop_id': 'imperial_magic_shop',
            'sprite': 'mage'
        },
        'weapon_shop_owner': {
            'name': 'Blacksmith',
            'position': [180, 140],
            'shop_id': 'imperial_weapon_shop',
            'sprite': 'blacksmith'
        },
        'inn_keeper': {
            'name': 'Inn Keeper',
            'position': [60, 140],
            'dialogue_id': 'inn_keeper',
            'sprite': 'inn_keeper'
        }
    },

    'imperial_city_inn': {
        'fritzzit': {
            'name': 'Fritzzit',
            'position': [100, 100],
            'recruitable': True,
            'character_id': 'fritzzit',
            'sprite': 'goblin'
        },
        'crankpot': {
            'name': 'Crankpot',
            'position': [120, 100],
            'recruitable': True,
            'character_id': 'crankpot',
            'sprite': 'goblin'
        },
        'cookie': {
            'name': 'Cookie',
            'position': [140, 120],
            'recruitable': True,
            'character_id': 'cookie',
            'sprite': 'halfling'
        },
        'iris': {
            'name': 'Iris',
            'position': [160, 120],
            'recruitable': True,
            'character_id': 'iris',
            'sprite': 'halfling'
        }
    },

    'army_camp': {
        'quartermaster': {
            'name': 'Quartermaster',
            'position': [128, 100],
            'shop_id': 'army_camp_shop',
            'sprite': 'soldier'
        },
        'warghoul': {
            'name': 'Warghoul',
            'position': [80, 120],
            'recruitable': True,
            'character_id': 'warghoul',
            'sprite': 'ghoul'
        }
    },

    'desert_outpost': {
        'merchant': {
            'name': 'Desert Trader',
            'position': [128, 100],
            'shop_id': 'desert_item_shop',
            'sprite': 'merchant'
        }
    }
}

# Location triggers (doors, warps, etc.)
LOCATION_TRIGGERS = {
    'imperial_city': {
        'inn_door': {
            'position': [60, 140],
            'size': [16, 16],
            'type': 'door',
            'target_location': 'imperial_city_inn'
        },
        'magic_shop_door': {
            'position': [180, 100],
            'size': [16, 16],
            'type': 'door',
            'target_location': 'imperial_magic_shop'
        },
        'weapon_shop_door': {
            'position': [180, 140],
            'size': [16, 16],
            'type': 'door',
            'target_location': 'imperial_weapon_shop'
        },
        'cathedral_door': {
            'position': [128, 60],
            'size': [16, 16],
            'type': 'door',
            'target_location': 'imperial_cathedral'
        }
    },

    'surface_forest': {
        'warren_entrance': {
            'position': [128, 220],
            'size': [16, 16],
            'type': 'warp',
            'target_location': 'post_imperial_warren'
        },
        'city_path': {
            'position': [240, 112],
            'size': [16, 32],
            'type': 'warp',
            'target_location': 'imperial_city'
        }
    }
}


def get_location_npcs(location_id):
    """Get NPCs at location"""
    return LOCATION_NPCS.get(location_id, {})


def get_location_triggers(location_id):
    """Get triggers at location"""
    return LOCATION_TRIGGERS.get(location_id, {})
