"""
Character class definitions and progression data
All 12 recruitable characters with evolution paths
"""

# Character class definitions with base stats and growth rates
CHARACTERS = {
    # Required Characters
    'javin': {
        'name': 'Javin',
        'starting_class': 'claw_noble',
        'evolved_class': 'dreamwalker',
        'required': True,
        'initial_level': 1,
        'base_stats': {
            'hp': 40,
            'mp': 5,
            'attack': 12,
            'defense': 8,
            'magic_power': 4,
            'spell_resistance': 6,
            'speed': 14
        },
        'growth_rates': {
            'hp': 4.5,
            'mp': 0.8,
            'attack': 2.1,
            'defense': 1.8,
            'magic_power': 0.5,
            'spell_resistance': 1.2,
            'speed': 2.3
        },
        'weapon_types': ['dagger', 'short_sword'],
        'armor_types': ['light'],
        'can_learn_magic': False,  # Exception: Has 1 fire spell
        'starting_spell': 'fire',  # Level 1 fire spell
        'key_item': 'baby_dragon',
        'key_item_optional': True,
        'recruitment_location': None,  # Starting character
        'sprite_base': 'javin'
    },

    'frostbite': {
        'name': 'Frostbite',
        'starting_class': 'gunner',
        'evolved_class': None,  # No class evolution, gets ultimate weapon
        'required': True,
        'initial_level': 3,
        'base_stats': {
            'hp': 45,
            'mp': 0,
            'attack': 16,
            'defense': 10,
            'magic_power': 0,
            'spell_resistance': 8,
            'speed': 11
        },
        'growth_rates': {
            'hp': 5.0,
            'mp': 0,
            'attack': 2.4,
            'defense': 1.9,
            'magic_power': 0,
            'spell_resistance': 1.4,
            'speed': 1.8
        },
        'weapon_types': ['shotgun', 'grenade'],
        'armor_types': ['medium'],
        'can_learn_magic': False,
        'key_item': 'shotgun_blueprint',
        'key_item_optional': False,
        'recruitment_location': 'lycanthrope_battle',
        'sprite_base': 'frostbite'
    },

    'fei': {
        'name': 'Fei',
        'starting_class': 'warrior',
        'evolved_class': 'weapon_master',
        'required': True,
        'initial_level': 4,
        'base_stats': {
            'hp': 55,
            'mp': 0,
            'attack': 14,
            'defense': 13,
            'magic_power': 0,
            'spell_resistance': 7,
            'speed': 10
        },
        'growth_rates': {
            'hp': 6.0,
            'mp': 0,
            'attack': 2.2,
            'defense': 2.5,
            'magic_power': 0,
            'spell_resistance': 1.3,
            'speed': 1.5
        },
        'weapon_types': ['sword', 'axe', 'spear'],
        'armor_types': ['heavy', 'medium'],
        'can_equip_shield': True,
        'can_learn_magic': False,
        'key_item': 'grizzly_bear_skull',
        'key_item_optional': False,
        'recruitment_location': 'caravan_battle',
        'sprite_base': 'fei',
        'special_mechanic': 'shield_taunt'
    },

    'michael': {
        'name': 'Michael',
        'starting_class': 'cleric',
        'evolved_class': 'paladin',
        'required': True,
        'initial_level': 5,
        'base_stats': {
            'hp': 42,
            'mp': 15,
            'attack': 10,
            'defense': 11,
            'magic_power': 13,
            'spell_resistance': 12,
            'speed': 9
        },
        'growth_rates': {
            'hp': 4.8,
            'mp': 2.2,
            'attack': 1.6,
            'defense': 2.0,
            'magic_power': 2.3,
            'spell_resistance': 2.1,
            'speed': 1.4
        },
        'weapon_types': ['mace', 'staff'],
        'armor_types': ['medium'],
        'can_learn_magic': True,
        'magic_types': ['holy', 'healing'],
        'key_item': 'sentimental_travelers_pouch',
        'key_item_optional': False,
        'key_item_story_given': True,  # ONLY REQUIRED KEY ITEM
        'recruitment_location': 'imperial_city',
        'sprite_base': 'michael',
        'special_mechanic': 'auto_taunt_when_paladin'
    },

    'flood': {
        'name': 'Flood',
        'starting_class': 'ice_mage',
        'evolved_class': None,  # Already ultimate class
        'required': True,
        'initial_level': 6,
        'base_stats': {
            'hp': 35,
            'mp': 20,
            'attack': 7,
            'defense': 8,
            'magic_power': 18,
            'spell_resistance': 14,
            'speed': 12
        },
        'growth_rates': {
            'hp': 3.5,
            'mp': 2.8,
            'attack': 0.9,
            'defense': 1.4,
            'magic_power': 3.2,
            'spell_resistance': 2.4,
            'speed': 1.9
        },
        'weapon_types': ['staff'],
        'armor_types': ['light'],
        'can_learn_magic': True,
        'magic_types': ['ice', 'water'],
        'max_level': 99,  # Always 99, already in ultimate class
        'key_item': None,  # No key item - foreshadows death
        'has_sidequest': False,  # No sidequest - foreshadows death
        'recruitment_location': 'imperial_city',
        'sprite_base': 'flood',
        'special_mechanic': 'double_spell_power',
        'dies_permanently': True,
        'death_event': 'second_dragon_boss'
    },

    'hannah': {
        'name': 'Hannah',
        'starting_class': 'witch',
        'evolved_class': 'magus',
        'required': True,
        'initial_level': 5,
        'base_stats': {
            'hp': 38,
            'mp': 18,
            'attack': 8,
            'defense': 7,
            'magic_power': 16,
            'spell_resistance': 13,
            'speed': 11
        },
        'growth_rates': {
            'hp': 3.8,
            'mp': 2.5,
            'attack': 1.0,
            'defense': 1.3,
            'magic_power': 2.9,
            'spell_resistance': 2.3,
            'speed': 1.7
        },
        'weapon_types': ['staff'],
        'armor_types': ['light'],
        'can_learn_magic': True,
        'magic_types': ['fire', 'thunder', 'earth', 'wind'],
        'key_item': None,  # Only character without key item requirement
        'key_item_optional': False,
        'recruitment_location': 'imperial_city',
        'sprite_base': 'hannah',
        'special_mechanic': 'double_damage_and_multi_target',
        'story_event': 'flood_death_scream'
    },

    'warghoul': {
        'name': 'Warghoul',
        'starting_class': 'undead_warrior',
        'evolved_class': 'deathknight',
        'required': True,  # Required by army camp
        'initial_level': 7,
        'base_stats': {
            'hp': 50,
            'mp': 8,
            'attack': 15,
            'defense': 12,
            'magic_power': 6,
            'spell_resistance': 10,
            'speed': 8
        },
        'growth_rates': {
            'hp': 5.5,
            'mp': 1.2,
            'attack': 2.3,
            'defense': 2.1,
            'magic_power': 0.8,
            'spell_resistance': 1.6,
            'speed': 1.3
        },
        'weapon_types': ['sword', 'axe'],
        'armor_types': ['heavy', 'medium'],
        'can_learn_magic': True,
        'magic_types': ['dark', 'necromancy'],
        'key_item': 'orc_funeral_totem',
        'key_item_optional': False,
        'recruitment_location': 'undead_lands',
        'recruitment_optional_early': True,  # Can recruit early or required later
        'sprite_base': 'warghoul',
        'special_mechanic': 'summon_skeletons'
    },

    # Optional Characters
    'cookie': {
        'name': 'Cookie',
        'starting_class': 'druid',
        'evolved_class': 'druidess',
        'required': False,
        'initial_level': 6,
        'base_stats': {
            'hp': 40,
            'mp': 16,
            'attack': 9,
            'defense': 9,
            'magic_power': 14,
            'spell_resistance': 11,
            'speed': 10
        },
        'growth_rates': {
            'hp': 4.2,
            'mp': 2.3,
            'attack': 1.2,
            'defense': 1.5,
            'magic_power': 2.5,
            'spell_resistance': 1.9,
            'speed': 1.6
        },
        'weapon_types': ['staff'],
        'armor_types': ['light'],
        'can_learn_magic': True,
        'magic_types': ['nature', 'control'],
        'key_item': 'crown_of_flowers',
        'key_item_optional': False,
        'key_item_has_cutscene': True,
        'key_item_cutscene': 'cookie_crown_comment',
        'recruitment_location': 'halfling_rescue',
        'backup_locations': ['army_camp', 'imperial_city_inn'],
        'sprite_base': 'cookie'
    },

    'iris': {
        'name': 'Iris',
        'starting_class': 'nature_bound_druid',
        'evolved_class': 'shapeshifter',
        'required': False,
        'initial_level': 6,
        'base_stats': {
            'hp': 43,
            'mp': 12,
            'attack': 13,
            'defense': 10,
            'magic_power': 10,
            'spell_resistance': 9,
            'speed': 13
        },
        'growth_rates': {
            'hp': 4.6,
            'mp': 1.8,
            'attack': 2.0,
            'defense': 1.6,
            'magic_power': 1.4,
            'spell_resistance': 1.5,
            'speed': 2.1
        },
        'weapon_types': ['claw', 'staff'],
        'armor_types': ['light'],
        'can_learn_magic': False,  # Learns enemy attacks instead
        'key_item': 'tuft_of_panda_fur',
        'key_item_optional': False,
        'key_item_has_cutscene': True,
        'key_item_cutscene': 'fei_grooming',
        'recruitment_location': 'halfling_rescue',
        'backup_locations': ['army_camp', 'imperial_city_inn'],
        'sprite_base': 'iris',
        'special_mechanic': 'learns_wildlife_attacks',
        'berserk_trigger': 'fei_death'
    },

    'fritzzit': {
        'name': 'Fritzzit',
        'starting_class': 'sniper',
        'evolved_class': None,  # Gets ultimate weapon instead
        'required': False,
        'initial_level': 7,
        'base_stats': {
            'hp': 42,
            'mp': 0,
            'attack': 17,
            'defense': 9,
            'magic_power': 0,
            'spell_resistance': 7,
            'speed': 15
        },
        'growth_rates': {
            'hp': 4.4,
            'mp': 0,
            'attack': 2.6,
            'defense': 1.6,
            'magic_power': 0,
            'spell_resistance': 1.3,
            'speed': 2.2
        },
        'weapon_types': ['rifle', 'sniper_rifle', 'crossbow'],
        'armor_types': ['light', 'medium'],
        'can_learn_magic': False,
        'key_item': 'sniper_rifle_blueprint',
        'key_item_optional': False,
        'recruitment_location': 'imperial_city_inn',
        'recruitment_paired_with': 'crankpot',  # BOTH join together
        'recruitment_window': 'post_kobolds_pre_orisia',
        'sprite_base': 'fritzzit',
        'special_mechanic': 'instant_kill_crits'
    },

    'crankpot': {
        'name': 'Crankpot',
        'starting_class': 'firemage',
        'evolved_class': 'arsonist',
        'required': False,
        'initial_level': 7,
        'base_stats': {
            'hp': 37,
            'mp': 19,
            'attack': 8,
            'defense': 8,
            'magic_power': 17,
            'spell_resistance': 12,
            'speed': 11
        },
        'growth_rates': {
            'hp': 3.9,
            'mp': 2.7,
            'attack': 1.1,
            'defense': 1.4,
            'magic_power': 3.0,
            'spell_resistance': 2.2,
            'speed': 1.7
        },
        'weapon_types': ['staff'],
        'armor_types': ['light'],
        'can_learn_magic': True,
        'magic_types': ['fire'],
        'key_item': 'molotov_cocktail',
        'key_item_optional': False,
        'recruitment_location': 'imperial_city_inn',
        'recruitment_paired_with': 'fritzzit',  # BOTH join together
        'recruitment_window': 'post_kobolds_pre_orisia',
        'sprite_base': 'crankpot',
        'special_mechanic': 'burn_status_and_spread',
        'backstory': 'ptsd_survivor'
    },

    'yipp': {
        'name': 'Yipp',
        'starting_class': 'necromancer',
        'evolved_class': ['saint', 'vampire'],  # Alignment choice
        'required': False,
        'initial_level': 8,
        'base_stats': {
            'hp': 36,
            'mp': 21,
            'attack': 7,
            'defense': 7,
            'magic_power': 16,
            'spell_resistance': 13,
            'speed': 12
        },
        'growth_rates': {
            'hp': 3.6,
            'mp': 2.9,
            'attack': 0.9,
            'defense': 1.3,
            'magic_power': 2.8,
            'spell_resistance': 2.3,
            'speed': 1.8
        },
        'weapon_types': ['staff', 'dagger'],
        'armor_types': ['light'],
        'can_learn_magic': True,
        'magic_types': ['necromancy', 'dark'],
        'key_item': ['holy_symbol', 'empty_pewter_wine_glass'],  # BOTH required
        'key_item_optional': False,
        'recruitment_location': 'random_dungeon_pre_orisia',
        'backup_locations': ['imperial_city_magic_shop'],
        'recruitment_constraint': 'pre_orisia_only',  # CRITICAL
        'sprite_base': 'yipp',
        'special_mechanic': 'alignment_choice',
        'alignment_affects_ending': True,
        'best_ending_requires': 'saint'
    }
}

