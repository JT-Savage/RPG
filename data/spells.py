"""
Magic spell system with purchasable spells
MP cost = spell level (Level 1 = 1 MP, Level 9 = 9 MP)
"""

# Spell definitions
# Format: spell_id: {name, level, element, descriptor, effects, learnable_by}
SPELLS = {
    # Level 1 Spells
    'fire': {
        'name': 'Fire',
        'level': 1,
        'element': 'fire',
        'descriptor': 'magical',  # Reduced by Spell Resistance
        'target': 'single',
        'base_damage': 15,
        'learnable_by': ['firemage', 'arsonist', 'witch', 'magus'],
        'description': 'Basic fire spell that damages a single enemy',
        'shop_cost': 50
    },
    'cure': {
        'name': 'Cure',
        'level': 1,
        'element': 'holy',
        'descriptor': None,  # Healing
        'target': 'single',
        'base_healing': 25,
        'learnable_by': ['cleric', 'paladin', 'saint'],
        'description': 'Restores HP to a single ally',
        'shop_cost': 50
    },
    'thunder': {
        'name': 'Thunder',
        'level': 1,
        'element': 'thunder',
        'descriptor': 'magical',
        'target': 'single',
        'base_damage': 15,
        'learnable_by': ['witch', 'magus'],
        'description': 'Basic thunder spell that damages a single enemy',
        'shop_cost': 50
    },
    'blizzard': {
        'name': 'Blizzard',
        'level': 1,
        'element': 'ice',
        'descriptor': 'magical',
        'target': 'single',
        'base_damage': 15,
        'learnable_by': ['ice_mage', 'witch', 'magus'],
        'description': 'Basic ice spell that damages a single enemy',
        'shop_cost': 50
    },
    'drain': {
        'name': 'Drain',
        'level': 1,
        'element': 'dark',
        'descriptor': 'magical',
        'target': 'single',
        'base_damage': 12,
        'hp_drain': 0.5,  # 50% of damage heals caster
        'learnable_by': ['necromancer', 'saint', 'vampire'],
        'description': 'Damages enemy and restores HP to caster',
        'shop_cost': 60
    },

    # Level 2 Spells
    'fira': {
        'name': 'Fira',
        'level': 2,
        'element': 'fire',
        'descriptor': 'magical',
        'target': 'single',
        'base_damage': 30,
        'learnable_by': ['firemage', 'arsonist', 'witch', 'magus'],
        'description': 'Moderate fire spell that damages a single enemy',
        'shop_cost': 150
    },
    'cura': {
        'name': 'Cura',
        'level': 2,
        'element': 'holy',
        'descriptor': None,
        'target': 'single',
        'base_healing': 50,
        'learnable_by': ['cleric', 'paladin', 'saint'],
        'description': 'Restores moderate HP to a single ally',
        'shop_cost': 150
    },
    'thundara': {
        'name': 'Thundara',
        'level': 2,
        'element': 'thunder',
        'descriptor': 'magical',
        'target': 'single',
        'base_damage': 30,
        'learnable_by': ['witch', 'magus'],
        'description': 'Moderate thunder spell',
        'shop_cost': 150
    },
    'blizzara': {
        'name': 'Blizzara',
        'level': 2,
        'element': 'ice',
        'descriptor': 'magical',
        'target': 'single',
        'base_damage': 30,
        'learnable_by': ['ice_mage', 'witch', 'magus'],
        'description': 'Moderate ice spell',
        'shop_cost': 150
    },
    'sleep': {
        'name': 'Sleep',
        'level': 2,
        'element': None,
        'descriptor': 'magical',
        'target': 'single',
        'status_effect': 'sleep',
        'duration': 3,
        'learnable_by': ['witch', 'magus', 'necromancer'],
        'description': 'Puts enemy to sleep for 3 turns',
        'shop_cost': 120
    },
    'holy_bolt': {
        'name': 'Holy Bolt',
        'level': 2,
        'element': 'holy',
        'descriptor': 'magical',
        'target': 'single',
        'base_damage': 30,
        'vs_undead_bonus': 1.5,
        'learnable_by': ['saint', 'cleric', 'paladin'],
        'description': 'Holy damage, bonus against undead',
        'shop_cost': 160
    },
    'ice_shard': {
        'name': 'Ice Shard',
        'level': 2,
        'element': 'ice',
        'descriptor': 'magical',
        'target': 'single',
        'base_damage': 32,
        'learnable_by': ['ice_mage'],
        'description': 'Sharp ice projectile',
        'shop_cost': 150,
        'ability_unlock': True  # Also learned as ability at level 10
    },
    'bone_spike': {
        'name': 'Bone Spike',
        'level': 2,
        'element': 'dark',
        'descriptor': 'magical',
        'target': 'single',
        'base_damage': 28,
        'learnable_by': ['necromancer', 'vampire', 'deathknight'],
        'description': 'Dark magic projectile',
        'shop_cost': 140
    },

    # Level 3 Spells
    'firaga': {
        'name': 'Firaga',
        'level': 3,
        'element': 'fire',
        'descriptor': 'magical',
        'target': 'single',
        'base_damage': 50,
        'learnable_by': ['firemage', 'arsonist', 'witch', 'magus'],
        'description': 'Strong fire spell',
        'shop_cost': 300
    },
    'curaga': {
        'name': 'Curaga',
        'level': 3,
        'element': 'holy',
        'descriptor': None,
        'target': 'single',
        'base_healing': 80,
        'learnable_by': ['cleric', 'paladin', 'saint'],
        'description': 'Restores significant HP to a single ally',
        'shop_cost': 300
    },
    'thundaga': {
        'name': 'Thundaga',
        'level': 3,
        'element': 'thunder',
        'descriptor': 'magical',
        'target': 'single',
        'base_damage': 50,
        'learnable_by': ['witch', 'magus'],
        'description': 'Strong thunder spell',
        'shop_cost': 300
    },
    'blizzaga': {
        'name': 'Blizzaga',
        'level': 3,
        'element': 'ice',
        'descriptor': 'magical',
        'target': 'single',
        'base_damage': 50,
        'learnable_by': ['ice_mage', 'witch', 'magus'],
        'description': 'Strong ice spell',
        'shop_cost': 300
    },
    'poison': {
        'name': 'Poison',
        'level': 3,
        'element': None,
        'descriptor': 'magical',
        'target': 'single',
        'status_effect': 'poison',
        'duration': 5,
        'learnable_by': ['witch', 'magus', 'necromancer'],
        'description': 'Poisons enemy for 5 turns',
        'shop_cost': 250
    },
    'bio': {
        'name': 'Bio',
        'level': 3,
        'element': None,
        'descriptor': 'magical',
        'target': 'all_enemies',
        'base_damage': 25,
        'status_effect': 'poison',
        'duration': 3,
        'learnable_by': ['witch', 'magus', 'necromancer'],
        'description': 'Poison damage to all enemies',
        'shop_cost': 350
    },

    # Level 4 Spells
    'haste': {
        'name': 'Haste',
        'level': 4,
        'element': None,
        'descriptor': None,
        'target': 'single',
        'status_effect': 'haste',
        'duration': 5,
        'learnable_by': ['witch', 'magus'],
        'description': 'Increases ally speed for 5 turns',
        'shop_cost': 400
    },
    'slow': {
        'name': 'Slow',
        'level': 4,
        'element': None,
        'descriptor': 'magical',
        'target': 'single',
        'status_effect': 'slow',
        'duration': 4,
        'learnable_by': ['witch', 'magus', 'necromancer'],
        'description': 'Decreases enemy speed for 4 turns',
        'shop_cost': 350
    },
    'protect': {
        'name': 'Protect',
        'level': 4,
        'element': None,
        'descriptor': None,
        'target': 'single',
        'defense_boost': 1.5,
        'duration': 5,
        'learnable_by': ['cleric', 'paladin', 'witch', 'magus'],
        'description': 'Increases ally defense for 5 turns',
        'shop_cost': 400
    },
    'shell': {
        'name': 'Shell',
        'level': 4,
        'element': None,
        'descriptor': None,
        'target': 'single',
        'spell_resistance_boost': 1.5,
        'duration': 5,
        'learnable_by': ['cleric', 'paladin', 'witch', 'magus'],
        'description': 'Increases ally spell resistance for 5 turns',
        'shop_cost': 400
    },
    'confuse': {
        'name': 'Confuse',
        'level': 4,
        'element': None,
        'descriptor': 'magical',
        'target': 'single',
        'status_effect': 'confuse',
        'duration': 3,
        'learnable_by': ['witch', 'magus', 'necromancer'],
        'description': 'Confuses enemy for 3 turns',
        'shop_cost': 350
    },
    'mass_heal': {
        'name': 'Mass Heal',
        'level': 4,
        'element': 'holy',
        'descriptor': None,
        'target': 'all_allies',
        'base_healing': 50,
        'learnable_by': ['saint'],
        'description': 'Heals all allies',
        'shop_cost': 500,
        'ability_unlock': True  # Saint level 30
    },
    'glacial_spike': {
        'name': 'Glacial Spike',
        'level': 4,
        'element': 'ice',
        'descriptor': 'magical',
        'target': 'single',
        'base_damage': 65,
        'learnable_by': ['ice_mage'],
        'description': 'High damage ice attack',
        'shop_cost': 450,
        'ability_unlock': True  # Flood level 30
    },
    'curse': {
        'name': 'Curse',
        'level': 4,
        'element': 'dark',
        'descriptor': 'magical',
        'target': 'single',
        'debuff': {'attack': -0.25, 'defense': -0.25},
        'duration': 4,
        'learnable_by': ['necromancer', 'vampire'],
        'description': 'Reduces enemy attack and defense',
        'shop_cost': 380
    },
    'blood_mist': {
        'name': 'Blood Mist',
        'level': 4,
        'element': 'dark',
        'descriptor': 'magical',
        'target': 'contextual',  # Damages living, heals party
        'base_damage': 40,
        'base_healing': 30,
        'learnable_by': ['vampire'],
        'description': 'Damages living enemies, heals party',
        'shop_cost': 500,
        'contextual': True
    },

    # Level 5 Spells
    'raise': {
        'name': 'Raise',
        'level': 5,
        'element': 'holy',
        'descriptor': None,
        'target': 'single_dead',
        'resurrection': True,
        'hp_restore': 0.5,  # 50% HP
        'learnable_by': ['paladin', 'saint'],
        'description': 'Resurrects fallen ally with 50% HP',
        'shop_cost': 800,
        'ability_unlock': True  # Michael/Paladin level 50
    },
    'esuna': {
        'name': 'Esuna',
        'level': 5,
        'element': None,
        'descriptor': None,
        'target': 'single',
        'removes_status': 'all',
        'learnable_by': ['cleric', 'paladin', 'saint'],
        'description': 'Removes all status effects from ally',
        'shop_cost': 600
    },
    'quake': {
        'name': 'Quake',
        'level': 5,
        'element': 'earth',
        'descriptor': 'magical',
        'target': 'all_enemies',
        'base_damage': 45,
        'learnable_by': ['witch', 'magus'],
        'description': 'Earth damage to all enemies',
        'shop_cost': 700
    },
    'tornado': {
        'name': 'Tornado',
        'level': 5,
        'element': 'wind',
        'descriptor': 'magical',
        'target': 'all_enemies',
        'base_damage': 45,
        'learnable_by': ['witch', 'magus'],
        'description': 'Wind damage to all enemies',
        'shop_cost': 700
    },
    'chain_lightning': {
        'name': 'Chain Lightning',
        'level': 5,
        'element': 'thunder',
        'descriptor': 'magical',
        'target': 'chain',  # Bounces between enemies
        'base_damage': 40,
        'max_chains': 3,
        'learnable_by': ['witch', 'magus'],
        'description': 'Thunder that bounces between enemies',
        'shop_cost': 750,
        'ability_unlock': True  # Hannah level 40
    },
    'death_coil': {
        'name': 'Death Coil',
        'level': 5,
        'element': 'dark',
        'descriptor': 'magical',
        'target': 'contextual',  # Damages enemy or heals undead
        'base_damage': 55,
        'base_healing': 55,
        'learnable_by': ['necromancer', 'vampire', 'deathknight'],
        'description': 'Damages enemy or heals undead ally',
        'shop_cost': 650,
        'contextual': True
    },
    'natures_wrath': {
        'name': "Nature's Wrath",
        'level': 5,
        'element': 'nature',
        'descriptor': 'magical',
        'target': 'all_enemies',
        'base_damage': 45,
        'learnable_by': ['druid', 'druidess'],
        'description': 'Nature damage to all enemies',
        'shop_cost': 700
    },
    'inferno': {
        'name': 'Inferno',
        'level': 5,
        'element': 'fire',
        'descriptor': 'magical',
        'target': 'all_enemies',
        'base_damage': 48,
        'learnable_by': ['firemage', 'arsonist'],
        'description': 'Fire damage to all enemies',
        'shop_cost': 720,
        'ability_unlock': True  # Crankpot level 40
    },

    # Level 6 Spells
    'flare': {
        'name': 'Flare',
        'level': 6,
        'element': 'fire',
        'descriptor': 'magical',
        'target': 'single',
        'base_damage': 85,
        'learnable_by': ['firemage', 'arsonist', 'witch', 'magus'],
        'description': 'Extremely powerful fire spell',
        'shop_cost': 1200
    },
    'holy': {
        'name': 'Holy',
        'level': 6,
        'element': 'holy',
        'descriptor': 'magical',
        'target': 'single',
        'base_damage': 85,
        'vs_undead_bonus': 2.0,
        'learnable_by': ['saint', 'paladin'],
        'description': 'Powerful holy damage, devastating to undead',
        'shop_cost': 1200
    },
    'blizzaja': {
        'name': 'Blizzaja',
        'level': 6,
        'element': 'ice',
        'descriptor': 'magical',
        'target': 'all_enemies',
        'base_damage': 55,
        'learnable_by': ['ice_mage', 'witch', 'magus'],
        'description': 'Powerful ice damage to all enemies',
        'shop_cost': 1100
    },
    'thundaja': {
        'name': 'Thundaja',
        'level': 6,
        'element': 'thunder',
        'descriptor': 'magical',
        'target': 'all_enemies',
        'base_damage': 55,
        'learnable_by': ['witch', 'magus'],
        'description': 'Powerful thunder damage to all enemies',
        'shop_cost': 1100
    },
    'blizzard_storm': {
        'name': 'Blizzard Storm',
        'level': 6,
        'element': 'ice',
        'descriptor': 'magical',
        'target': 'all_enemies',
        'base_damage': 58,
        'learnable_by': ['ice_mage'],
        'description': 'Massive ice storm',
        'shop_cost': 1150,
        'ability_unlock': True  # Flood level 60
    },
    'holy_nova': {
        'name': 'Holy Nova',
        'level': 6,
        'element': 'holy',
        'descriptor': 'magical',
        'target': 'all_enemies',
        'base_damage': 55,
        'vs_undead_bonus': 1.5,
        'learnable_by': ['saint'],
        'description': 'AoE holy damage, bonus vs undead',
        'shop_cost': 1200,
        'ability_unlock': True  # Yipp/Saint level 60
    },
    'life_siphon': {
        'name': 'Life Siphon',
        'level': 6,
        'element': 'dark',
        'descriptor': 'magical',
        'target': 'all_enemies',
        'base_damage': 40,
        'hp_drain': 0.3,
        'learnable_by': ['vampire'],
        'description': 'Drains HP from all enemies',
        'shop_cost': 1100
    },

    # Level 7 Spells
    'meteor': {
        'name': 'Meteor',
        'level': 7,
        'element': 'fire',
        'descriptor': 'physical',  # Physical descriptor!
        'target': 'all_enemies',
        'base_damage': 70,
        'learnable_by': ['witch', 'magus'],
        'description': 'Massive meteor strike, physical damage',
        'shop_cost': 1800
    },
    'ultima': {
        'name': 'Ultima',
        'level': 7,
        'element': None,  # Non-elemental
        'descriptor': 'magical',
        'target': 'all_enemies',
        'base_damage': 75,
        'learnable_by': ['magus'],
        'description': 'Ultimate non-elemental magic',
        'shop_cost': 2000
    },
    'full_life': {
        'name': 'Full-Life',
        'level': 7,
        'element': 'holy',
        'descriptor': None,
        'target': 'single_dead',
        'resurrection': True,
        'hp_restore': 1.0,  # 100% HP
        'learnable_by': ['saint', 'paladin'],
        'description': 'Resurrects ally with full HP',
        'shop_cost': 1800
    },
    'doom': {
        'name': 'Doom',
        'level': 7,
        'element': 'dark',
        'descriptor': 'magical',
        'target': 'single',
        'status_effect': 'doom',
        'duration': 5,  # Death after 5 turns
        'learnable_by': ['necromancer', 'vampire'],
        'description': 'Enemy dies after 5 turns',
        'shop_cost': 1600
    },
    'judgment': {
        'name': 'Judgment',
        'level': 7,
        'element': 'holy',
        'descriptor': 'magical',
        'target': 'single',
        'base_damage': 80,
        'vs_undead_bonus': 2.0,
        'learnable_by': ['paladin', 'saint'],
        'description': 'Massive holy damage to undead',
        'shop_cost': 1700,
        'ability_unlock': True  # Michael/Paladin level 80
    },
    'plague': {
        'name': 'Plague',
        'level': 7,
        'element': None,
        'descriptor': 'magical',
        'target': 'all_enemies',
        'status_effect': 'poison',
        'duration': 5,
        'base_damage': 35,
        'learnable_by': ['necromancer'],
        'description': 'AoE poison damage',
        'shop_cost': 1500,
        'ability_unlock': True  # Yipp/Necromancer level 70
    },
    'arson': {
        'name': 'Arson',
        'level': 7,
        'element': 'fire',
        'descriptor': 'magical',
        'target': 'all_enemies',
        'base_damage': 65,
        'guaranteed_burn_spread': True,
        'learnable_by': ['arsonist'],
        'description': 'Massive fire + guaranteed Burn spread',
        'shop_cost': 1750,
        'ability_unlock': True  # Crankpot/Arsonist level 80
    },

    # Level 8 Spells
    'meteor_swarm': {
        'name': 'Meteor Swarm',
        'level': 8,
        'element': 'fire',
        'descriptor': 'physical',
        'target': 'all_enemies',
        'base_damage': 85,
        'learnable_by': ['magus'],
        'description': 'Massive fire/physical AoE',
        'shop_cost': 2500,
        'ability_unlock': True  # Hannah/Magus level 80
    },
    'resurrect_all': {
        'name': 'Resurrect All',
        'level': 8,
        'element': 'holy',
        'descriptor': None,
        'target': 'all_dead',
        'resurrection': True,
        'hp_restore': 0.5,
        'learnable_by': ['saint'],
        'description': 'Revives all fallen allies',
        'shop_cost': 2800,
        'ability_unlock': True  # Yipp/Saint level 80
    },

    # Level 9 Spells
    'diamond_dust': {
        'name': 'Diamond Dust',
        'level': 9,
        'element': 'ice',
        'descriptor': 'magical',
        'target': 'all_enemies',
        'base_damage': 95,
        'learnable_by': ['ice_mage'],
        'description': 'Ultimate ice magic',
        'shop_cost': 3500,
        'ability_unlock': True  # Flood level 90
    },
    'sensory_deprivation': {
        'name': 'Sensory Deprivation',
        'level': 9,
        'element': 'nature',
        'descriptor': 'magical',
        'target': 'all_enemies',
        'removes_magic_resistance': True,
        'status_effect': 'silence',
        'duration': 5,
        'learnable_by': ['druidess'],
        'description': 'Removes magic resistance + Silence for 5 turns',
        'shop_cost': 5000,  # Expensive desert exclusive
        'desert_exclusive': True
    },

    # Dreamwalker Exclusive Spells (Psychic - cannot be resisted)
    'dream_heal': {
        'name': 'Dream Heal',
        'level': 3,
        'element': 'psychic',
        'descriptor': None,
        'target': 'single',
        'base_healing': 70,
        'learnable_by': ['dreamwalker'],
        'description': 'Psychic healing spell',
        'shop_cost': 350,
        'ability_unlock': True  # Javin/Dreamwalker level 30
    },
    'dream_shield': {
        'name': 'Dream Shield',
        'level': 4,
        'element': 'psychic',
        'descriptor': None,
        'target': 'single',
        'shield_value': 50,
        'duration': 3,
        'learnable_by': ['dreamwalker'],
        'description': 'Creates psychic shield that absorbs damage',
        'shop_cost': 450,
        'ability_unlock': True  # Javin/Dreamwalker level 60
    },
    'nightmare_bolt': {
        'name': 'Nightmare Bolt',
        'level': 3,
        'element': 'psychic',
        'descriptor': 'psychic',  # CANNOT BE RESISTED
        'target': 'single',
        'base_damage': 45,  # Slightly weaker than normal
        'crit_bonus': 0.15,  # Higher crit chance
        'learnable_by': ['dreamwalker'],
        'description': 'Psychic damage that cannot be resisted',
        'shop_cost': 400
    },
    'nightmare_storm': {
        'name': 'Nightmare Storm',
        'level': 6,
        'element': 'psychic',
        'descriptor': 'psychic',
        'target': 'all_enemies',
        'base_damage': 50,  # Slightly weaker than normal
        'crit_bonus': 0.15,
        'learnable_by': ['dreamwalker'],
        'description': 'AoE psychic damage that cannot be resisted',
        'shop_cost': 1300
    },
    'terror_wave': {
        'name': 'Terror Wave',
        'level': 8,
        'element': 'psychic',
        'descriptor': 'psychic',
        'target': 'all_enemies',
        'base_damage': 80,  # Slightly weaker than normal
        'crit_bonus': 0.20,
        'learnable_by': ['dreamwalker'],
        'description': 'Massive psychic AoE that cannot be resisted',
        'shop_cost': 2700,
        'ability_unlock': True  # Javin/Dreamwalker level 80
    },

    # Druidess Control Spells
    'sandstorm': {
        'name': 'Sandstorm',
        'level': 3,
        'element': 'nature',
        'descriptor': 'magical',
        'target': 'all_enemies',
        'status_effect': 'blind',
        'duration': 4,
        'learnable_by': ['druidess'],
        'description': 'Blinds all enemies',
        'shop_cost': 400,
        'ability_unlock': True  # Cookie/Druidess level 30
    },
    'excessive_vinegrowth': {
        'name': 'Excessive Vinegrowth',
        'level': 4,
        'element': 'nature',
        'descriptor': 'magical',
        'target': 'all_enemies',
        'status_effect': 'slow',
        'duration': 4,
        'learnable_by': ['druidess'],
        'description': 'Slows all enemies',
        'shop_cost': 500,
        'ability_unlock': True  # Cookie/Druidess level 60
    },
    'bubble': {
        'name': 'Bubble',
        'level': 5,
        'element': 'nature',
        'descriptor': 'magical',
        'target': 'single',
        'status_effect': ['silence', 'prevent_attack'],
        'breaks_on_hit': True,
        'learnable_by': ['druidess'],
        'description': 'Silence + prevents attack, pops when hit',
        'shop_cost': 650,
        'ability_unlock': True  # Cookie/Druidess level 80
    }
}

