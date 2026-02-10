"""
NPC Data
All non-recruitable NPCs
"""

NPCS = {
    # === Guards ===
    'guard_generic': {
        'name': 'Guard',
        'dialogue_id': 'guard_generic',
        'message': 'Stay safe, traveler.'
    },

    'guard_imperial': {
        'name': 'Imperial Guard',
        'dialogue_id': 'guard_imperial',
        'message': 'The Emperor has ordered all citizens to remain vigilant against the undead threat.'
    },

    # === Shop Keepers ===
    'inn_keeper': {
        'name': 'Inn Keeper',
        'dialogue_id': 'inn_keeper',
        'shop_id': None,  # Inn has special interaction
        'message': 'Welcome! Rest here to restore your HP and MP. Only 50 Gil!'
    },

    'weapon_shop_owner': {
        'name': 'Blacksmith',
        'shop_id': 'imperial_weapon_shop',
        'message': 'Best weapons and armor in the Empire!'
    },

    'magic_shop_owner': {
        'name': 'Mage',
        'shop_id': 'imperial_magic_shop',
        'message': 'Spells for your magic users! They won\'t learn themselves!'
    },

    'item_shop_owner': {
        'name': 'Merchant',
        'shop_id': 'imperial_item_shop',
        'message': 'Potions, antidotes, everything you need!'
    },

    # === Quest NPCs ===
    'jerod': {
        'name': 'Jerod',
        'dialogue_id': 'jerod_quest',
        'quest_id': 'jerod_investigation',
        'message': 'My house? Nothing strange there...'
    },

    'dragon_mother': {
        'name': 'Dragon Mother',
        'dialogue_id': 'dragon_mother',
        'quest_id': 'baby_dragon_quest',
        'message': 'My baby! Have you seen my baby dragon?'
    },

    # === Story NPCs ===
    'orisia': {
        'name': 'Orisia',
        'dialogue_id': 'orisia_desert_warning',
        'message': 'The source of the plague lies in the deep desert. Are you ready?'
    },

    'emperor': {
        'name': 'Emperor',
        'dialogue_id': 'emperor_meeting',
        'message': 'This undead plague must be stopped at all costs.'
    },

    'kella': {
        'name': 'Queen Kella',
        'dialogue_id': 'kella_first_meeting',
        'message': 'Welcome, brave adventurers. I have heard of your deeds.'
    },

    # === Random NPCs ===
    'citizen_1': {
        'name': 'Citizen',
        'message': 'Have you heard about the undead in the warrens? Terrifying!'
    },

    'citizen_2': {
        'name': 'Citizen',
        'message': 'The Emperor is doing everything he can to stop the plague.'
    },

    'citizen_3': {
        'name': 'Citizen',
        'message': 'I heard a group of heroes escaped from the warrens. Could that be you?'
    },

    'soldier_1': {
        'name': 'Soldier',
        'message': 'We\'re preparing for a major offensive against the undead.'
    },

    'soldier_2': {
        'name': 'Soldier',
        'message': 'Warghoul over there is a strange one. Says he wants to help us.'
    },

    'priest': {
        'name': 'Priest',
        'dialogue_id': 'priest_healing',
        'message': 'May the light bless you, traveler. I can heal your wounds for a small donation.'
    },

    'scholar': {
        'name': 'Scholar',
        'dialogue_id': 'scholar_lore',
        'message': 'The necromantic arts are forbidden for good reason. This plague proves it.'
    },

    'traveler': {
        'name': 'Traveler',
        'message': 'I\'m getting out of here before the undead arrive!'
    },

    # === Mysterious NPCs ===
    'nosferatu': {
        'name': 'Mysterious Figure',
        'dialogue_id': 'nosferatu_offer',
        'message': 'Power... I can grant you power beyond imagination...'
    },

    'captain_donald': {
        'name': 'Captain Donald',
        'dialogue_id': 'captain_donald_reveal',
        'message': 'You\'ll pay for ruining my business!'
    }
}

# NPC dialogues (simple ones)
NPC_DIALOGUES = {
    'guard_generic': [
        'Stay safe out there.',
        'The undead are everywhere these days.'
    ],

    'guard_imperial': [
        'Halt! State your business.',
        'The city is on high alert.',
        'Move along, citizen.'
    ],

    'priest_healing': [
        'May I heal your wounds? 100 Gil for the party.',
        'The light will restore you.'
    ],

    'scholar_lore': [
        'Necromancy was outlawed centuries ago.',
        'Whoever is behind this plague must be immensely powerful.',
        'The ancient texts speak of a ritual that could end this...'
    ]
}