# Level-up abilities for each character (every 10 levels)
# Format: level: {'name': str, 'type': str, 'description': str, 'effect': dict}
LEVEL_UP_ABILITIES = {
    'javin': {
        10: {'name': 'Critical Strike Mastery', 'type': 'passive', 'description': '+10% Critical Hit Chance', 'effect': {'crit_chance': 0.10}},
        20: {'name': 'Shadow Step', 'type': 'combat', 'description': 'Teleport behind enemy, bonus damage', 'effect': {'damage_multiplier': 1.5, 'type': 'melee'}},
        30: {'name': 'Dream Heal', 'type': 'spell_or_passive', 'description': 'Heal spell if Dreamwalker, otherwise HP regen', 'effect': {'conditional': True}},
        40: {'name': 'Nightmare Strike', 'type': 'combat', 'description': 'Psychic damage melee attack', 'effect': {'damage_type': 'psychic', 'type': 'melee'}},
        50: {'name': 'Evasion Mastery', 'type': 'passive', 'description': '+15% Evasion', 'effect': {'evasion': 0.15}},
        60: {'name': 'Dream Shield', 'type': 'spell_or_passive', 'description': 'Shield buff if Dreamwalker', 'effect': {'conditional': True}},
        70: {'name': 'Assassinate', 'type': 'combat', 'description': 'High damage to single target', 'effect': {'damage_multiplier': 2.5, 'type': 'single_target'}},
        80: {'name': 'Terror Wave', 'type': 'spell_or_passive', 'description': 'AoE psychic damage if Dreamwalker', 'effect': {'conditional': True}},
        90: {'name': "Dreamwalker's Mastery", 'type': 'passive', 'description': 'All psychic spells +25% damage', 'effect': {'psychic_damage_bonus': 0.25}}
    },

    'frostbite': {
        10: {'name': 'Piercing Shot', 'type': 'combat', 'description': 'Ignores partial armor', 'effect': {'armor_pierce': 0.5}},
        20: {'name': 'Range Damage', 'type': 'passive', 'description': '+10% Range Damage', 'effect': {'range_damage': 0.10}},
        30: {'name': 'Grenade Mastery', 'type': 'passive', 'description': 'Grenades have larger AoE', 'effect': {'grenade_aoe': 1.3}},
        40: {'name': 'Scatter Shot', 'type': 'combat', 'description': 'Hits all enemies for reduced damage', 'effect': {'aoe': True, 'damage_multiplier': 0.7}},
        50: {'name': 'Quick Reload', 'type': 'passive', 'description': '+15% attack speed', 'effect': {'attack_speed': 0.15}},
        60: {'name': 'Explosive Round', 'type': 'combat', 'description': 'Shotgun shot that explodes on impact', 'effect': {'aoe': True, 'damage_multiplier': 1.3}},
        70: {'name': 'Critical Damage', 'type': 'passive', 'description': '+20% Critical Damage', 'effect': {'crit_damage': 0.20}},
        80: {'name': 'Suppressing Fire', 'type': 'combat', 'description': 'All enemies Slowed for 3 turns', 'effect': {'status': 'slow', 'duration': 3, 'aoe': True}},
        90: {'name': "Gunner's Focus", 'type': 'passive', 'description': 'All gun attacks +25% damage', 'effect': {'gun_damage': 0.25}}
    },

    'fei': {
        10: {'name': 'Power Strike', 'type': 'combat', 'description': 'Single target high damage', 'effect': {'damage_multiplier': 1.8}},
        20: {'name': 'Physical Defense', 'type': 'passive', 'description': '+15% Physical Defense', 'effect': {'defense': 0.15}},
        30: {'name': 'Shield Bash', 'type': 'combat', 'description': 'If shield equipped, stuns enemy', 'effect': {'status': 'stun', 'duration': 1, 'requires_shield': True}},
        40: {'name': 'Berserker Rage', 'type': 'combat', 'description': '+50% attack, -25% defense for 3 turns', 'effect': {'attack_bonus': 0.50, 'defense_penalty': -0.25, 'duration': 3}},
        50: {'name': 'Battle Cry', 'type': 'combat', 'description': 'All allies +10% attack for 3 turns', 'effect': {'party_attack_bonus': 0.10, 'duration': 3}},
        60: {'name': 'Whirlwind Attack', 'type': 'combat', 'description': 'Hits all enemies', 'effect': {'aoe': True}},
        70: {'name': 'Max HP Boost', 'type': 'passive', 'description': '+20% Max HP', 'effect': {'max_hp': 0.20}},
        80: {'name': 'Precision Strike', 'type': 'combat', 'description': 'Guaranteed critical hit', 'effect': {'guaranteed_crit': True}},
        90: {'name': "Weapon Master's Edge", 'type': 'passive', 'description': 'If Weapon Master, all attacks +30% damage', 'effect': {'conditional': True, 'damage_bonus': 0.30}}
    },

    'flood': {
        10: {'name': 'Ice Shard', 'type': 'spell', 'description': 'Single target ice damage', 'effect': {'spell_level': 2, 'element': 'ice'}},
        20: {'name': 'Frost Aura', 'type': 'passive', 'description': 'Enemies that hit Flood in melee take ice damage', 'effect': {'counter_damage': True, 'element': 'ice'}},
        30: {'name': 'Glacial Spike', 'type': 'spell', 'description': 'High damage ice attack', 'effect': {'spell_level': 4, 'element': 'ice'}},
        40: {'name': 'Double Cast', 'type': 'passive', 'description': 'Can cast 2x MP to double spell power', 'effect': {'double_cast': True}},
        50: {'name': 'Magic Power', 'type': 'passive', 'description': '+15% Magic Power', 'effect': {'magic_power': 0.15}},
        60: {'name': 'Blizzard Storm', 'type': 'spell', 'description': 'AoE ice damage', 'effect': {'spell_level': 6, 'element': 'ice', 'aoe': True}},
        70: {'name': 'Absolute Zero', 'type': 'combat', 'description': 'Freeze enemy for 1 turn', 'effect': {'status': 'freeze', 'duration': 1}},
        80: {'name': "Ice Queen's Blessing", 'type': 'passive', 'description': 'All ice spells +20% damage', 'effect': {'ice_damage': 0.20}},
        90: {'name': 'Diamond Dust', 'type': 'spell', 'description': 'Massive AoE ice damage, costs 9 MP', 'effect': {'spell_level': 9, 'element': 'ice', 'aoe': True}}
    },

    'hannah': {
        10: {'name': 'Elemental Strike', 'type': 'combat', 'description': 'Ranged elemental attack', 'effect': {'damage_type': 'elemental', 'ranged': True}},
        20: {'name': 'Magic Power', 'type': 'passive', 'description': '+10% Magic Power', 'effect': {'magic_power': 0.10}},
        30: {'name': 'Mana Shield', 'type': 'passive', 'description': 'Can spend MP to reduce damage taken', 'effect': {'mana_shield': True}},
        40: {'name': 'Chain Lightning', 'type': 'spell', 'description': 'Bounces between enemies', 'effect': {'spell_level': 5, 'element': 'thunder', 'chain': True}},
        50: {'name': 'Spell Focus', 'type': 'passive', 'description': 'All spells +15% accuracy', 'effect': {'spell_accuracy': 0.15}},
        60: {'name': 'Multi-Cast', 'type': 'passive', 'description': 'If Magus, can make single-target spells hit all enemies for +3 MP', 'effect': {'conditional': True, 'multi_cast': True}},
        70: {'name': 'Arcane Mastery', 'type': 'passive', 'description': 'All elemental spells +20% damage', 'effect': {'elemental_damage': 0.20}},
        80: {'name': 'Meteor Swarm', 'type': 'spell', 'description': 'Massive fire/physical AoE', 'effect': {'spell_level': 8, 'element': 'fire', 'aoe': True, 'physical_component': True}},
        90: {'name': 'Magus Supremacy', 'type': 'passive', 'description': 'If Magus, all magic +25% power', 'effect': {'conditional': True, 'magic_bonus': 0.25}}
    },

    'michael': {
        10: {'name': 'Holy Light', 'type': 'spell', 'description': 'Single target holy damage', 'effect': {'spell_level': 2, 'element': 'holy'}},
        20: {'name': 'Healing Power', 'type': 'passive', 'description': 'All healing spells restore +10%', 'effect': {'healing_bonus': 0.10}},
        30: {'name': 'Divine Shield', 'type': 'combat', 'description': 'Grants ally damage immunity for 1 turn', 'effect': {'immunity': 1}},
        40: {'name': 'Smite', 'type': 'combat', 'description': 'If Paladin, holy physical attack', 'effect': {'conditional': True, 'element': 'holy', 'type': 'physical'}},
        50: {'name': 'Raise', 'type': 'spell', 'description': 'Resurrects fallen ally, if Paladin', 'effect': {'conditional': True, 'resurrect': True}},
        60: {'name': 'Physical Defense', 'type': 'passive', 'description': '+20% Physical Defense', 'effect': {'defense': 0.20}},
        70: {'name': 'Holy Aura', 'type': 'passive', 'description': 'All allies regenerate HP each turn', 'effect': {'party_regen': True}},
        80: {'name': 'Judgment', 'type': 'spell', 'description': 'Massive holy damage to undead', 'effect': {'spell_level': 7, 'element': 'holy', 'vs_undead_bonus': 2.0}},
        90: {'name': "Paladin's Resolve", 'type': 'passive', 'description': 'If Paladin, +30% defense when shield equipped', 'effect': {'conditional': True, 'defense_bonus': 0.30}}
    },

    'warghoul': {
        10: {'name': 'Death Strike', 'type': 'combat', 'description': 'Drains HP from enemy', 'effect': {'hp_drain': 0.3}},
        20: {'name': 'Physical Attack', 'type': 'passive', 'description': '+15% Physical Attack', 'effect': {'attack': 0.15}},
        30: {'name': 'Undead Resilience', 'type': 'passive', 'description': 'Immune to poison, 50% resistance to holy', 'effect': {'poison_immune': True, 'holy_resistance': 0.50}},
        40: {'name': 'Soul Harvest', 'type': 'combat', 'description': 'Kills enemy, restores HP to Warghoul', 'effect': {'execute': True, 'hp_restore': True}},
        50: {'name': 'Summon Skeleton', 'type': 'combat', 'description': 'If Deathknight, summons skeleton allies', 'effect': {'conditional': True, 'summon': 'skeleton'}},
        60: {'name': 'Dark Aura', 'type': 'passive', 'description': 'Enemies near Warghoul take damage each turn', 'effect': {'aoe_dot': True}},
        70: {'name': 'Max HP Boost', 'type': 'passive', 'description': '+25% Max HP', 'effect': {'max_hp': 0.25}},
        80: {'name': "Reaper's Touch", 'type': 'combat', 'description': 'Instant kill low-HP enemy', 'effect': {'execute_threshold': 0.25}},
        90: {'name': "Deathknight's Dominion", 'type': 'passive', 'description': 'If Deathknight, all dark abilities +30%', 'effect': {'conditional': True, 'dark_damage': 0.30}}
    },

    'cookie': {
        10: {'name': 'Entangle', 'type': 'combat', 'description': 'Roots enemy in place for 2 turns', 'effect': {'status': 'root', 'duration': 2}},
        20: {'name': 'Nature Damage', 'type': 'passive', 'description': '+10% Nature Damage', 'effect': {'nature_damage': 0.10}},
        30: {'name': 'Sandstorm', 'type': 'spell', 'description': 'If Druidess, blinds all enemies', 'effect': {'conditional': True, 'status': 'blind', 'aoe': True}},
        40: {'name': 'Thorns', 'type': 'passive', 'description': 'Enemies that attack Cookie take damage', 'effect': {'counter_damage': True}},
        50: {'name': "Nature's Wrath", 'type': 'spell', 'description': 'AoE nature damage', 'effect': {'spell_level': 5, 'element': 'nature', 'aoe': True}},
        60: {'name': 'Excessive Vinegrowth', 'type': 'spell', 'description': 'If Druidess, slows all enemies', 'effect': {'conditional': True, 'status': 'slow', 'aoe': True}},
        70: {'name': 'Spell Resistance', 'type': 'passive', 'description': '+15% Spell Resistance', 'effect': {'spell_resistance': 0.15}},
        80: {'name': 'Bubble', 'type': 'spell', 'description': 'If Druidess, silence + prevent attack, pops when hit', 'effect': {'conditional': True, 'status': ['silence', 'prevent_attack'], 'breaks_on_hit': True}},
        90: {'name': 'Druidess Supremacy', 'type': 'passive', 'description': 'If Druidess, all control spells last +2 turns', 'effect': {'conditional': True, 'status_duration': 2}}
    },

    'iris': {
        10: {'name': 'Animal Instinct', 'type': 'passive', 'description': '+10% evasion', 'effect': {'evasion': 0.10}},
        20: {'name': 'Wild Strike', 'type': 'combat', 'description': 'Mimics last wildlife attack seen', 'effect': {'mimic': True}},
        30: {'name': "Shapeshifter's Agility", 'type': 'passive', 'description': '+15% attack speed', 'effect': {'attack_speed': 0.15}},
        40: {'name': 'Panda Form', 'type': 'combat', 'description': 'If Shapeshifter, transform into panda', 'effect': {'conditional': True, 'transform': 'panda'}},
        50: {'name': "Predator's Focus", 'type': 'passive', 'description': '+20% damage to beasts/wildlife', 'effect': {'vs_wildlife': 0.20}},
        60: {'name': 'Pack Tactics', 'type': 'passive', 'description': '+10% damage for each ally alive', 'effect': {'pack_bonus': 0.10}},
        70: {'name': 'Physical Attack', 'type': 'passive', 'description': '+20% Physical Attack', 'effect': {'attack': 0.20}},
        80: {'name': 'Feral Rage', 'type': 'combat', 'description': 'If Shapeshifter, go Berserk voluntarily for 3 turns', 'effect': {'conditional': True, 'berserk': True, 'duration': 3}},
        90: {'name': "Shapeshifter's Mastery", 'type': 'passive', 'description': 'If Shapeshifter, Panda form gets 4th attack', 'effect': {'conditional': True, 'panda_attacks': 4}}
    },

    'fritzzit': {
        10: {'name': 'Headshot', 'type': 'combat', 'description': 'High damage, bonus crit chance', 'effect': {'damage_multiplier': 1.6, 'crit_bonus': 0.20}},
        20: {'name': 'Critical Chance', 'type': 'passive', 'description': '+15% Critical Chance', 'effect': {'crit_chance': 0.15}},
        30: {'name': 'Armor Piercing', 'type': 'passive', 'description': 'Attacks ignore 25% of enemy armor', 'effect': {'armor_pierce': 0.25}},
        40: {'name': 'Explosive Shot', 'type': 'combat', 'description': 'Bullet explodes on impact, AoE damage', 'effect': {'aoe': True, 'damage_multiplier': 1.4}},
        50: {'name': 'Eagle Eye', 'type': 'passive', 'description': '+20% accuracy', 'effect': {'accuracy': 0.20}},
        60: {'name': 'Critical Damage', 'type': 'passive', 'description': '+25% Critical Damage', 'effect': {'crit_damage': 0.25}},
        70: {'name': 'Killshot', 'type': 'combat', 'description': 'If Ultimate Rifle, guaranteed crit', 'effect': {'conditional': True, 'guaranteed_crit': True}},
        80: {'name': "Sniper's Focus", 'type': 'passive', 'description': '+30% damage to single targets', 'effect': {'single_target_bonus': 0.30}},
        90: {'name': 'Deadeye', 'type': 'passive', 'description': 'Critical hits deal 3x damage instead of 2x', 'effect': {'crit_multiplier': 3.0}}
    },

    'crankpot': {
        10: {'name': 'Fireball', 'type': 'spell', 'description': 'Single target fire damage', 'effect': {'spell_level': 2, 'element': 'fire'}},
        20: {'name': 'Fire Damage', 'type': 'passive', 'description': '+10% Fire Damage', 'effect': {'fire_damage': 0.10}},
        30: {'name': 'Flame Wall', 'type': 'combat', 'description': 'Creates fire barrier that damages enemies', 'effect': {'barrier': True, 'element': 'fire'}},
        40: {'name': 'Inferno', 'type': 'spell', 'description': 'AoE fire damage', 'effect': {'spell_level': 5, 'element': 'fire', 'aoe': True}},
        50: {'name': 'Burn Mastery', 'type': 'passive', 'description': 'If Arsonist, all fire spells inflict Burn', 'effect': {'conditional': True, 'inflict_burn': True}},
        60: {'name': 'Spell Power', 'type': 'passive', 'description': '+15% Spell Power', 'effect': {'spell_power': 0.15}},
        70: {'name': 'Blazing Aura', 'type': 'passive', 'description': 'Enemies near Crankpot take fire damage', 'effect': {'aoe_dot': True, 'element': 'fire'}},
        80: {'name': 'Arson', 'type': 'spell', 'description': 'If Arsonist, massive fire damage + guaranteed Burn spread', 'effect': {'conditional': True, 'spell_level': 7, 'element': 'fire', 'burn_spread': True}},
        90: {'name': "Pyromancer's Fury", 'type': 'passive', 'description': 'If Arsonist, all fire spells +30% damage', 'effect': {'conditional': True, 'fire_damage': 0.30}}
    },

    'yipp': {
        # Saint Path
        'saint': {
            10: {'name': 'Holy Bolt', 'type': 'spell', 'description': 'Single target holy damage', 'effect': {'spell_level': 2, 'element': 'holy'}},
            20: {'name': 'Holy Damage', 'type': 'passive', 'description': '+15% Holy Damage', 'effect': {'holy_damage': 0.15}},
            30: {'name': 'Mass Heal', 'type': 'spell', 'description': 'Heals all allies', 'effect': {'spell_level': 4, 'heal_all': True}},
            40: {'name': 'Turn Undead', 'type': 'combat', 'description': 'Forces undead to flee', 'effect': {'vs_undead': True, 'flee': True}},
            50: {'name': 'Divine Intervention', 'type': 'passive', 'description': '20% chance to survive lethal damage', 'effect': {'survive_chance': 0.20}},
            60: {'name': 'Holy Nova', 'type': 'spell', 'description': 'AoE holy damage, bonus vs undead', 'effect': {'spell_level': 6, 'element': 'holy', 'aoe': True, 'vs_undead_bonus': 1.5}},
            70: {'name': 'Healing Power', 'type': 'passive', 'description': '+20% Healing Power', 'effect': {'healing_bonus': 0.20}},
            80: {'name': 'Resurrect All', 'type': 'spell', 'description': 'Revives all fallen allies', 'effect': {'spell_level': 8, 'resurrect_all': True}},
            90: {'name': "Saint's Grace", 'type': 'passive', 'description': 'All holy spells +30% power', 'effect': {'holy_damage': 0.30}}
        },
        # Vampire Path
        'vampire': {
            10: {'name': 'Drain Life', 'type': 'combat', 'description': 'Steals HP from enemy', 'effect': {'hp_drain': 0.4}},
            20: {'name': 'Dark Damage', 'type': 'passive', 'description': '+15% Dark Damage', 'effect': {'dark_damage': 0.15}},
            30: {'name': 'Blood Mist', 'type': 'spell', 'description': 'Damages living enemies, heals party', 'effect': {'spell_level': 4, 'contextual': True}},
            40: {'name': 'Dominate Undead', 'type': 'combat', 'description': 'Control 1 non-boss undead', 'effect': {'control_undead': True}},
            50: {'name': 'Vampiric Resilience', 'type': 'passive', 'description': 'Regenerate HP each turn', 'effect': {'hp_regen': True}},
            60: {'name': 'Life Siphon', 'type': 'spell', 'description': 'Drains HP from all enemies', 'effect': {'spell_level': 6, 'aoe': True, 'hp_drain': 0.3}},
            70: {'name': 'Max HP Boost', 'type': 'passive', 'description': '+20% Max HP', 'effect': {'max_hp': 0.20}},
            80: {'name': 'Blood Frenzy', 'type': 'passive', 'description': 'Attacks restore HP', 'effect': {'lifesteal': True}},
            90: {'name': 'Vampire Lord', 'type': 'passive', 'description': 'All vampire abilities +30% effectiveness', 'effect': {'vampire_bonus': 0.30}}
        },
        # Necromancer Path (no evolution)
        'necromancer': {
            10: {'name': 'Bone Spike', 'type': 'spell', 'description': 'Single target dark damage', 'effect': {'spell_level': 2, 'element': 'dark'}},
            20: {'name': 'Dark Damage', 'type': 'passive', 'description': '+10% Dark Damage', 'effect': {'dark_damage': 0.10}},
            30: {'name': 'Summon Zombie', 'type': 'combat', 'description': 'Summons weak undead ally', 'effect': {'summon': 'zombie'}},
            40: {'name': 'Curse', 'type': 'spell', 'description': 'Reduces enemy stats', 'effect': {'spell_level': 4, 'debuff': True}},
            50: {'name': 'Death Coil', 'type': 'spell', 'description': 'Damages enemy or heals undead ally', 'effect': {'spell_level': 5, 'contextual': True}},
            60: {'name': 'Spell Power', 'type': 'passive', 'description': '+15% Spell Power', 'effect': {'spell_power': 0.15}},
            70: {'name': 'Plague', 'type': 'spell', 'description': 'AoE poison damage', 'effect': {'spell_level': 7, 'status': 'poison', 'aoe': True}}
        }
    }
}

