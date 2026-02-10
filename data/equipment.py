"""
Equipment data: weapons, armor, shields, and accessories
Includes elemental properties and character restrictions
"""

# Weapon definitions
WEAPONS = {
    # Daggers (Javin, Yipp)
    'rusty_dagger': {
        'name': 'Rusty Dagger',
        'type': 'dagger',
        'attack': 8,
        'equippable_by': ['javin', 'yipp'],
        'shop_cost': 50,
        'description': 'A worn, rusted dagger'
    },
    'iron_dagger': {
        'name': 'Iron Dagger',
        'type': 'dagger',
        'attack': 15,
        'equippable_by': ['javin', 'yipp'],
        'shop_cost': 200,
        'description': 'A basic iron dagger'
    },
    'mythril_dagger': {
        'name': 'Mythril Dagger',
        'type': 'dagger',
        'attack': 30,
        'equippable_by': ['javin', 'yipp'],
        'shop_cost': 1000,
        'description': 'A dagger forged from mythril'
    },
    'assassins_blade': {
        'name': "Assassin's Blade",
        'type': 'dagger',
        'attack': 55,
        'crit_chance_bonus': 0.15,
        'equippable_by': ['javin'],
        'shop_cost': 5000,
        'description': 'Increases critical hit chance'
    },

    # Short Swords (Javin)
    'bronze_sword': {
        'name': 'Bronze Sword',
        'type': 'short_sword',
        'attack': 12,
        'equippable_by': ['javin'],
        'shop_cost': 150,
        'description': 'A basic bronze blade'
    },
    'silver_sword': {
        'name': 'Silver Sword',
        'type': 'short_sword',
        'attack': 25,
        'vs_undead_bonus': 1.25,
        'equippable_by': ['javin'],
        'shop_cost': 800,
        'description': 'Effective against undead'
    },

    # Swords (Fei, Michael, Warghoul)
    'iron_sword': {
        'name': 'Iron Sword',
        'type': 'sword',
        'attack': 18,
        'equippable_by': ['fei', 'michael', 'warghoul'],
        'shop_cost': 250,
        'description': 'A sturdy iron sword'
    },
    'flame_sword': {
        'name': 'Flame Sword',
        'type': 'sword',
        'attack': 35,
        'element': 'fire',
        'equippable_by': ['fei', 'michael', 'warghoul'],
        'shop_cost': 1500,
        'description': 'A sword wreathed in flames'
    },
    'excalibur': {
        'name': 'Excalibur',
        'type': 'sword',
        'attack': 75,
        'element': 'holy',
        'equippable_by': ['fei', 'michael'],
        'shop_cost': 10000,
        'description': 'A legendary holy blade'
    },

    # Axes (Fei, Warghoul)
    'battle_axe': {
        'name': 'Battle Axe',
        'type': 'axe',
        'attack': 40,
        'equippable_by': ['fei', 'warghoul'],
        'shop_cost': 1200,
        'description': 'A heavy two-handed axe'
    },
    'great_axe': {
        'name': 'Great Axe',
        'type': 'axe',
        'attack': 65,
        'crit_damage_bonus': 0.25,
        'equippable_by': ['fei', 'warghoul'],
        'shop_cost': 6000,
        'description': 'Deals extra critical damage'
    },

    # Spears (Fei)
    'bronze_spear': {
        'name': 'Bronze Spear',
        'type': 'spear',
        'attack': 16,
        'equippable_by': ['fei'],
        'shop_cost': 200,
        'description': 'A basic bronze spear'
    },
    'holy_lance': {
        'name': 'Holy Lance',
        'type': 'spear',
        'attack': 60,
        'element': 'holy',
        'vs_undead_bonus': 1.5,
        'equippable_by': ['fei'],
        'shop_cost': 7500,
        'description': 'Devastating against undead'
    },

    # Maces (Michael)
    'wooden_mace': {
        'name': 'Wooden Mace',
        'type': 'mace',
        'attack': 10,
        'equippable_by': ['michael'],
        'shop_cost': 100,
        'description': 'A simple wooden mace'
    },
    'iron_mace': {
        'name': 'Iron Mace',
        'type': 'mace',
        'attack': 22,
        'equippable_by': ['michael'],
        'shop_cost': 400,
        'description': 'A sturdy iron mace'
    },
    'holy_mace': {
        'name': 'Holy Mace',
        'type': 'mace',
        'attack': 50,
        'element': 'holy',
        'magic_power_bonus': 10,
        'equippable_by': ['michael'],
        'shop_cost': 5000,
        'description': 'Increases magic power'
    },

    # Staves (Michael, Flood, Hannah, Cookie, Iris, Yipp, Crankpot)
    'wooden_staff': {
        'name': 'Wooden Staff',
        'type': 'staff',
        'attack': 5,
        'magic_power_bonus': 8,
        'equippable_by': ['michael', 'flood', 'hannah', 'cookie', 'iris', 'yipp', 'crankpot'],
        'shop_cost': 80,
        'description': 'Increases magic power'
    },
    'mythril_staff': {
        'name': 'Mythril Staff',
        'type': 'staff',
        'attack': 12,
        'magic_power_bonus': 18,
        'equippable_by': ['michael', 'flood', 'hannah', 'cookie', 'iris', 'yipp', 'crankpot'],
        'shop_cost': 800,
        'description': 'Greatly increases magic power'
    },
    'fire_rod': {
        'name': 'Fire Rod',
        'type': 'staff',
        'attack': 15,
        'magic_power_bonus': 22,
        'fire_damage_bonus': 0.25,
        'equippable_by': ['hannah', 'crankpot'],
        'shop_cost': 2500,
        'description': 'Boosts fire spell damage'
    },
    'ice_rod': {
        'name': 'Ice Rod',
        'type': 'staff',
        'attack': 15,
        'magic_power_bonus': 22,
        'ice_damage_bonus': 0.25,
        'equippable_by': ['flood', 'hannah'],
        'shop_cost': 2500,
        'description': 'Boosts ice spell damage'
    },
    'holy_staff': {
        'name': 'Holy Staff',
        'type': 'staff',
        'attack': 18,
        'magic_power_bonus': 30,
        'healing_bonus': 0.20,
        'equippable_by': ['michael', 'yipp'],
        'shop_cost': 6000,
        'description': 'Boosts healing spells'
    },

    # Shotguns (Frostbite)
    'basic_shotgun': {
        'name': 'Basic Shotgun',
        'type': 'shotgun',
        'attack': 25,
        'equippable_by': ['frostbite'],
        'shop_cost': 500,
        'description': 'A standard shotgun'
    },
    'double_barrel_shotgun': {
        'name': 'Double-Barrel Shotgun',
        'type': 'shotgun',
        'attack': 45,
        'equippable_by': ['frostbite'],
        'shop_cost': 2000,
        'description': 'Powerful double-barrel design'
    },
    'combat_shotgun': {
        'name': 'Combat Shotgun',
        'type': 'shotgun',
        'attack': 65,
        'equippable_by': ['frostbite'],
        'shop_cost': 7500,
        'description': 'Military-grade shotgun'
    },
    'ultimate_shotgun': {
        'name': 'Ultimate Shotgun',
        'type': 'shotgun',
        'attack': 110,
        'special_ability': 'double_attack',
        'equippable_by': ['frostbite'],
        'not_purchasable': True,
        'sidequest_reward': True,
        'description': 'Frostbite\'s ultimate weapon - attacks twice per turn'
    },

    # Rifles/Sniper Rifles (Fritzzit)
    'hunting_rifle': {
        'name': 'Hunting Rifle',
        'type': 'rifle',
        'attack': 30,
        'crit_chance_bonus': 0.10,
        'equippable_by': ['fritzzit'],
        'shop_cost': 800,
        'description': 'A basic hunting rifle'
    },
    'marksman_rifle': {
        'name': 'Marksman Rifle',
        'type': 'sniper_rifle',
        'attack': 55,
        'crit_chance_bonus': 0.20,
        'equippable_by': ['fritzzit'],
        'shop_cost': 4000,
        'description': 'Precision rifle with high crit chance'
    },
    'anti_material_rifle': {
        'name': 'Anti-Material Rifle',
        'type': 'sniper_rifle',
        'attack': 80,
        'crit_chance_bonus': 0.25,
        'armor_pierce': 0.30,
        'equippable_by': ['fritzzit'],
        'shop_cost': 9000,
        'description': 'Pierces armor and high crit chance'
    },
    'ultimate_sniper_rifle': {
        'name': 'Ultimate Sniper Rifle',
        'type': 'sniper_rifle',
        'attack': 120,
        'crit_chance_bonus': 0.35,
        'special_ability': 'instant_kill_crit',
        'equippable_by': ['fritzzit'],
        'not_purchasable': True,
        'sidequest_reward': True,
        'description': 'Critical hits instantly kill non-boss enemies'
    },

    # Crossbows (Fritzzit)
    'light_crossbow': {
        'name': 'Light Crossbow',
        'type': 'crossbow',
        'attack': 22,
        'equippable_by': ['fritzzit'],
        'shop_cost': 400,
        'description': 'A simple crossbow'
    },

    # Claws (Iris)
    'iron_claws': {
        'name': 'Iron Claws',
        'type': 'claw',
        'attack': 20,
        'equippable_by': ['iris'],
        'shop_cost': 300,
        'description': 'Metal claw weapons'
    },
    'tiger_claws': {
        'name': 'Tiger Claws',
        'type': 'claw',
        'attack': 45,
        'attack_speed_bonus': 0.15,
        'equippable_by': ['iris'],
        'shop_cost': 3000,
        'description': 'Increases attack speed'
    }
}

