"""
Key Item system with locations, cutscene triggers, and sidequest requirements
Key items cannot be sold or destroyed once obtained
"""

# Key item definitions
KEY_ITEMS = {
    # Javin's Key Item
    'baby_dragon': {
        'name': 'Baby Dragon',
        'character': 'javin',
        'optional': True,  # Can miss in tutorial
        'description': 'A baby dragon you saved from the infected warren. Chirps happily when near you.',
        'hint': 'Perhaps this dragon could help me in battle if I learn to bond with it...',
        'location_type': 'tutorial_optional',
        'location': 'tutorial_warren_escape',
        'trigger_event': 'tutorial_baby_dragon_save',
        'effect': 'Equippable by Javin only - Dragon attacks every 4th turn',
        'sidequest_requirement': True,
        'evolution_unlocks': 'dreamwalker',
        'new_game_plus_reminder': True,  # Javin reminds player if not obtained
        'introduces_key_item_system': True  # Tutorial trigger
    },

    # Michael's Key Item (ONLY REQUIRED KEY ITEM)
    'sentimental_travelers_pouch': {
        'name': "Sentimental Traveler's Pouch",
        'character': 'michael',
        'optional': False,  # Story-given, cannot miss
        'description': 'A worn leather pouch that Michael carries. Contains mementos from his travels.',
        'hint': 'This pouch has seen many adventures. Perhaps it could unlock more power...',
        'location_type': 'story_given',
        'location': 'imperial_city_michael_recruitment',
        'trigger_event': 'michael_joins_party',
        'effect': 'Required for Michael to evolve into Paladin',
        'sidequest_requirement': True,
        'evolution_unlocks': 'paladin',
        'guaranteed': True  # Cannot be missed
    },

    # Frostbite's Key Item
    'shotgun_blueprint': {
        'name': 'Shotgun Blueprint',
        'character': 'frostbite',
        'optional': False,  # Must purchase
        'description': 'Detailed blueprints for crafting an ultimate shotgun. Smells of gunpowder.',
        'hint': 'With these plans, I could forge the most powerful shotgun ever created...',
        'location_type': 'purchasable',
        'location': 'imperial_city_weapon_shop',
        'purchase_cost': 5000,
        'trigger_event': 'purchase_from_shop',
        'effect': 'Unlocks Ultimate Shotgun sidequest for Frostbite, level cap 75->99',
        'sidequest_requirement': True,
        'evolution_unlocks': 'ultimate_shotgun',
        'level_cap_increase': True  # 75 -> 99 upon getting weapon
    },

    # Fritzzit's Key Item
    'sniper_rifle_blueprint': {
        'name': 'Sniper Rifle Blueprint',
        'character': 'fritzzit',
        'optional': False,  # Must purchase
        'description': 'Precise schematics for an legendary sniper rifle. Pages are worn from study.',
        'hint': 'This weapon could make me the deadliest sniper alive...',
        'location_type': 'purchasable',
        'location': 'imperial_city_weapon_shop',
        'purchase_cost': 5000,
        'trigger_event': 'purchase_from_shop',
        'effect': 'Unlocks Ultimate Sniper Rifle sidequest for Fritzzit, level cap 75->99',
        'sidequest_requirement': True,
        'evolution_unlocks': 'ultimate_sniper_rifle',
        'level_cap_increase': True
    },

    # Fei's Key Item
    'grizzly_bear_skull': {
        'name': 'Grizzly Bear Skull',
        'character': 'fei',
        'optional': False,
        'description': 'The massive skull of an ancient grizzly bear. Radiates primal strength.',
        'hint': 'Warriors of old wore these as helms to channel the bear\'s ferocity...',
        'location_type': 'static',
        'location': 'pre_orisia_accessible_area',  # Static spawn before Orisia
        'trigger_event': None,
        'effect': 'Fei wears skull as helmet when evolving to Weapon Master',
        'sidequest_requirement': True,
        'evolution_unlocks': 'weapon_master',
        'visual_change': 'bear_skull_helmet_icon'
    },

    # Warghoul's Key Item
    'orc_funeral_totem': {
        'name': 'Orc Funeral Totem',
        'character': 'warghoul',
        'optional': False,
        'description': 'A carved totem used in orc funeral rites. Still hums with ancestral power.',
        'hint': 'This totem could help me command the spirits of fallen warriors...',
        'location_type': 'static',
        'location': 'undead_lands_orc_village',
        'trigger_event': None,
        'effect': 'Unlocks Deathknight evolution and skeleton summoning',
        'sidequest_requirement': True,
        'evolution_unlocks': 'deathknight'
    },

    # Cookie's Key Item
    'crown_of_flowers': {
        'name': 'Crown of Flowers',
        'character': 'cookie',
        'optional': False,
        'description': 'A pristine crown of wildflowers that never wilts. Keeps fungal rot at bay.',
        'hint': 'This crown pulses with nature\'s purest magic. It could enhance my druidic powers...',
        'location_type': 'static_with_cutscene',
        'location': 'route_to_jerods_house',
        'trigger_event': 'cookie_crown_comment',
        'cutscene_required': True,
        'cutscene_trigger': {
            'character_in_party': 'cookie',
            'cookie_dialogue': "There's an item over there that appears to be keeping the fungal rot away from it.",
            'becomes_lootable_after': True,
            'always_lootable_if_cookie_not_recruited': True
        },
        'effect': 'Unlocks Druidess evolution and powerful control spells',
        'sidequest_requirement': True,
        'evolution_unlocks': 'druidess'
    },

    # Iris's Key Item
    'tuft_of_panda_fur': {
        'name': 'Tuft of Panda Fur',
        'character': 'iris',
        'optional': False,
        'description': 'Soft, black and white fur from Fei. Iris treasures it deeply.',
        'hint': 'This fur reminds me of Fei. Perhaps it could help me transform...',
        'location_type': 'cutscene_unlock',
        'location': 'inn_after_halfling_rescue',
        'trigger_event': 'fei_grooming_cutscene',
        'cutscene_required': True,
        'cutscene_trigger': {
            'after_event': 'cookie_iris_rescue_or_recruitment',
            'at_location': 'inn_or_rest_point',
            'cutscene_sequence': [
                "Fei brushes his fur",
                'Fei: "It\'s so hard to get mats out after a fight."',
                "Fei places brush on table/dresser",
                'Iris fawns over it',
                'Iris: "I want to touch it so badly..."',
                "Tuft of Panda Fur becomes lootable from table/dresser"
            ]
        },
        'effect': 'Unlocks Shapeshifter evolution and Panda Form',
        'sidequest_requirement': True,
        'evolution_unlocks': 'shapeshifter'
    },

    # Crankpot's Key Item
    'molotov_cocktail': {
        'name': 'Molotov Cocktail',
        'character': 'crankpot',
        'optional': False,
        'description': 'A bottle filled with flammable liquid and a rag fuse. Smells dangerous.',
        'hint': 'This reminds me of... simpler times. Before the flames consumed everything.',
        'location_type': 'static',
        'location': 'pre_orisia_accessible_area',
        'trigger_event': None,
        'effect': 'Unlocks Arsonist evolution and Burn spread mechanic',
        'sidequest_requirement': True,
        'evolution_unlocks': 'arsonist',
        'ptsd_reference': True  # Crankpot's backstory
    },

    # Yipp's Key Items (BOTH REQUIRED)
    'holy_symbol': {
        'name': 'Holy Symbol',
        'character': 'yipp',
        'optional': False,
        'description': 'A blessed silver pendant depicting a radiant sun. Warm to the touch.',
        'hint': 'This holy relic could guide me toward the light... or away from it.',
        'location_type': 'random_dungeon_pre_orisia',
        'location': 'yipp_random_dungeon_spawn_alternatives',
        'trigger_event': None,
        'constraint': 'pre_orisia_only',  # CRITICAL
        'spawns_in': 'dungeons_where_yipp_could_spawn_but_didnt',
        'effect': 'One of two items required for Yipp alignment choice',
        'sidequest_requirement': True,
        'both_required_with': 'empty_pewter_wine_glass',
        'alignment_choice': 'saint_or_vampire'
    },

    'empty_pewter_wine_glass': {
        'name': 'Empty Pewter Wine Glass',
        'character': 'yipp',
        'optional': False,
        'description': 'An elegant but empty wine glass made of dark pewter. Faintly smells of iron.',
        'hint': 'This glass thirsts for something... something red. Blood? Or wine?',
        'location_type': 'random_dungeon_pre_orisia',
        'location': 'yipp_random_dungeon_spawn_alternatives',
        'trigger_event': None,
        'constraint': 'pre_orisia_only',  # CRITICAL
        'spawns_in': 'dungeons_where_yipp_could_spawn_but_didnt',
        'effect': 'One of two items required for Yipp alignment choice',
        'sidequest_requirement': True,
        'both_required_with': 'holy_symbol',
        'alignment_choice': 'saint_or_vampire'
    }
}