# Magic shop inventories by location
MAGIC_SHOPS = {
    'imperial_city_1': {
        'location': 'Imperial City - First Visit',
        'spells': ['fire', 'cure', 'thunder', 'blizzard', 'drain', 'fira', 'cura', 'thundara', 'blizzara', 'sleep']
    },
    'imperial_city_2': {
        'location': 'Imperial City - Second Visit',
        'spells': ['firaga', 'curaga', 'thundaga', 'blizzaga', 'poison', 'bio', 'haste', 'slow', 'protect', 'shell', 'confuse']
    },
    'army_camp': {
        'location': 'Army Camp',
        'spells': ['raise', 'esuna', 'quake', 'tornado', 'flare', 'holy', 'blizzaja', 'thundaja']
    },
    'desert_vendor_1': {
        'location': 'Desert - Abandoned Town 1',
        'spells': ['meteor', 'ultima', 'full_life', 'doom', 'sensory_deprivation'],
        'price_multiplier': 1.5  # 50% markup
    },
    'desert_vendor_2': {
        'location': 'Desert - Abandoned Town 2',
        'spells': ['nightmare_bolt', 'nightmare_storm', 'terror_wave', 'sandstorm', 'excessive_vinegrowth', 'bubble'],
        'price_multiplier': 1.5
    }
}

