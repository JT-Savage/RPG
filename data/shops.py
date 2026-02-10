"""
Shop Data
All shops in the game
"""

SHOPS = {
    # === Imperial City ===

    'imperial_item_shop': {
        'name': 'Imperial Item Shop',
        'type': 'item',
        'location': 'imperial_city',
        'items': [
            'potion',
            'hi_potion',
            'ether',
            'hi_ether',
            'antidote',
            'eye_drops',
            'echo_screen',
            'remedy',
            'phoenix_down',
            'tent',
            'cottage'
        ]
    },

    'imperial_weapon_shop': {
        'name': 'Imperial Weapon & Armor',
        'type': 'equipment',
        'location': 'imperial_city',
        'equipment': [
            'iron_sword',
            'iron_spear',
            'iron_axe',
            'oak_staff',
            'hunting_bow',
            'leather_armor',
            'chain_mail',
            'iron_helm',
            'iron_shield'
        ]
    },

    'imperial_magic_shop': {
        'name': 'Imperial Magic Shop',
        'type': 'magic',
        'location': 'imperial_city',
        'spells': [
            'fire',
            'ice',
            'lightning',
            'cure',
            'poisona',
            'protect',
            'shell'
        ],
        'description': 'Learn spells for your magic users!'
    },

    # === Starting Town ===

    'starter_item_shop': {
        'name': 'General Store',
        'type': 'item',
        'location': 'starter_town',
        'items': [
            'potion',
            'antidote',
            'tent'
        ]
    },

    'starter_equipment_shop': {
        'name': 'Blacksmith',
        'type': 'equipment',
        'location': 'starter_town',
        'equipment': [
            'bronze_sword',
            'bronze_spear',
            'wooden_staff',
            'cloth_armor',
            'leather_cap'
        ]
    },

    # === Army Camp ===

    'army_camp_shop': {
        'name': 'Army Quartermaster',
        'type': 'general',
        'location': 'army_camp',
        'items': [
            'potion',
            'hi_potion',
            'ether',
            'antidote',
            'phoenix_down'
        ],
        'equipment': [
            'steel_sword',
            'steel_spear',
            'steel_axe',
            'plate_mail',
            'steel_helm'
        ]
    },

    # === Desert Outpost ===

    'desert_item_shop': {
        'name': 'Desert Trader',
        'type': 'item',
        'location': 'desert_outpost',
        'items': [
            'hi_potion',
            'x_potion',
            'hi_ether',
            'mega_ether',
            'remedy',
            'phoenix_down',
            'elixir'
        ]
    },

    'desert_weapon_shop': {
        'name': 'Desert Armory',
        'type': 'equipment',
        'location': 'desert_outpost',
        'equipment': [
            'mythril_sword',
            'mythril_spear',
            'mythril_axe',
            'flame_staff',
            'mythril_armor',
            'mythril_helm',
            'mythril_shield'
        ]
    },

    'desert_magic_shop': {
        'name': 'Desert Mage',
        'type': 'magic',
        'location': 'desert_outpost',
        'spells': [
            'fira',
            'blizzara',
            'thundara',
            'cura',
            'raise',
            'esuna',
            'haste',
            'slow'
        ]
    },

    # === Late Game ===

    'endgame_item_shop': {
        'name': 'Master Merchant',
        'type': 'item',
        'location': 'final_town',
        'items': [
            'x_potion',
            'mega_potion',
            'mega_ether',
            'elixir',
            'megalixir',
            'remedy',
            'phoenix_down'
        ]
    },

    'endgame_weapon_shop': {
        'name': 'Legendary Forge',
        'type': 'equipment',
        'location': 'final_town',
        'equipment': [
            'diamond_sword',
            'holy_lance',
            'great_axe',
            'sage_staff',
            'ultima_bow',
            'diamond_armor',
            'genji_helm',
            'aegis_shield'
        ]
    },

    'endgame_magic_shop': {
        'name': 'Archmage\'s Tower',
        'type': 'magic',
        'location': 'final_town',
        'spells': [
            'firaga',
            'blizzaga',
            'thundaga',
            'curaga',
            'full-life',
            'flare',
            'holy',
            'ultima'
        ]
    },

    # === Special Shops ===

    'traveling_merchant': {
        'name': 'Traveling Merchant',
        'type': 'general',
        'location': 'random',
        'items': [
            'potion',
            'ether',
            'phoenix_down',
            'tent'
        ],
        'equipment': [
            'traveler_cloak',
            'lucky_ring'
        ],
        'description': 'Rare items for the adventurous!'
    },

    'black_market': {
        'name': 'Black Market',
        'type': 'item',
        'location': 'hidden',
        'items': [
            'smoke_bomb',
            'poison_powder',
            'sleeping_powder',
            'mega_ether',
            'elixir'
        ],
        'description': 'Don\'t ask where these came from...'
    }
}

# Shop availability by story flags
SHOP_CONDITIONS = {
    'imperial_item_shop': {
        'required_flags': ['imperial_city_visited']
    },
    'imperial_weapon_shop': {
        'required_flags': ['imperial_city_visited']
    },
    'imperial_magic_shop': {
        'required_flags': ['imperial_city_visited']
    },
    'desert_item_shop': {
        'required_flags': ['desert_entered']
    },
    'desert_weapon_shop': {
        'required_flags': ['desert_entered']
    },
    'desert_magic_shop': {
        'required_flags': ['desert_entered']
    },
    'endgame_item_shop': {
        'required_flags': ['necromancer_defeated']
    },
    'endgame_weapon_shop': {
        'required_flags': ['necromancer_defeated']
    },
    'endgame_magic_shop': {
        'required_flags': ['necromancer_defeated']
    }
}

def get_available_shops(location, story_flags):
    """
    Get available shops at location

    Args:
        location: Location identifier
        story_flags: Story flags dict

    Returns:
        list: Available shop IDs
    """
    available = []

    for shop_id, shop_data in SHOPS.items():
        # Check location
        if shop_data['location'] != location and shop_data['location'] != 'random':
            continue

        # Check conditions
        conditions = SHOP_CONDITIONS.get(shop_id)
        if conditions:
            # Check required flags
            required_flags = conditions.get('required_flags', [])
            if not all(story_flags.get(flag) for flag in required_flags):
                continue

            # Check forbidden flags
            forbidden_flags = conditions.get('forbidden_flags', [])
            if any(story_flags.get(flag) for flag in forbidden_flags):
                continue

        available.append(shop_id)

    return available