# Armor definitions
ARMOR = {
    # Light Armor (Javin, Flood, Hannah, Cookie, Iris, Yipp, Crankpot, Fritzzit)
    'leather_armor': {
        'name': 'Leather Armor',
        'type': 'light',
        'defense': 8,
        'equippable_by': ['javin', 'flood', 'hannah', 'cookie', 'iris', 'yipp', 'crankpot', 'fritzzit'],
        'shop_cost': 100,
        'description': 'Basic leather protection'
    },
    'studded_leather': {
        'name': 'Studded Leather',
        'type': 'light',
        'defense': 15,
        'equippable_by': ['javin', 'flood', 'hannah', 'cookie', 'iris', 'yipp', 'crankpot', 'fritzzit'],
        'shop_cost': 400,
        'description': 'Reinforced leather armor'
    },
    'mythril_vest': {
        'name': 'Mythril Vest',
        'type': 'light',
        'defense': 28,
        'spell_resistance_bonus': 10,
        'equippable_by': ['javin', 'flood', 'hannah', 'cookie', 'iris', 'yipp', 'crankpot', 'fritzzit'],
        'shop_cost': 2000,
        'description': 'Light mythril armor with magic resistance'
    },

    # Medium Armor (Frostbite, Fei, Michael)
    'chainmail': {
        'name': 'Chainmail',
        'type': 'medium',
        'defense': 18,
        'equippable_by': ['frostbite', 'fei', 'michael', 'warghoul'],
        'shop_cost': 500,
        'description': 'Standard chain armor'
    },
    'scale_mail': {
        'name': 'Scale Mail',
        'type': 'medium',
        'defense': 30,
        'equippable_by': ['frostbite', 'fei', 'michael', 'warghoul'],
        'shop_cost': 1500,
        'description': 'Layered scale armor'
    },
    'dragon_mail': {
        'name': 'Dragon Mail',
        'type': 'medium',
        'defense': 50,
        'fire_resistance': 0.25,
        'equippable_by': ['frostbite', 'fei', 'michael', 'warghoul'],
        'shop_cost': 8000,
        'description': 'Armor made from dragon scales'
    },

    # Heavy Armor (Fei, Warghoul, Michael as Paladin)
    'iron_armor': {
        'name': 'Iron Armor',
        'type': 'heavy',
        'defense': 25,
        'equippable_by': ['fei', 'warghoul'],
        'shop_cost': 800,
        'description': 'Heavy iron plate armor'
    },
    'knight_armor': {
        'name': 'Knight Armor',
        'type': 'heavy',
        'defense': 40,
        'equippable_by': ['fei', 'warghoul'],
        'shop_cost': 3000,
        'description': 'Full plate knight armor'
    },
    'paladin_armor': {
        'name': 'Paladin Armor',
        'type': 'heavy',
        'defense': 60,
        'spell_resistance_bonus': 20,
        'equippable_by': ['fei', 'warghoul', 'michael'],  # Michael can equip as Paladin
        'requires_class': ['paladin'],  # Michael only
        'shop_cost': 10000,
        'description': 'Holy plate armor for paladins'
    }
}