# Key item location tracking and logic
KEY_ITEM_LOCATIONS = {
    # Static locations (same every playthrough)
    'tutorial_warren_escape': {
        'type': 'optional_event',
        'item': 'baby_dragon',
        'trigger': 'player_chooses_to_save_dragon',
        'can_miss': True,
        'new_game_plus_reminder': 'javin_hears_dragon_before_leaving'
    },

    'imperial_city_michael_recruitment': {
        'type': 'story_guaranteed',
        'item': 'sentimental_travelers_pouch',
        'trigger': 'michael_joins_party',
        'can_miss': False
    },

    'imperial_city_weapon_shop': {
        'type': 'purchasable',
        'items': ['shotgun_blueprint', 'sniper_rifle_blueprint'],
        'cost': 5000,  # Each
        'can_miss': True,
        'available_window': 'any_time_after_first_visit'
    },

    'undead_lands_orc_village': {
        'type': 'static_spawn',
        'item': 'orc_funeral_totem',
        'exact_location': 'abandoned_orc_village_chest',
        'can_miss': False
    },

    'route_to_jerods_house': {
        'type': 'static_with_cutscene',
        'item': 'crown_of_flowers',
        'cutscene_character': 'cookie',
        'lootable_condition': 'after_cookie_comment_or_cookie_not_in_party',
        'can_miss': False
    },

    'inn_after_halfling_rescue': {
        'type': 'cutscene_unlock',
        'item': 'tuft_of_panda_fur',
        'cutscene': 'fei_grooming',
        'lootable_from': 'table_or_dresser_after_cutscene',
        'can_miss': False
    },

    'pre_orisia_area_1': {
        'type': 'static_spawn',
        'items': ['grizzly_bear_skull', 'molotov_cocktail'],
        'accessible_before': 'orisia_meeting',
        'can_miss': False
    },

    # Randomized locations (different each playthrough)
    'yipp_random_dungeons': {
        'type': 'randomized_pre_orisia',
        'items': ['holy_symbol', 'empty_pewter_wine_glass'],
        'constraint': 'pre_orisia_dungeons_only',
        'logic': 'spawn_in_dungeons_where_yipp_could_spawn_but_didnt',
        'yipp_spawn': 'one_random_dungeon',
        'key_items_spawn': 'other_eligible_dungeons',
        'can_miss': True,
        'deadline': 'orisia_meeting'
    }
}

