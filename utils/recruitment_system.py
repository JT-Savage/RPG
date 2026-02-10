"""
Recruitment System
Handles character recruitment with dialogue loops and deadline mechanics
"""

from data.characters import CHARACTERS

class RecruitmentSystem:
    """Manages character recruitment"""

    def __init__(self, game_state):
        self.game_state = game_state

    def is_character_recruitable(self, char_id):
        """
        Check if character can be recruited now

        Args:
            char_id: Character identifier

        Returns:
            bool: Can recruit
        """
        # Check if already recruited
        if char_id in self.game_state.characters_recruited:
            return False

        # Check if recruitment deadline passed
        if self.game_state.story_flags.get('recruitment_deadline_passed'):
            return False

        # Check story flags for this character
        char_data = CHARACTERS.get(char_id)
        if not char_data:
            return False

        recruitment_location = char_data.get('recruitment_location')

        # Check location-specific requirements
        if recruitment_location == 'lycanthrope_battle':
            return self.game_state.story_flags.get('met_frostbite', False)

        elif recruitment_location == 'caravan_battle':
            return self.game_state.story_flags.get('met_fei', False)

        elif recruitment_location == 'imperial_city':
            return self.game_state.story_flags.get('imperial_city_visited', False)

        elif recruitment_location == 'halfling_rescue':
            return self.game_state.story_flags.get('cookie_iris_rescued', False)

        elif recruitment_location == 'imperial_city_inn':
            # Fritzzit and Crankpot
            if char_id in ['fritzzit', 'crankpot']:
                # Only available after kobolds released, before Orisia
                return (self.game_state.story_flags.get('kobolds_released', False) and
                        not self.game_state.story_flags.get('met_orisia', False))

        elif recruitment_location == 'random_dungeon_pre_orisia':
            # Yipp
            if char_id == 'yipp':
                # Check if in correct dungeon and haven't met Orisia
                return (not self.game_state.story_flags.get('met_orisia', False) and
                        not self.game_state.story_flags.get('yipp_encountered', False))

        elif recruitment_location == 'undead_lands':
            # Warghoul - optional early, required by army camp
            return True

        return False

    def get_recruitment_dialogue(self, char_id):
        """
        Get recruitment dialogue for character

        Args:
            char_id: Character identifier

        Returns:
            dict: Dialogue data
        """
        dialogues = {
            'frostbite': {
                'greeting': 'A gunner, eh? Those lycanthropes didn\'t stand a chance.',
                'question': 'I could use someone like you. Want to join?',
                'accept': 'Good. Let\'s move.',
                'decline': 'Suit yourself. I\'ll be around if you change your mind.',
                'location': 'After lycanthrope battle'
            },

            'fei': {
                'greeting': 'You fight well. Those bandits never saw it coming.',
                'question': 'I\'m heading the same direction. Want to travel together?',
                'accept': 'Excellent! Your caravan is in good paws.',
                'decline': 'No problem. Find me at the caravan if you change your mind.',
                'location': 'After caravan battle'
            },

            'michael': {
                'greeting': 'Blessings, traveler. I sense great trials ahead of you.',
                'question': 'Would you allow a humble cleric to accompany you?',
                'accept': 'Thank you. My healing magic is yours.',
                'decline': 'I understand. I\'ll be at the cathedral if you need me.',
                'location': 'Imperial City'
            },

            'flood': {
                'greeting': 'Ice magic user here. I heard about the kobold plague.',
                'question': 'I want to help stop this. Can I join you?',
                'accept': 'Perfect. Let\'s freeze some undead.',
                'decline': 'Alright. I\'ll be studying at the library.',
                'location': 'Imperial City'
            },

            'hannah': {
                'greeting': 'You\'re investigating the necromantic plague? Me too.',
                'question': 'We should work together. What do you say?',
                'accept': 'Great! My elemental magic will be useful.',
                'decline': 'Your loss. I\'ll be at the magic shop.',
                'location': 'Imperial City'
            },

            'warghoul': {
                'greeting': 'You don\'t fear the undead? Interesting.',
                'question': 'I seek to end this plague as well. Let me join you.',
                'accept': 'Good. The dead will serve us.',
                'decline': 'Very well. I will wait in the undead lands.',
                'location': 'Undead Lands'
            },

            'cookie': {
                'greeting': 'Thank you for saving us! That was terrifying.',
                'question': 'Want me to come with you? I\'m good with nature magic!',
                'accept': 'Yay! I won\'t let you down!',
                'decline': 'Oh... okay. I\'ll be at the inn if you need me.',
                'location': 'After halfling rescue'
            },

            'iris': {
                'greeting': 'You saved us! You\'re so brave!',
                'question': 'Can I join you? I want to help! ...And pet the panda.',
                'accept': 'YES! Thank you! *tries to hug Fei*',
                'decline': 'Aww... I\'ll be with Cookie at the inn.',
                'location': 'After halfling rescue'
            },

            'fritzzit': {
                'greeting': 'Goblin sniper at your service. This is Crankpot.',
                'question': 'We both want to help. We\'re a package deal. What do you say?',
                'accept': 'Excellent! You won\'t regret this.',
                'decline': 'Understood. We\'ll stay at the inn.',
                'location': 'Imperial City Inn',
                'paired_with': 'crankpot'
            },

            'crankpot': {
                'greeting': '...Fire mage. I specialize in... burning things.',
                'question': 'Fritzzit and I work together. Both or neither.',
                'accept': 'Good. Let\'s get to work.',
                'decline': 'Fine. We\'ll be at the inn.',
                'location': 'Imperial City Inn',
                'paired_with': 'fritzzit'
            },

            'yipp': {
                'greeting': '*panting* Thanks for the save! Those undead almost had me!',
                'question': 'I\'m a necromancer trying to STOP the plague. Can I join you?',
                'accept': 'Thank you! I\'ll prove I\'m one of the good ones!',
                'decline': 'I understand. I\'ll be at the magic shop in the city.',
                'location': 'Random dungeon encounter'
            }
        }

        return dialogues.get(char_id, {
            'greeting': f'{char_id} stands before you.',
            'question': 'Can I join you?',
            'accept': 'Thank you!',
            'decline': 'I understand.',
            'location': 'Unknown'
        })

    def attempt_recruitment(self, char_id, player_choice):
        """
        Attempt to recruit character

        Args:
            char_id: Character identifier
            player_choice: 'yes' or 'no'

        Returns:
            dict: Recruitment result
        """
        if not self.is_character_recruitable(char_id):
            return {
                'success': False,
                'reason': 'not_recruitable',
                'message': 'This character cannot be recruited right now.'
            }

        char_data = CHARACTERS.get(char_id)
        if not char_data:
            return {
                'success': False,
                'reason': 'invalid_character'
            }

        if player_choice.lower() == 'yes':
            # Special handling for paired recruitment (Fritzzit & Crankpot)
            if char_id in ['fritzzit', 'crankpot']:
                return self._recruit_paired_characters('fritzzit', 'crankpot')

            # Normal recruitment
            success = self.game_state.recruit_character(char_id)

            if success:
                # Set recruitment flag
                if char_id == 'frostbite':
                    self.game_state.story_flags['met_frostbite'] = True
                elif char_id == 'fei':
                    self.game_state.story_flags['met_fei'] = True
                elif char_id == 'yipp':
                    self.game_state.story_flags['yipp_encountered'] = True

                return {
                    'success': True,
                    'char_id': char_id,
                    'message': self.get_recruitment_dialogue(char_id)['accept']
                }

            return {
                'success': False,
                'reason': 'recruitment_failed'
            }

        else:  # player_choice == 'no'
            # Character stays at location
            return {
                'success': False,
                'reason': 'player_declined',
                'message': self.get_recruitment_dialogue(char_id)['decline'],
                'can_retry': True
            }

    def _recruit_paired_characters(self, char1_id, char2_id):
        """
        Recruit paired characters (Fritzzit & Crankpot)

        Args:
            char1_id: First character
            char2_id: Second character

        Returns:
            dict: Recruitment result
        """
        # Both must be recruited together
        success1 = self.game_state.recruit_character(char1_id)
        success2 = self.game_state.recruit_character(char2_id)

        if success1 and success2:
            return {
                'success': True,
                'char_id': [char1_id, char2_id],
                'message': f'{char1_id.title()} and {char2_id.title()} have joined the party!',
                'paired': True
            }

        # Shouldn't happen, but rollback if failed
        if success1:
            self.game_state.characters_recruited.remove(char1_id)
        if success2:
            self.game_state.characters_recruited.remove(char2_id)

        return {
            'success': False,
            'reason': 'paired_recruitment_failed'
        }

    def get_backup_recruitment_location(self, char_id):
        """
        Get backup recruitment location for character

        Args:
            char_id: Character identifier

        Returns:
            str: Location or None
        """
        char_data = CHARACTERS.get(char_id)
        if not char_data:
            return None

        backup_locations = char_data.get('backup_locations', [])
        if not backup_locations:
            return None

        # Check which backup location is accessible
        if 'army_camp' in backup_locations:
            if self.game_state.current_location == 'army_camp':
                return 'army_camp'

        if 'imperial_city_inn' in backup_locations:
            if self.game_state.story_flags.get('imperial_city_visited'):
                return 'imperial_city_inn'

        if 'imperial_city_magic_shop' in backup_locations:
            if self.game_state.story_flags.get('imperial_city_visited'):
                return 'imperial_city_magic_shop'

        return None

    def close_recruitment_window(self):
        """
        Close recruitment window (Orisia says YES to desert)
        All un-recruited optional characters become lost
        """
        self.game_state.close_recruitment()

        # Get list of lost characters
        lost = []
        for char_id, char_data in CHARACTERS.items():
            if not char_data['required'] and char_id not in self.game_state.characters_recruited:
                lost.append(char_id)

        return {
            'recruitment_closed': True,
            'lost_characters': lost,
            'message': 'Recruitment window closed. Un-recruited characters will become zombies in final battle.'
        }

    def warn_recruitment_deadline(self):
        """
        Warn player about recruitment deadline (Orisia meeting)

        Returns:
            dict: Warning message
        """
        if self.game_state.story_flags.get('orisia_ready_warning_given'):
            return None

        self.game_state.story_flags['orisia_ready_warning_given'] = True

        # Count un-recruited optional characters
        missing = []
        for char_id, char_data in CHARACTERS.items():
            if not char_data['required'] and char_id not in self.game_state.characters_recruited:
                missing.append(char_id)

        if missing:
            return {
                'warning': True,
                'missing_characters': missing,
                'message': f'Orisia: "Are you ready to enter the final area? You cannot return until the evil is defeated. {len(missing)} potential allies remain unfound."'
            }

        return {
            'warning': False,
            'message': 'Orisia: "Are you ready to enter the final area? You cannot return until the evil is defeated."'
        }

    def get_yipp_spawn_dungeon(self):
        """
        Get which dungeon Yipp spawns in

        Returns:
            str: Dungeon name
        """
        return self.game_state.story_flags.get('yipp_spawn_dungeon')

    def trigger_yipp_encounter(self):
        """
        Trigger Yipp dungeon encounter

        Returns:
            dict: Encounter data
        """
        if self.game_state.story_flags.get('met_orisia'):
            return {
                'success': False,
                'reason': 'too_late',
                'message': 'Yipp can only be found before meeting Orisia.'
            }

        if self.game_state.story_flags.get('yipp_encountered'):
            return {
                'success': False,
                'reason': 'already_encountered'
            }

        # Check New Game+ for Frostbite comment
        ng_plus = self.game_state.ng_plus_data
        previous_yipp_dungeon = ng_plus.get('yipp_spawn_dungeon') if ng_plus else None

        encounter = {
            'success': True,
            'dungeon': self.get_yipp_spawn_dungeon(),
            'sequence': [
                'You enter the room...',
                'A ratling is fighting undead enemies!',
                'He\'s losing badly!',
                '[Battle starts with Yipp as NPC ally]'
            ]
        }

        # New Game+ Easter egg
        if previous_yipp_dungeon == self.game_state.current_location:
            encounter['frostbite_comment'] = 'Frostbite: "Why does this smell like dead rat?"'

        return encounter

    def is_recruitment_available(self):
        """
        Check if any recruitment is still available

        Returns:
            bool: Recruitment available
        """
        if self.game_state.story_flags.get('recruitment_deadline_passed'):
            return False

        # Check if any optional characters remain
        for char_id, char_data in CHARACTERS.items():
            if not char_data['required'] and char_id not in self.game_state.characters_recruited:
                return True

        return False

    def get_available_recruits(self):
        """
        Get list of characters available for recruitment

        Returns:
            list: Character IDs
        """
        available = []

        for char_id in CHARACTERS:
            if self.is_character_recruitable(char_id):
                available.append(char_id)

        return available

    def get_missing_optional_characters(self):
        """
        Get list of optional characters not yet recruited

        Returns:
            list: Character IDs
        """
        missing = []

        for char_id, char_data in CHARACTERS.items():
            if not char_data['required'] and char_id not in self.game_state.characters_recruited:
                missing.append(char_id)

        return missing