# Class evolution requirements and effects
CLASS_EVOLUTIONS = {
    'javin': {
        'from_class': 'claw_noble',
        'to_class': 'dreamwalker',
        'requires_key_item': 'baby_dragon',
        'level_cap_increase': True,  # 75 -> 99
        'new_abilities': ['dream_spells', 'nightmare_spells'],
        'description': 'Gains psychic damage spells that cannot be resisted'
    },
    'frostbite': {
        'from_class': 'gunner',
        'to_class': None,  # No class change, gets weapon
        'requires_key_item': 'shotgun_blueprint',
        'level_cap_increase': True,  # 75 -> 99 upon getting Ultimate Shotgun
        'reward': 'ultimate_shotgun',
        'new_abilities': ['double_attack_shotgun'],
        'description': 'Receives Ultimate Shotgun and can attack twice per turn'
    },
    'fei': {
        'from_class': 'warrior',
        'to_class': 'weapon_master',
        'requires_key_item': 'grizzly_bear_skull',
        'level_cap_increase': True,  # 75 -> 99
        'loses': ['shield_equip'],
        'gains': ['dual_wield', 'double_attack'],
        'visual_change': 'bear_skull_helmet',
        'description': 'Loses shield but gains dual wielding and double attacks'
    },
    'michael': {
        'from_class': 'cleric',
        'to_class': 'paladin',
        'requires_key_item': 'sentimental_travelers_pouch',
        'level_cap_increase': True,  # 75 -> 99
        'keeps': ['all_cleric_spells'],
        'gains': ['sword_mace_equip', 'shield_equip', 'plate_armor', 'auto_taunt', 'raise_spell'],
        'description': 'Becomes best tank while keeping all healing magic'
    },
    'hannah': {
        'from_class': 'witch',
        'to_class': 'magus',
        'requires_key_item': None,  # Only character without key item
        'level_cap_increase': True,  # 75 -> 99
        'gains': ['double_damage', 'multi_target'],
        'description': 'Can double spell damage or make spells hit all enemies'
    },
    'warghoul': {
        'from_class': 'undead_warrior',
        'to_class': 'deathknight',
        'requires_key_item': 'orc_funeral_totem',
        'level_cap_increase': True,  # 75 -> 99
        'gains': ['summon_skeletons'],
        'description': 'Can summon skeleton allies with taunt ability'
    },
    'cookie': {
        'from_class': 'druid',
        'to_class': 'druidess',
        'requires_key_item': 'crown_of_flowers',
        'level_cap_increase': True,  # 75 -> 99
        'gains': ['sandstorm', 'excessive_vinegrowth', 'bubble', 'sensory_deprivation'],
        'description': 'Gains powerful control spells and desert exclusive spell'
    },
    'iris': {
        'from_class': 'nature_bound_druid',
        'to_class': 'shapeshifter',
        'requires_key_item': 'tuft_of_panda_fur',
        'level_cap_increase': True,  # 75 -> 99
        'gains': ['panda_form', 'triple_attack', 'fei_bonus', 'improved_berserk'],
        'description': 'Can transform into panda with 3 attacks per turn'
    },
    'fritzzit': {
        'from_class': 'sniper',
        'to_class': None,  # No class change, gets weapon
        'requires_key_item': 'sniper_rifle_blueprint',
        'level_cap_increase': True,  # 75 -> 99 upon getting Ultimate Sniper Rifle
        'reward': 'ultimate_sniper_rifle',
        'gains': ['instant_kill_crits', 'increased_crit_chance'],
        'description': 'Critical hits instantly kill non-boss enemies'
    },
    'crankpot': {
        'from_class': 'firemage',
        'to_class': 'arsonist',
        'requires_key_item': 'molotov_cocktail',
        'level_cap_increase': True,  # 75 -> 99
        'gains': ['burn_status', 'burn_spread_15_percent'],
        'description': 'All fire spells inflict Burn status that can spread'
    },
    'yipp': {
        'from_class': 'necromancer',
        'to_class': ['saint', 'vampire'],  # Alignment choice
        'requires_key_item': ['holy_symbol', 'empty_pewter_wine_glass'],  # BOTH required
        'level_cap_increase': True,  # 75 -> 99
        'choice': True,
        'saint': {
            'gains': ['holy_aoe', 'mass_heal', 'resurrect'],
            'description': 'Becomes holy caster with healing and resurrection',
            'ending_requirement': 'best_ending'
        },
        'vampire': {
            'gains': ['drain_life', 'blood_mist', 'undead_control'],
            'description': 'Becomes vampire with life-stealing abilities',
            'final_battle': 'betrays_party',
            'ending_lock': 'bad_ending_only'
        }
    }
}