# Cutscene data for key items
KEY_ITEM_CUTSCENES = {
    'baby_dragon_save': {
        'location': 'tutorial_warren',
        'trigger': 'player_investigates_crying_sound',
        'sequence': [
            'Player hears baby dragon crying',
            'Optional: Go to save it or leave',
            'If saved: Baby dragon joins as key item',
            'Tutorial explanation of key item system'
        ],
        'new_game_plus_variant': {
            'javin_dialogue': 'I hear a baby dragon... I should save it this time.',
            'condition': 'baby_dragon_not_saved_in_previous_playthrough'
        }
    },

    'cookie_crown_comment': {
        'location': 'route_to_jerods_house',
        'trigger': 'party_walks_near_crown_of_flowers',
        'requires_character': 'cookie',
        'sequence': [
            'Party approaches Crown of Flowers',
            'Cookie: "There\'s an item over there that appears to be keeping the fungal rot away from it."',
            'Crown of Flowers becomes lootable',
            'Player can pick it up'
        ],
        'no_cookie_variant': {
            'always_lootable': True,
            'no_dialogue': True
        }
    },

    'fei_grooming': {
        'location': 'inn_or_rest_point',
        'trigger': 'after_cookie_iris_rescue_or_recruitment',
        'sequence': [
            'Cutscene starts at inn/rest point',
            'Fei is grooming his panda fur with a brush',
            'Fei: "It\'s so hard to get mats out after a fight."',
            'Fei places brush on table/dresser',
            'Camera focuses on Iris',
            'Iris is visibly fawning over the brush',
            'Iris: "I want to touch it so badly..."',
            'Cutscene ends',
            'Tuft of Panda Fur now lootable from table/dresser'
        ]
    },

    'yipp_dungeon_encounter': {
        'location': 'random_pre_orisia_dungeon',
        'trigger': 'party_enters_room',
        'randomized': True,
        'sequence': [
            'Party walks into room',
            'Yipp is fighting undead enemies and losing',
            'Battle starts with Yipp as NPC ally',
            'Party helps defeat enemies',
            'After battle, Yipp asks to join',
            'If declined: Yipp moves to Imperial City magic shop',
            'If accepted: Yipp joins party'
        ],
        'new_game_plus_variant': {
            'frostbite_dialogue': 'Why does this smell like dead rat?',
            'condition': 'this_was_yipp_spawn_location_last_playthrough'
        }
    }
}

