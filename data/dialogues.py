"""
Dialogue Data
All NPC dialogues, story conversations, and recruitment dialogues
"""

from utils.dialogue_system import create_recruitment_dialogue, create_simple_dialogue

# Main dialogue database
DIALOGUES = {}

# === Recruitment Dialogues ===

DIALOGUES['recruit_frostbite'] = create_recruitment_dialogue(
    'frostbite',
    greeting='A gunner, eh? Those lycanthropes didn\'t stand a chance.',
    question='I could use someone like you. Want to join?',
    accept_text='Good. Let\'s move.',
    decline_text='Suit yourself. I\'ll be around if you change your mind.'
)

DIALOGUES['recruit_fei'] = create_recruitment_dialogue(
    'fei',
    greeting='You fight well. Those bandits never saw it coming.',
    question='I\'m heading the same direction. Want to travel together?',
    accept_text='Excellent! Your caravan is in good paws.',
    decline_text='No problem. Find me at the caravan if you change your mind.'
)

DIALOGUES['recruit_michael'] = create_recruitment_dialogue(
    'michael',
    greeting='Blessings, traveler. I sense great trials ahead of you.',
    question='Would you allow a humble cleric to accompany you?',
    accept_text='Thank you. My healing magic is yours.',
    decline_text='I understand. I\'ll be at the cathedral if you need me.'
)

DIALOGUES['recruit_flood'] = create_recruitment_dialogue(
    'flood',
    greeting='Ice magic user here. I heard about the kobold plague.',
    question='I want to help stop this. Can I join you?',
    accept_text='Perfect. Let\'s freeze some undead.',
    decline_text='Alright. I\'ll be studying at the library.'
)

DIALOGUES['recruit_hannah'] = create_recruitment_dialogue(
    'hannah',
    greeting='You\'re investigating the necromantic plague? Me too.',
    question='We should work together. What do you say?',
    accept_text='Great! My elemental magic will be useful.',
    decline_text='Your loss. I\'ll be at the magic shop.'
)

DIALOGUES['recruit_warghoul'] = create_recruitment_dialogue(
    'warghoul',
    greeting='You don\'t fear the undead? Interesting.',
    question='I seek to end this plague as well. Let me join you.',
    accept_text='Good. The dead will serve us.',
    decline_text='Very well. I will wait in the undead lands.'
)

DIALOGUES['recruit_cookie'] = create_recruitment_dialogue(
    'cookie',
    greeting='Thank you for saving us! That was terrifying.',
    question='Want me to come with you? I\'m good with nature magic!',
    accept_text='Yay! I won\'t let you down!',
    decline_text='Oh... okay. I\'ll be at the inn if you need me.'
)

DIALOGUES['recruit_iris'] = create_recruitment_dialogue(
    'iris',
    greeting='You saved us! You\'re so brave!',
    question='Can I join you? I want to help! ...And pet the panda.',
    accept_text='YES! Thank you! *tries to hug Fei*',
    decline_text='Aww... I\'ll be with Cookie at the inn.'
)

DIALOGUES['recruit_fritzzit_crankpot'] = {
    'nodes': [
        {
            'speaker': 'fritzzit',
            'text': 'Goblin sniper at your service. This is Crankpot.',
            'next_node': 1
        },
        {
            'speaker': 'crankpot',
            'text': '...Fire mage. I specialize in... burning things.',
            'next_node': 2
        },
        {
            'speaker': 'fritzzit',
            'text': 'We both want to help. We\'re a package deal. What do you say?',
            'choices': [
                {
                    'text': 'Yes',
                    'effects': {
                        'recruit_character': 'fritzzit',
                        'set_flag': 'fritzzit_recruited'
                    },
                    'next_node': 3
                },
                {
                    'text': 'No',
                    'next_node': 4
                }
            ]
        },
        {
            'speaker': 'fritzzit',
            'text': 'Excellent! You won\'t regret this.',
            'next_node': 5
        },
        {
            'speaker': 'fritzzit',
            'text': 'Understood. We\'ll stay at the inn.',
            'next_node': 2  # Loop back
        },
        {
            'speaker': 'crankpot',
            'text': 'Good. Let\'s get to work.'
        }
    ]
}

DIALOGUES['recruit_yipp'] = create_recruitment_dialogue(
    'yipp',
    greeting='*panting* Thanks for the save! Those undead almost had me!',
    question='I\'m a necromancer trying to STOP the plague. Can I join you?',
    accept_text='Thank you! I\'ll prove I\'m one of the good ones!',
    decline_text='I understand. I\'ll be at the magic shop in the city.'
)

