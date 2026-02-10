"""
Items and consumables data
"""

# Consumable items
ITEMS = {
    # Healing items
    'potion': {
        'name': 'Potion',
        'type': 'healing',
        'target': 'single',
        'effect': {'hp_restore': 50},
        'description': 'Restores 50 HP to one ally',
        'shop_cost': 50,
        'sellable': True,
        'sell_price': 25
    },
    'hi_potion': {
        'name': 'Hi-Potion',
        'type': 'healing',
        'target': 'single',
        'effect': {'hp_restore': 150},
        'description': 'Restores 150 HP to one ally',
        'shop_cost': 200,
        'sellable': True,
        'sell_price': 100
    },
    'x_potion': {
        'name': 'X-Potion',
        'type': 'healing',
        'target': 'single',
        'effect': {'hp_restore': 'full'},
        'description': 'Fully restores HP to one ally',
        'shop_cost': 800,
        'sellable': True,
        'sell_price': 400
    },
    'ether': {
        'name': 'Ether',
        'type': 'mp_restore',
        'target': 'single',
        'effect': {'mp_restore': 50},
        'description': 'Restores 50 MP to one ally',
        'shop_cost': 250,
        'sellable': True,
        'sell_price': 125
    },
    'hi_ether': {
        'name': 'Hi-Ether',
        'type': 'mp_restore',
        'target': 'single',
        'effect': {'mp_restore': 'full'},
        'description': 'Fully restores MP to one ally',
        'shop_cost': 1000,
        'sellable': True,
        'sell_price': 500
    },
    'elixir': {
        'name': 'Elixir',
        'type': 'full_restore',
        'target': 'single',
        'effect': {'hp_restore': 'full', 'mp_restore': 'full'},
        'description': 'Fully restores HP and MP to one ally',
        'shop_cost': 5000,
        'sellable': True,
        'sell_price': 2500
    },

    # Status cure items
    'antidote': {
        'name': 'Antidote',
        'type': 'status_cure',
        'target': 'single',
        'effect': {'removes_status': 'poison'},
        'description': 'Cures poison status',
        'shop_cost': 80,
        'sellable': True,
        'sell_price': 40
    },
    'eye_drops': {
        'name': 'Eye Drops',
        'type': 'status_cure',
        'target': 'single',
        'effect': {'removes_status': 'blind'},
        'description': 'Cures blind status',
        'shop_cost': 80,
        'sellable': True,
        'sell_price': 40
    },
    'echo_herbs': {
        'name': 'Echo Herbs',
        'type': 'status_cure',
        'target': 'single',
        'effect': {'removes_status': 'silence'},
        'description': 'Cures silence status',
        'shop_cost': 120,
        'sellable': True,
        'sell_price': 60
    },
    'remedy': {
        'name': 'Remedy',
        'type': 'status_cure',
        'target': 'single',
        'effect': {'removes_status': 'all'},
        'description': 'Cures all status ailments',
        'shop_cost': 500,
        'sellable': True,
        'sell_price': 250
    },

    # Revival items
    'phoenix_down': {
        'name': 'Phoenix Down',
        'type': 'revival',
        'target': 'single_dead',
        'effect': {'revive': True, 'hp_restore_percent': 0.25},
        'description': 'Revives a fallen ally with 25% HP',
        'shop_cost': 500,
        'sellable': True,
        'sell_price': 250
    },
    'megalixir': {
        'name': 'Megalixir',
        'type': 'full_restore',
        'target': 'all_allies',
        'effect': {'hp_restore': 'full', 'mp_restore': 'full'},
        'description': 'Fully restores HP and MP to all allies',
        'shop_cost': 20000,
        'sellable': True,
        'sell_price': 10000
    },

    # Battle items
    'grenade': {
        'name': 'Grenade',
        'type': 'damage',
        'target': 'all_enemies',
        'effect': {'base_damage': 100, 'element': 'fire'},
        'description': 'Fire damage to all enemies',
        'shop_cost': 300,
        'sellable': True,
        'sell_price': 150
    },
    'smoke_bomb': {
        'name': 'Smoke Bomb',
        'type': 'escape',
        'target': 'party',
        'effect': {'flee': True, 'success_rate': 1.0},
        'description': 'Guarantees escape from battle',
        'shop_cost': 200,
        'sellable': True,
        'sell_price': 100
    }
}

# Item shop inventories by location
ITEM_SHOPS = {
    'imperial_city_1': {
        'location': 'Imperial City - General Store',
        'items': ['potion', 'antidote', 'eye_drops', 'phoenix_down', 'grenade']
    },
    'imperial_city_2': {
        'location': 'Imperial City - Item Emporium',
        'items': ['hi_potion', 'ether', 'remedy', 'phoenix_down', 'smoke_bomb']
    },
    'army_camp': {
        'location': 'Army Camp - Quartermaster',
        'items': ['x_potion', 'hi_ether', 'remedy', 'phoenix_down', 'grenade']
    },
    'desert_vendor': {
        'location': 'Desert - Traveling Merchant',
        'items': ['elixir', 'megalixir', 'remedy', 'phoenix_down'],
        'price_multiplier': 1.5  # 50% markup in desert
    }
}