# Orisia sidequest requirements
ORISIA_SIDEQUESTS = {
    'javin_dreamwalker': {
        'character': 'javin',
        'requires_key_item': ['baby_dragon'],
        'orisia_dialogue': 'Your bond with that dragon is strong. I can help you unlock its full potential.',
        'reward': 'Dreamwalker class evolution',
        'effects': ['psychic_spells', 'level_cap_99']
    },

    'frostbite_ultimate_shotgun': {
        'character': 'frostbite',
        'requires_key_item': ['shotgun_blueprint'],
        'orisia_dialogue': 'With these blueprints, I can forge you the ultimate weapon.',
        'reward': 'Ultimate Shotgun',
        'effects': ['double_attack', 'level_cap_99', 'best_in_slot_weapon']
    },

    'fei_weapon_master': {
        'character': 'fei',
        'requires_key_item': ['grizzly_bear_skull'],
        'orisia_dialogue': 'That skull carries the spirit of the berserker. Wear it and master all weapons.',
        'reward': 'Weapon Master class evolution',
        'effects': ['dual_wield', 'double_attack', 'lose_shield', 'bear_skull_helmet', 'level_cap_99']
    },

    'michael_paladin': {
        'character': 'michael',
        'requires_key_item': ['sentimental_travelers_pouch'],
        'orisia_dialogue': 'Your travels have prepared you for a greater calling. Become a paladin.',
        'reward': 'Paladin class evolution',
        'effects': ['keep_all_cleric_spells', 'plate_armor', 'auto_taunt', 'raise_spell', 'level_cap_99']
    },

    'hannah_magus': {
        'character': 'hannah',
        'requires_key_item': None,  # No key item needed
        'orisia_dialogue': 'Your raw magical talent is exceptional. I will teach you the ways of the Magus.',
        'reward': 'Magus class evolution',
        'effects': ['double_damage', 'multi_target', 'level_cap_99']
    },

    'warghoul_deathknight': {
        'character': 'warghoul',
        'requires_key_item': ['orc_funeral_totem'],
        'orisia_dialogue': 'That totem binds you to the spirits. Use it to command the undead.',
        'reward': 'Deathknight class evolution',
        'effects': ['summon_skeletons', 'level_cap_99']
    },

    'cookie_druidess': {
        'character': 'cookie',
        'requires_key_item': ['crown_of_flowers'],
        'orisia_dialogue': 'That crown connects you to nature\'s purest essence. Become a true druidess.',
        'reward': 'Druidess class evolution',
        'effects': ['control_spells', 'sensory_deprivation', 'level_cap_99']
    },

    'iris_shapeshifter': {
        'character': 'iris',
        'requires_key_item': ['tuft_of_panda_fur'],
        'orisia_dialogue': 'Your bond with Fei runs deep. Use it to unlock your shapeshifting potential.',
        'reward': 'Shapeshifter class evolution',
        'effects': ['panda_form', 'triple_attack', 'fei_bonus', 'improved_berserk', 'level_cap_99']
    },

    'fritzzit_ultimate_sniper': {
        'character': 'fritzzit',
        'requires_key_item': ['sniper_rifle_blueprint'],
        'orisia_dialogue': 'These plans are masterful. Let me craft you the perfect weapon.',
        'reward': 'Ultimate Sniper Rifle',
        'effects': ['instant_kill_crits', 'increased_crit_chance', 'level_cap_99', 'best_in_slot_weapon']
    },

    'crankpot_arsonist': {
        'character': 'crankpot',
        'requires_key_item': ['molotov_cocktail'],
        'orisia_dialogue': 'You\'ve embraced the flame. Let me show you how to truly master fire.',
        'reward': 'Arsonist class evolution',
        'effects': ['burn_status', 'burn_spread_15_percent', 'level_cap_99']
    },

    'yipp_alignment_choice': {
        'character': 'yipp',
        'requires_key_item': ['holy_symbol', 'empty_pewter_wine_glass'],  # BOTH required
        'both_items_required': True,
        'orisia_dialogue': 'You carry both light and darkness. You must choose your path.',
        'choice': True,
        'options': {
            'saint': {
                'dialogue': 'I choose the light. I will atone for my past.',
                'reward': 'Saint class evolution',
                'effects': ['holy_spells', 'mass_heal', 'resurrect', 'level_cap_99'],
                'ending_requirement': 'best_ending',
                'final_battle': 'fights_with_party'
            },
            'vampire': {
                'dialogue': 'The darkness calls to me. I embrace it.',
                'reward': 'Vampire class evolution',
                'effects': ['drain_life', 'blood_mist', 'undead_control', 'level_cap_99'],
                'ending_lock': 'bad_ending_only',
                'final_battle': 'betrays_party'
            }
        }
    },

    'flood_no_sidequest': {
        'character': 'flood',
        'requires_key_item': None,
        'has_sidequest': False,
        'orisia_dialogue': "She's already as powerful as she will ever be.",
        'orisia_comment_condition': 'all_other_sidequests_completed',
        'foreshadows': 'flood_permanent_death'
    }
}

