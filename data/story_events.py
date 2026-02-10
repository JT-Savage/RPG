"""
Story Events Data
All story events, triggers, and cutscenes
"""

# Main story events database
STORY_EVENTS = {
    # === Tutorial & Opening ===

    'intro_cutscene': {
        'name': 'Opening Cutscene',
        'dialogue_id': 'intro_tutorial',
        'one_time': True,
        'effects': {
            'set_flags': {
                'game_started': True,
                'in_tutorial': True
            }
        }
    },

    'warren_escape': {
        'name': 'Warren Escape',
        'dialogue_id': 'warren_escape',
        'required_flags': ['tutorial_battle'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'warren_escaped': True,
                'kobolds_released': True,
                'tutorial_completed': True
            },
            'unlock_locations': ['surface_forest', 'imperial_city']
        }
    },

    # === Imperial City ===

    'imperial_city_arrival': {
        'name': 'Imperial City Arrival',
        'dialogue_id': 'imperial_city_arrival',
        'one_time': True,
        'effects': {
            'set_flags': {
                'imperial_city_visited': True
            },
            'unlock_locations': ['imperial_magic_shop', 'imperial_weapon_shop']
        }
    },

    # === Major Story Beats ===

    'fei_death_iris_berserk': {
        'name': 'Fei\'s Death',
        'dialogue_id': 'fei_death_iris_berserk',
        'required_characters': ['fei', 'iris'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'fei_died': True,
                'iris_berserk_triggered': True
            },
            'trigger_iris_berserk': True
        }
    },

    'iris_berserk_end': {
        'name': 'Iris Calms Down',
        'dialogue_id': 'iris_berserk_end',
        'required_flags': ['iris_berserk_triggered'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'iris_berserk_ended': True
            }
        }
    },

    'flood_sacrifice': {
        'name': 'Flood\'s Sacrifice',
        'dialogue_id': 'flood_sacrifice',
        'required_characters': ['flood'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'flood_sacrificed': True,
                'flood_dead': True
            },
            'kill_character': 'flood'
        }
    },

    # === Recruitment Deadline ===

    'orisia_desert_warning': {
        'name': 'Orisia Meeting',
        'dialogue_id': 'orisia_desert_warning',
        'one_time': True,
        'effects': {
            'set_flags': {
                'met_orisia': True,
                'orisia_ready_warning_given': True
            }
        }
    },

    'recruitment_deadline_passed': {
        'name': 'Recruitment Window Closed',
        'required_flags': ['desert_entered'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'recruitment_deadline_passed': True
            }
        }
    },

    # === Yipp Arc ===

    'yipp_dungeon_encounter': {
        'name': 'Yipp Rescue',
        'dialogue_id': 'recruit_yipp',
        'forbidden_flags': ['met_orisia', 'yipp_encountered'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'yipp_encountered': True
            }
        }
    },

    'yipp_alignment_choice': {
        'name': 'Yipp\'s Choice',
        'dialogue_id': 'yipp_alignment_choice',
        'required_characters': ['yipp'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'yipp_alignment_chosen': True
            }
        }
    },

    # === Queen Kella Arc ===

    'kella_first_meeting': {
        'name': 'Meeting Queen Kella',
        'dialogue_id': 'kella_first_meeting',
        'required_flags': ['imperial_city_visited'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'met_kella': True
            },
            'grant_gil': 1000
        }
    },

    'kella_infected': {
        'name': 'Infected Kella',
        'dialogue_id': 'kella_infected',
        'required_flags': ['desert_entered', 'met_kella'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'kella_infected_found': True
            },
            'trigger_battle': 'secret_boss_kella'
        }
    },

    # === Final Battle ===

    'final_boss_intro': {
        'name': 'Final Confrontation',
        'dialogue_id': 'final_boss_intro',
        'required_flags': ['desert_entered'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'final_boss_triggered': True
            },
            'trigger_battle': 'final_boss'
        }
    },

    'necromancer_defeated': {
        'name': 'Victory!',
        'required_flags': ['final_boss_defeated'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'necromancer_defeated': True,
                'game_completed': True
            }
        }
    },

    # === Post-Credits ===

    'captain_donald_reveal': {
        'name': 'Captain Donald',
        'dialogue_id': 'captain_donald_reveal',
        'required_flags': ['game_completed'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'captain_donald_encountered': True
            },
            'trigger_battle': 'post_credits_boss'
        }
    },

    'game_ending': {
        'name': 'The End',
        'dialogue_id': 'game_ending_good',
        'required_flags': ['necromancer_defeated'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'ending_seen': True
            }
        }
    },

    # === Class Evolution Events ===

    'frostbite_class_evolution': {
        'name': 'Frostbite Evolves',
        'required_characters': ['frostbite'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'frostbite_evolved': True
            }
        }
    },

    'fei_class_evolution': {
        'name': 'Fei Evolves',
        'required_characters': ['fei'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'fei_evolved': True
            }
        }
    },

    'iris_class_evolution': {
        'name': 'Iris Evolves',
        'required_characters': ['iris'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'iris_evolved': True
            }
        }
    },

    # Add more evolution events for other characters...

    # === Side Quests ===

    'baby_dragon_quest_start': {
        'name': 'Lost Dragon Cub',
        'required_characters': ['javin'],
        'one_time': True,
        'effects': {
            'start_quests': ['baby_dragon_quest']
        }
    },

    'baby_dragon_quest_complete': {
        'name': 'Dragon Reunited',
        'required_flags': ['baby_dragon_found'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'baby_dragon_quest_completed': True
            },
            'grant_key_items': ['baby_dragon']
        }
    },

    'jerod_house_quest': {
        'name': 'Investigate Jerod\'s House',
        'one_time': True,
        'effects': {
            'start_quests': ['jerod_investigation']
        }
    },

    'jerod_house_explosion': {
        'name': 'House Explosion',
        'required_flags': ['jerod_house_entered'],
        'one_time': True,
        'effects': {
            'set_flags': {
                'jerod_house_exploded': True,
                'fungal_enemies_removed': True
            },
            'trigger_battle': 'jerod_boss'
        }
    }
}