# Shield definitions
SHIELDS = {
    'wooden_shield': {
        'name': 'Wooden Shield',
        'defense': 5,
        'equippable_by': ['fei', 'michael'],
        'enables_taunt': True,
        'shop_cost': 80,
        'description': 'Basic wooden shield'
    },
    'iron_shield': {
        'name': 'Iron Shield',
        'defense': 12,
        'equippable_by': ['fei', 'michael'],
        'enables_taunt': True,
        'shop_cost': 300,
        'description': 'Sturdy iron shield'
    },
    'mythril_shield': {
        'name': 'Mythril Shield',
        'defense': 22,
        'spell_resistance_bonus': 10,
        'equippable_by': ['fei', 'michael'],
        'enables_taunt': True,
        'shop_cost': 2000,
        'description': 'Mythril shield with magic resistance'
    },
    'hero_shield': {
        'name': 'Hero Shield',
        'defense': 35,
        'spell_resistance_bonus': 15,
        'equippable_by': ['fei', 'michael'],
        'enables_taunt': True,
        'shop_cost': 8000,
        'description': 'Legendary shield of heroes'
    }
}

# Accessory definitions
ACCESSORIES = {
    'power_ring': {
        'name': 'Power Ring',
        'attack_bonus': 10,
        'description': 'Increases attack power',
        'shop_cost': 1000
    },
    'defense_ring': {
        'name': 'Defense Ring',
        'defense_bonus': 10,
        'description': 'Increases defense',
        'shop_cost': 1000
    },
    'magic_ring': {
        'name': 'Magic Ring',
        'magic_power_bonus': 10,
        'description': 'Increases magic power',
        'shop_cost': 1500
    },
    'speed_boots': {
        'name': 'Speed Boots',
        'speed_bonus': 20,
        'description': 'Increases speed',
        'shop_cost': 2000
    },
    'fire_ring': {
        'name': 'Fire Ring',
        'fire_damage_bonus': 0.25,
        'description': 'Boosts fire damage by 25%',
        'shop_cost': 2500
    },
    'ice_ring': {
        'name': 'Ice Ring',
        'ice_damage_bonus': 0.25,
        'description': 'Boosts ice damage by 25%',
        'shop_cost': 2500
    },
    'thunder_ring': {
        'name': 'Thunder Ring',
        'thunder_damage_bonus': 0.25,
        'description': 'Boosts thunder damage by 25%',
        'shop_cost': 2500
    },
    'holy_pendant': {
        'name': 'Holy Pendant',
        'holy_damage_bonus': 0.30,
        'description': 'Boosts holy damage by 30%',
        'shop_cost': 5000
    },
    'anti_poison_charm': {
        'name': 'Anti-Poison Charm',
        'poison_immunity': True,
        'description': 'Grants immunity to poison',
        'shop_cost': 1500
    },
    'ribbon': {
        'name': 'Ribbon',
        'status_immunity': 'all',
        'description': 'Immunity to all status effects',
        'shop_cost': 10000
    }
}