# === Story Dialogues ===

DIALOGUES['intro_tutorial'] = {
    'nodes': [
        {
            'speaker': 'narrator',
            'text': 'Deep beneath the earth, kobolds work in the warrens...',
            'next_node': 1
        },
        {
            'speaker': 'narrator',
            'text': 'But something is wrong. A necromantic plague spreads...',
            'next_node': 2
        },
        {
            'speaker': 'narrator',
            'text': 'Infected kobolds rise as undead. You must escape!',
            'next_node': 3
        },
        {
            'speaker': 'frostbite',
            'text': 'We need to get out of here. Follow me!'
        }
    ]
}

DIALOGUES['tutorial_battle'] = create_simple_dialogue(
    'frostbite',
    [
        'Infected kobolds ahead! Get ready to fight!',
        'Use Attack to deal physical damage.',
        'Magic spells can hit multiple enemies.',
        'Don\'t forget to Defend when low on HP!'
    ]
)

DIALOGUES['warren_escape'] = create_simple_dialogue(
    'frostbite',
    [
        'We made it to the surface!',
        'But the infection will spread if we don\'t stop it.',
        'We need to find allies and discover the source.'
    ]
)

DIALOGUES['imperial_city_arrival'] = {
    'nodes': [
        {
            'speaker': 'guard',
            'text': 'Halt! State your business in the Imperial City.',
            'next_node': 1
        },
        {
            'speaker': 'frostbite',
            'text': 'We need to report a necromantic outbreak in the warrens.',
            'next_node': 2
        },
        {
            'speaker': 'guard',
            'text': 'Another one? The Emperor has been dealing with outbreaks all over...',
            'next_node': 3
        },
        {
            'speaker': 'guard',
            'text': 'Enter. The magic shop and cathedral might have information.',
        }
    ],
    'completion_effects': {
        'set_flag': 'imperial_city_visited'
    }
}

DIALOGUES['fei_death_iris_berserk'] = {
    'nodes': [
        {
            'speaker': 'iris',
            'text': 'FEI! NO!',
            'next_node': 1
        },
        {
            'speaker': 'narrator',
            'text': 'Iris\'s eyes glow with primal rage...',
            'next_node': 2
        },
        {
            'speaker': 'iris',
            'text': 'I\'LL KILL YOU!!!',
        }
    ],
    'completion_effects': {
        'trigger_iris_berserk': True
    }
}

DIALOGUES['flood_sacrifice'] = {
    'nodes': [
        {
            'speaker': 'flood',
            'text': 'The necromancer\'s power is too great...',
            'next_node': 1
        },
        {
            'speaker': 'flood',
            'text': 'I can seal him, but it will cost me my life.',
            'next_node': 2
        },
        {
            'speaker': 'frostbite',
            'text': 'Flood, no! There has to be another way!',
            'next_node': 3
        },
        {
            'speaker': 'flood',
            'text': 'This is the only way. Tell everyone... I\'m sorry.',
            'next_node': 4
        },
        {
            'speaker': 'narrator',
            'text': 'Flood channels all his magic into a final seal...',
        }
    ],
    'completion_effects': {
        'kill_character': 'flood',
        'set_flag': 'flood_sacrificed'
    }
}

DIALOGUES['orisia_desert_warning'] = {
    'nodes': [
        {
            'speaker': 'orisia',
            'text': 'The source of the plague lies in the deep desert.',
            'next_node': 1
        },
        {
            'speaker': 'orisia',
            'text': 'Once you enter, you cannot return until the evil is defeated.',
            'next_node': 2
        },
        {
            'speaker': 'orisia',
            'text': 'Are you ready? Have you gathered all your allies?',
            'choices': [
                {
                    'text': 'Yes, I\'m ready',
                    'effects': {
                        'set_flag': 'desert_entered',
                        'set_flag': 'recruitment_deadline_passed',
                        'teleport': 'desert_region'
                    }
                },
                {
                    'text': 'Not yet',
                    'effects': {}
                }
            ]
        }
    ]
}

