"""
Dungeon Data
All dungeons and their layouts
"""

DUNGEONS = {
    # === Story Dungeons ===

    'tutorial_warren': {
        'name': 'Kobold Warren',
        'num_floors': 1,
        'random_layout': False,
        'encounter_table': 'tutorial_warren',
        'encounter_rate': 0.15,
        'boss': None,  # Tutorial, no boss
        'layout': {
            'floors': [
                {
                    'floor': 1,
                    'rooms': [
                        {
                            'id': 'start',
                            'type': 'start',
                            'connections': ['tunnel_1']
                        },
                        {
                            'id': 'tunnel_1',
                            'type': 'corridor',
                            'connections': ['start', 'first_battle']
                        },
                        {
                            'id': 'first_battle',
                            'type': 'battle',
                            'connections': ['tunnel_1', 'exit']
                        },
                        {
                            'id': 'exit',
                            'type': 'exit',
                            'connections': ['first_battle']
                        }
                    ]
                }
            ]
        }
    },

    'post_imperial_warren': {
        'name': 'Infected Warren',
        'num_floors': 2,
        'random_layout': False,
        'encounter_table': 'post_imperial_warren',
        'encounter_rate': 0.30,
        'boss': 'warren_boss',
        'layout': {
            'floors': [
                {
                    'floor': 1,
                    'rooms': [
                        {'id': 'entrance', 'type': 'start', 'connections': ['hall_1']},
                        {'id': 'hall_1', 'type': 'corridor', 'connections': ['entrance', 'hall_2']},
                        {'id': 'hall_2', 'type': 'corridor', 'connections': ['hall_1', 'stairs']},
                        {'id': 'stairs', 'type': 'stairs', 'connections': ['hall_2'], 'leads_to': 2}
                    ]
                },
                {
                    'floor': 2,
                    'rooms': [
                        {'id': 'lower_hall', 'type': 'corridor', 'connections': ['boss_room']},
                        {'id': 'boss_room', 'type': 'boss', 'connections': ['lower_hall'], 'boss': 'warren_boss'}
                    ]
                }
            ]
        }
    },

    'catacombs': {
        'name': 'Ancient Catacombs',
        'num_floors': 3,
        'random_layout': False,
        'encounter_table': 'catacombs',
        'encounter_rate': 0.30,
        'boss': 'catacombs_boss',
        'layout': {
            'floors': [
                {
                    'floor': 1,
                    'rooms': [
                        {'id': 'entrance', 'type': 'start'},
                        {'id': 'tomb_1', 'type': 'room'},
                        {'id': 'tomb_2', 'type': 'room'},
                        {'id': 'stairs_1', 'type': 'stairs', 'leads_to': 2}
                    ]
                },
                {
                    'floor': 2,
                    'rooms': [
                        {'id': 'hall', 'type': 'corridor'},
                        {'id': 'crypt', 'type': 'room'},
                        {'id': 'stairs_2', 'type': 'stairs', 'leads_to': 3}
                    ]
                },
                {
                    'floor': 3,
                    'rooms': [
                        {'id': 'boss_hall', 'type': 'corridor'},
                        {'id': 'boss_room', 'type': 'boss', 'boss': 'catacombs_boss'}
                    ]
                }
            ]
        }
    },

    'jerod_house': {
        'name': 'Jerod\'s House',
        'num_floors': 2,
        'random_layout': False,
        'encounter_table': 'jerod_house',
        'encounter_rate': 0.20,
        'boss': 'jerod',
        'layout': {
            'floors': [
                {
                    'floor': 1,
                    'rooms': [
                        {'id': 'living_room', 'type': 'start'},
                        {'id': 'kitchen', 'type': 'room'},
                        {'id': 'basement_stairs', 'type': 'stairs', 'leads_to': 2}
                    ]
                },
                {
                    'floor': 2,
                    'rooms': [
                        {'id': 'basement', 'type': 'room'},
                        {'id': 'lab', 'type': 'boss', 'boss': 'jerod'}
                    ]
                }
            ]
        }
    },

    'necromancer_sanctum': {
        'name': 'Necromancer\'s Sanctum',
        'num_floors': 4,
        'random_layout': False,
        'encounter_table': 'necromancer_sanctum',
        'encounter_rate': 0.30,
        'boss': 'necromancer_lich',
        'layout': {
            'floors': [
                {
                    'floor': 1,
                    'rooms': [
                        {'id': 'entrance_hall', 'type': 'start'},
                        {'id': 'corridor_1', 'type': 'corridor'},
                        {'id': 'stairs_1', 'type': 'stairs', 'leads_to': 2}
                    ]
                },
                {
                    'floor': 2,
                    'rooms': [
                        {'id': 'ritual_room', 'type': 'room'},
                        {'id': 'stairs_2', 'type': 'stairs', 'leads_to': 3}
                    ]
                },
                {
                    'floor': 3,
                    'rooms': [
                        {'id': 'throne_room', 'type': 'room'},
                        {'id': 'stairs_3', 'type': 'stairs', 'leads_to': 4}
                    ]
                },
                {
                    'floor': 4,
                    'rooms': [
                        {'id': 'sanctum', 'type': 'boss', 'boss': 'necromancer_lich'}
                    ]
                }
            ]
        }
    },

    # === Random Dungeons (for Yipp spawn) ===

    'dungeon_1': {
        'name': 'Forgotten Tomb',
        'num_floors': 3,
        'random_layout': True,
        'rooms_per_floor': 5,
        'encounter_table': 'undead_lands',
        'encounter_rate': 0.25,
        'can_spawn_yipp': True
    },

    'dungeon_2': {
        'name': 'Abandoned Mine',
        'num_floors': 3,
        'random_layout': True,
        'rooms_per_floor': 5,
        'encounter_table': 'undead_lands',
        'encounter_rate': 0.25,
        'can_spawn_yipp': True
    },

    'dungeon_3': {
        'name': 'Cursed Ruins',
        'num_floors': 3,
        'random_layout': True,
        'rooms_per_floor': 5,
        'encounter_table': 'undead_lands',
        'encounter_rate': 0.25,
        'can_spawn_yipp': True
    },

    'dungeon_4': {
        'name': 'Dark Cavern',
        'num_floors': 3,
        'random_layout': True,
        'rooms_per_floor': 5,
        'encounter_table': 'undead_lands',
        'encounter_rate': 0.25,
        'can_spawn_yipp': True
    },

    'dungeon_5': {
        'name': 'Haunted Monastery',
        'num_floors': 3,
        'random_layout': True,
        'rooms_per_floor': 5,
        'encounter_table': 'undead_lands',
        'encounter_rate': 0.25,
        'can_spawn_yipp': True
    }
}

# Boss encounters by dungeon
DUNGEON_BOSSES = {
    'warren_boss': {
        'enemy_id': 'infected_overseer',
        'dialogue_before': 'warren_boss_intro',
        'dialogue_after': 'warren_boss_defeated'
    },

    'catacombs_boss': {
        'enemy_id': 'ancient_lich',
        'dialogue_before': 'catacombs_boss_intro',
        'dialogue_after': 'catacombs_boss_defeated'
    },

    'jerod': {
        'enemy_id': 'jerod_fungal',
        'dialogue_before': 'jerod_reveal',
        'dialogue_after': 'jerod_house_explosion'
    },

    'necromancer_lich': {
        'enemy_id': 'necromancer_lich',
        'dialogue_before': 'final_boss_intro',
        'dialogue_after': 'necromancer_defeated'
    }
}


def get_yipp_spawn_dungeons():
    """Get list of dungeons that can spawn Yipp"""
    return [
        'dungeon_1',
        'dungeon_2',
        'dungeon_3',
        'dungeon_4',
        'dungeon_5'
    ]


def select_random_yipp_dungeon():
    """Select random dungeon for Yipp spawn"""
    import random
    dungeons = get_yipp_spawn_dungeons()
    return random.choice(dungeons)