def can_character_learn_spell(character_class, spell_id):
    """Check if a character class can learn a specific spell"""
    spell = SPELLS.get(spell_id)
    if not spell:
        return False

    return character_class in spell.get('learnable_by', [])

def get_spell_cost(spell_id, shop_location=None):
    """Get the cost of a spell, accounting for shop markup"""
    spell = SPELLS.get(spell_id)
    if not spell:
        return 0

    base_cost = spell['shop_cost']

    if shop_location:
        shop = MAGIC_SHOPS.get(shop_location, {})
        multiplier = shop.get('price_multiplier', 1.0)
        return int(base_cost * multiplier)

    return base_cost

def calculate_spell_damage(spell_id, caster_magic_power, target_spell_resistance=0, caster_bonuses=None):
    """
    Calculate spell damage

    Args:
        spell_id: Spell identifier
        caster_magic_power: Caster's magic power stat
        target_spell_resistance: Target's spell resistance stat (0 if psychic)
        caster_bonuses: Dict of caster bonuses (elemental damage, etc.)

    Returns:
        Final damage value
    """
    spell = SPELLS.get(spell_id)
    if not spell or 'base_damage' not in spell:
        return 0

    base_damage = spell['base_damage']
    element = spell.get('element')
    descriptor = spell.get('descriptor')

    # Calculate base damage with magic power
    damage = base_damage + (caster_magic_power * 0.5)

    # Apply elemental bonuses
    if caster_bonuses and element:
        element_bonus_key = f'{element}_damage'
        if element_bonus_key in caster_bonuses:
            damage *= (1 + caster_bonuses[element_bonus_key])

    # Apply psychic damage rules
    if descriptor == 'psychic':
        # Psychic damage CANNOT BE RESISTED
        # Slightly weaker but higher crit chance
        pass  # No resistance applied
    elif descriptor == 'magical':
        # Normal magical damage reduced by spell resistance
        resistance_reduction = target_spell_resistance * 0.5
        damage = max(1, damage - resistance_reduction)

    return int(damage)

def calculate_spell_healing(spell_id, caster_magic_power, caster_bonuses=None):
    """Calculate spell healing amount"""
    spell = SPELLS.get(spell_id)
    if not spell or 'base_healing' not in spell:
        return 0

    base_healing = spell['base_healing']
    healing = base_healing + (caster_magic_power * 0.4)

    # Apply healing bonuses
    if caster_bonuses and 'healing_bonus' in caster_bonuses:
        healing *= (1 + caster_bonuses['healing_bonus'])

    return int(healing)
