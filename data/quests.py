"""
Quest definitions
Contains all sidequests and their rewards
"""

QUESTS = {
    # === Orisia Sidequests ===
    'recruit_frostbite': {
        'name': 'Recruit Frostbite',
        'description': 'Find and recruit Frostbite on the surface.',
        'rewards': {
            'exp': 200,
            'gil': 100,
        },
        'completion_event': None,
    },
    'recruit_fei': {
        'name': 'Recruit Fei',
        'description': 'Find and recruit Fei.',
        'rewards': {
            'exp': 200,
            'gil': 100,
        },
        'completion_event': None,
    },
    'recruit_fritzzit': {
        'name': 'Recruit Fritzzit',
        'description': 'Recruit Fritzzit and Crankpot.',
        'rewards': {
            'exp': 300,
            'gil': 150,
        },
        'completion_event': None,
    },
    'recruit_warghoul': {
        'name': 'Recruit Warghoul',
        'description': 'Recruit Warghoul before the deadline.',
        'rewards': {
            'exp': 400,
            'gil': 200,
        },
        'completion_event': None,
    },
    'recruit_michael': {
        'name': 'Recruit Michael',
        'description': 'Recruit Michael in the Imperial City.',
        'rewards': {
            'exp': 300,
            'gil': 150,
        },
        'completion_event': None,
    },
    'recruit_flood': {
        'name': 'Recruit Flood',
        'description': 'Recruit Flood in the Imperial City.',
        'rewards': {
            'exp': 300,
            'gil': 150,
        },
        'completion_event': None,
    },
    'recruit_hannah': {
        'name': 'Recruit Hannah',
        'description': 'Recruit Hannah in the Imperial City.',
        'rewards': {
            'exp': 300,
            'gil': 150,
        },
        'completion_event': None,
    },
    'recruit_yipp': {
        'name': "Yipp's Quest",
        'description': "Complete Yipp's dungeon and determine their alignment.",
        'rewards': {
            'exp': 1000,
            'gil': 500,
        },
        'completion_event': 'yipp_quest_complete',
    },

    # === Story Quests ===
    'rescue_cookie_iris': {
        'name': 'Rescue Cookie and Iris',
        'description': 'Rescue the halflings Cookie and Iris.',
        'rewards': {
            'exp': 500,
            'gil': 250,
            'items': {'potion': 3},
        },
        'completion_event': None,
    },
    'jerod_house': {
        'name': "Jerod's House",
        'description': "Explore Jerod's house and stop the threat.",
        'rewards': {
            'exp': 600,
            'gil': 300,
        },
        'completion_event': 'jerod_house_complete',
    },
    'find_the_cure': {
        'name': 'Find the Cure',
        'description': 'Find a cure for the infection plaguing the warren.',
        'rewards': {
            'exp': 2000,
            'gil': 1000,
        },
        'completion_event': 'cure_found_event',
    },
    'kobolds_escape': {
        'name': 'Free the Kobolds',
        'description': 'Release the imprisoned kobolds from the Imperial Warren.',
        'rewards': {
            'exp': 400,
            'gil': 200,
            'items': {'ether': 2},
        },
        'completion_event': None,
    },

    # === Post-credits Quests ===
    'slaver_island': {
        'name': 'Slaver Island',
        'description': 'Confront Captain Donald on Slaver Island.',
        'rewards': {
            'exp': 5000,
            'gil': 2000,
        },
        'completion_event': 'slaver_island_complete',
    },
}