# Events triggered by entering locations
LOCATION_EVENTS = {
    'imperial_city': ['imperial_city_arrival'],
    'desert_region': ['recruitment_deadline_passed'],
    'necromancer_sanctum': ['final_boss_intro'],
    'capitol_ruins': ['kella_infected'],
    'jerod_house': ['jerod_house_quest'],
    'throne_room': ['kella_first_meeting']
}

# Events triggered by story flags
FLAG_TRIGGERED_EVENTS = {
    'warren_escape': {
        'trigger_flag': 'tutorial_battle',
        'required_flags': []
    },
    'iris_berserk_end': {
        'trigger_flag': 'fei_revived',
        'required_flags': ['iris_berserk_triggered']
    },
    'necromancer_defeated': {
        'trigger_flag': 'final_boss_defeated',
        'required_flags': []
    }
}

# Quest database
QUESTS = {
    'baby_dragon_quest': {
        'name': 'Lost Dragon Cub',
        'description': 'Help Javin find the lost baby dragon.',
        'objectives': [
            'Search the volcanic caves',
            'Defeat the dragon poachers',
            'Return the baby dragon to its mother'
        ],
        'rewards': {
            'gil': 500,
            'exp': 1000,
            'key_items': ['baby_dragon']
        },
        'completion_event': 'baby_dragon_quest_complete'
    },

    'jerod_investigation': {
        'name': 'Investigate Jerod\'s House',
        'description': 'Something strange is happening at Jerod\'s house.',
        'objectives': [
            'Enter Jerod\'s house',
            'Investigate the basement',
            'Defeat Jerod'
        ],
        'rewards': {
            'gil': 1000,
            'exp': 2000,
            'items': {
                'elixir': 2
            }
        },
        'completion_event': 'jerod_house_explosion'
    },

    'kella_quest': {
        'name': 'Find Queen Kella',
        'description': 'Queen Kella has gone missing. Find her.',
        'objectives': [
            'Search the capitol ruins',
            'Confront infected Kella',
            'Defeat her to grant mercy'
        ],
        'rewards': {
            'gil': 5000,
            'exp': 10000,
            'items': {
                'megalixir': 1
            }
        },
        'completion_event': 'kella_infected'
    }
}