DIALOGUES['yipp_alignment_choice'] = {
    'nodes': [
        {
            'speaker': 'mysterious_figure',
            'text': 'Yipp... I can grant you power beyond imagination.',
            'next_node': 1
        },
        {
            'speaker': 'yipp',
            'text': 'Who... who are you?',
            'next_node': 2
        },
        {
            'speaker': 'mysterious_figure',
            'text': 'I am Nosferatu. Accept my gift, and become a vampire.',
            'next_node': 3
        },
        {
            'speaker': 'mysterious_figure',
            'text': 'Or remain weak, a mere necromancer.',
            'next_node': 4
        },
        {
            'speaker': 'yipp',
            'text': 'I... I don\'t know what to do...',
            'next_node': 5
        },
        {
            'speaker': 'narrator',
            'text': 'What should Yipp choose?',
            'choices': [
                {
                    'text': 'Accept vampirism',
                    'effects': {
                        'set_alignment': 'vampire',
                        'character': 'yipp',
                        'set_flag': 'yipp_vampire'
                    },
                    'next_node': 6
                },
                {
                    'text': 'Refuse, stay necromancer',
                    'effects': {
                        'set_alignment': 'necromancer',
                        'character': 'yipp',
                        'set_flag': 'yipp_necromancer'
                    },
                    'next_node': 7
                },
                {
                    'text': 'Reject both, become druid',
                    'effects': {
                        'set_alignment': 'druid',
                        'character': 'yipp',
                        'set_flag': 'yipp_druid'
                    },
                    'next_node': 8
                }
            ]
        },
        {
            'speaker': 'yipp',
            'text': 'I accept your gift, Nosferatu. Give me power!',
        },
        {
            'speaker': 'yipp',
            'text': 'No. I will remain what I am. I don\'t need your power.',
        },
        {
            'speaker': 'yipp',
            'text': 'I reject both paths. I will follow nature\'s way instead.',
        }
    ]
}

DIALOGUES['kella_first_meeting'] = create_simple_dialogue(
    'kella',
    [
        'Greetings, travelers. I am Queen Kella of the Capitol.',
        'The undead plague threatens all our lands.',
        'If you can discover its source, I will reward you greatly.'
    ]
)

DIALOGUES['kella_infected'] = {
    'nodes': [
        {
            'speaker': 'frostbite',
            'text': 'By the gods... Queen Kella!',
            'next_node': 1
        },
        {
            'speaker': 'narrator',
            'text': 'The once-noble queen has been transformed into a monster.',
            'next_node': 2
        },
        {
            'speaker': 'kella',
            'text': '...help... me...',
            'next_node': 3
        },
        {
            'speaker': 'narrator',
            'text': 'There is only one mercy you can give her now.',
        }
    ]
}

DIALOGUES['final_boss_intro'] = {
    'nodes': [
        {
            'speaker': 'necromancer_lich',
            'text': 'So... you\'ve made it this far.',
            'next_node': 1
        },
        {
            'speaker': 'necromancer_lich',
            'text': 'But you\'re too late. My army is complete!',
            'next_node': 2
        },
        {
            'speaker': 'frostbite',
            'text': 'We\'ll stop you, no matter what it takes!',
            'next_node': 3
        },
        {
            'speaker': 'necromancer_lich',
            'text': 'You recognize these faces? Your lost allies serve ME now!',
        }
    ],
    'completion_effects': {
        'start_battle': 'final_boss'
    }
}

DIALOGUES['captain_donald_reveal'] = create_simple_dialogue(
    'captain_donald',
    [
        'YOU! You\'re the ones who ruined everything!',
        'I was going to sell those kobolds for a fortune!',
        'But you HAD to be heroes and release them!',
        'Now you\'ll PAY for my lost profits!'
    ]
)

DIALOGUES['game_ending_good'] = {
    'nodes': [
        {
            'speaker': 'narrator',
            'text': 'The necromancer has been defeated. The plague is ended.',
            'next_node': 1
        },
        {
            'speaker': 'frostbite',
            'text': 'We did it. The kobolds are free, and the undead are gone.',
            'next_node': 2
        },
        {
            'speaker': 'flood',
            'text': 'Thank you for honoring my sacrifice. The seal held.',
            'next_node': 3
        },
        {
            'speaker': 'narrator',
            'text': 'But one last threat remains...',
        }
    ]
}

# === NPC Dialogues ===

DIALOGUES['inn_keeper'] = create_simple_dialogue(
    'inn_keeper',
    [
        'Welcome to the inn! Rest here to restore HP and MP.',
        'It\'s 50 Gil per night. What do you say?'
    ]
)

DIALOGUES['weapon_shop_owner'] = create_simple_dialogue(
    'weapon_shop_owner',
    [
        'Finest weapons and armor in the Empire!',
        'Looking to buy or sell?'
    ]
)

DIALOGUES['magic_shop_owner'] = create_simple_dialogue(
    'magic_shop_owner',
    [
        'Magical spells and scrolls for sale.',
        'Your mages will need these to grow stronger!'
    ]
)

# Add more dialogues as needed...