# Special equippable items (Baby Dragon for Javin)
SPECIAL_ITEMS = {
    'baby_dragon': {
        'name': 'Baby Dragon',
        'type': 'special',
        'equippable_by': ['javin'],
        'effect': 'dragon_attack_every_4th_turn',
        'dragon_attack_level': 2,  # Level 2 fire attack
        'nameable': True,
        'description': 'Dragon attacks every 4th turn with fire breath'
    }
}

# Equipment shops by location
EQUIPMENT_SHOPS = {
    'imperial_city_weapon_shop': {
        'location': 'Imperial City - Weapon Shop',
        'weapons': ['iron_sword', 'bronze_sword', 'iron_dagger', 'wooden_mace', 'basic_shotgun', 'hunting_rifle'],
        'special_items': [
            {'item': 'shotgun_blueprint', 'cost': 5000},
            {'item': 'sniper_rifle_blueprint', 'cost': 5000}
        ]
    },
    'imperial_city_armor_shop': {
        'location': 'Imperial City - Armor Shop',
        'armor': ['leather_armor', 'chainmail', 'iron_armor'],
        'shields': ['wooden_shield', 'iron_shield'],
        'accessories': ['power_ring', 'defense_ring', 'anti_poison_charm']
    },
    'army_camp_equipment': {
        'location': 'Army Camp - Armory',
        'weapons': ['flame_sword', 'battle_axe', 'mythril_dagger', 'combat_shotgun', 'marksman_rifle'],
        'armor': ['scale_mail', 'knight_armor', 'mythril_vest'],
        'shields': ['mythril_shield'],
        'accessories': ['magic_ring', 'fire_ring', 'ice_ring', 'thunder_ring']
    },
    'desert_vendor_equipment': {
        'location': 'Desert - Equipment Trader',
        'weapons': ['excalibur', 'great_axe', 'holy_lance', 'anti_material_rifle'],
        'armor': ['dragon_mail', 'paladin_armor'],
        'shields': ['hero_shield'],
        'accessories': ['holy_pendant', 'ribbon', 'speed_boots'],
        'price_multiplier': 1.5
    }
}

def can_character_equip(character_id, equipment_id, equipment_type, character_class=None):
    """
    Check if a character can equip an item

    Args:
        character_id: Character identifier
        equipment_id: Equipment item ID
        equipment_type: 'weapon', 'armor', 'shield', 'accessory'
        character_class: Current class of character (for class-specific items)

    Returns:
        bool: True if can equip
    """
    if equipment_type == 'weapon':
        item = WEAPONS.get(equipment_id)
    elif equipment_type == 'armor':
        item = ARMOR.get(equipment_id)
    elif equipment_type == 'shield':
        item = SHIELDS.get(equipment_id)
    elif equipment_type == 'accessory':
        return True  # Accessories can be equipped by anyone
    elif equipment_type == 'special':
        item = SPECIAL_ITEMS.get(equipment_id)
    else:
        return False

    if not item:
        return False

    # Check if character can equip
    equippable_by = item.get('equippable_by', [])
    if character_id not in equippable_by:
        return False

    # Check class requirements (e.g., Paladin Armor)
    if 'requires_class' in item and character_class:
        if character_class not in item['requires_class']:
            return False

    return True