def is_key_item_missable(item_id):
    """Check if a key item can be missed"""
    item = KEY_ITEMS.get(item_id)
    if not item:
        return False

    if item.get('guaranteed'):
        return False

    location = item.get('location_type')
    if location in ['story_given', 'cutscene_unlock', 'static_with_cutscene']:
        return False

    return True

def get_key_item_hint(item_id):
    """Get the hint text for a key item"""
    item = KEY_ITEMS.get(item_id)
    if not item:
        return ""

    return item.get('hint', '')

def check_sidequest_requirements(character_id, key_items_possessed):
    """
    Check if character has required key items for sidequest

    Args:
        character_id: Character identifier
        key_items_possessed: List of key item IDs the player has

    Returns:
        bool: True if requirements met
    """
    sidequest = ORISIA_SIDEQUESTS.get(f'{character_id}_sidequest')
    if not sidequest:
        # Check for special naming
        for quest_id, quest_data in ORISIA_SIDEQUESTS.items():
            if quest_data.get('character') == character_id:
                sidequest = quest_data
                break

    if not sidequest:
        return False

    if not sidequest.get('has_sidequest', True):
        return False

    required_items = sidequest.get('requires_key_item')
    if not required_items:
        return True  # No key items required (Hannah)

    if isinstance(required_items, list):
        # Check if ALL items are possessed (Yipp case)
        return all(item in key_items_possessed for item in required_items)

    return required_items in key_items_possessed