# Default level caps
DEFAULT_LEVEL_CAP = 75
EVOLVED_LEVEL_CAP = 99
FLOOD_LEVEL_CAP = 99  # Flood always has 99 cap

def get_character_stats_at_level(character_id, level):
    """Calculate character stats at a given level"""
    char = CHARACTERS[character_id]
    stats = char['base_stats'].copy()
    growth = char['growth_rates']

    for stat in stats:
        stats[stat] += growth[stat] * (level - 1)

    return stats

def get_max_level(character_id, evolved=False, has_ultimate_weapon=False):
    """Get max level for a character"""
    if character_id == 'flood':
        return FLOOD_LEVEL_CAP

    if character_id in ['frostbite', 'fritzzit'] and has_ultimate_weapon:
        return EVOLVED_LEVEL_CAP

    if evolved:
        return EVOLVED_LEVEL_CAP

    return DEFAULT_LEVEL_CAP

def can_character_learn_magic(character_id):
    """Check if character can learn magic spells"""
    return CHARACTERS[character_id].get('can_learn_magic', False)

def get_character_magic_types(character_id):
    """Get magic types a character can learn"""
    char = CHARACTERS[character_id]
    return char.get('magic_types', [])

def is_character_required(character_id):
    """Check if character is required to recruit"""
    return CHARACTERS[character_id]['required']
