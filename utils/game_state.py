"""
Game State Manager
Handles story flags, character progression, and game state
"""

import random
from data.characters import CHARACTERS, get_max_level
from data.key_items import KEY_ITEMS

class GameState:
    """Central game state management"""

    def __init__(self):
        # Initialize all game state
        self.reset_new_game()

    def reset_new_game(self, new_game_plus_data=None):
        """
        Initialize a new game

        Args:
            new_game_plus_data: Optional NG+ data from previous playthrough
        """
        # Is this New Game+?
        self.new_game_plus = new_game_plus_data is not None
        self.playthrough_count = 1
        if new_game_plus_data:
            self.playthrough_count = new_game_plus_data.get('playthrough_count', 1) + 1
            self.ng_plus_data = new_game_plus_data
        else:
            self.ng_plus_data = {}

        # Party management
        self.active_party = ['javin']  # Javin starts in party
        self.reserve_party = []
        self.characters_recruited = ['javin']
        self.lost_characters = []  # Un-recruited characters become zombies

        # Character states
        self.characters = self._initialize_characters(new_game_plus_data)

        # Character classes
        self.character_classes = {char_id: CHARACTERS[char_id]['starting_class'] for char_id in CHARACTERS}

        # Level caps
        self.level_caps = {}
        for char_id in CHARACTERS:
            self.level_caps[char_id] = get_max_level(char_id)

        # Inventory
        self.items = {
            'potion': 5,  # Start with 5 potions
        }
        self.equipment = {}
        self.key_items = []
        self.gil = 100  # Starting money

        # Story flags - CRITICAL
        self.story_flags = {
            # Tutorial
            'tutorial_complete': False,
            'baby_dragon_saved': False,

            # Warren
            'warren_infected': False,
            'kella_went_to_wake_dragons': False,

            # Surface
            'met_frostbite': False,
            'met_fei': False,

            # Imperial City
            'imperial_city_visited': False,
            'shotgun_blueprint_purchased': False,
            'sniper_rifle_blueprint_purchased': False,
            'met_michael': False,
            'met_flood': False,
            'met_hannah': False,

            # Imperial Warren
            'imperial_warren_explored': False,
            'imperial_warren_escape': False,
            'kobolds_released': False,

            # Fritzzit & Crankpot
            'fritzzit_crankpot_available': False,

            # Jerod's House
            'crown_of_flowers_comment_triggered': False,
            'jerod_house_explored': False,
            'jerod_boss_defeated': False,
            'jerod_house_explosion': False,
            'fungal_enemies_removed': False,

            # Halfling rescue
            'cookie_iris_rescued': False,
            'fei_grooming_cutscene': False,
            'panda_fur_available': False,

            # Yipp
            'yipp_dungeon_determined': False,
            'yipp_spawn_dungeon': None,
            'yipp_encountered': False,

            # Warghoul
            'warghoul_recruited_early': False,

            # Orisia
            'met_orisia': False,
            'orisia_ready_warning_given': False,
            'recruitment_deadline_passed': False,

            # Desert
            'desert_entered': False,
            'army_blocks_return': False,

            # Dragon Bosses
            'first_dragon_defeated': False,
            'second_dragon_defeated': False,
            'flood_dead': False,
            'flood_death_cutscene': False,
            'hannah_scream_triggered': False,

            # Catacombs
            'catacombs_unlocked': False,

            # Cure and Endings
            'cure_found': False,
            'kella_saved': False,

            # Final Battle
            'necromancer_defeated': False,
            'yipp_alignment': None,  # 'saint', 'vampire', or None
            'yipp_betrayed': False,

            # Secret Boss
            'kella_double_infected': False,
            'secret_boss_defeated': False,

            # Post-credits
            'post_credits_unlocked': False,
            'slaver_island_completed': False,
            'captain_donald_defeated': False,

            # Ending
            'ending_achieved': None,
        }

        # Orisia sidequests completed
        self.orisia_sidequests_completed = []

        # Ultimate weapons
        self.ultimate_weapons = []

        # Fei and Iris special
        self.fei_dead = False
        self.iris_berserk = False

        # Position
        self.current_location = 'tutorial_warren'
        self.player_position = {'x': 0, 'y': 0}

        # Playtime
        self.playtime_seconds = 0

        # Combat state
        self.in_battle = False

        # Quest tracking
        self.active_quests = []
        self.completed_quests = []

        # Yipp spawn dungeon determination (randomized at game start)
        self._determine_yipp_spawn()

    def _initialize_characters(self, ng_plus_data):
        """
        Initialize character states

        Args:
            ng_plus_data: Optional NG+ data

        Returns:
            dict: Character states
        """
        characters = {}

        for char_id, char_data in CHARACTERS.items():
            # Determine starting level
            if ng_plus_data:
                # New Game+: Start at max available level from previous playthrough
                previous_level = ng_plus_data.get('character_levels', {}).get(char_id, 1)
                previous_class = ng_plus_data.get('character_classes', {}).get(char_id, char_data['starting_class'])

                # Check if they evolved
                evolved = previous_class != char_data['starting_class']

                # Check if they had ultimate weapon
                ultimate_weapon = False
                if char_id in ['frostbite', 'fritzzit']:
                    ultimate_weapon = char_id in ng_plus_data.get('ultimate_weapons', [])

                max_level = get_max_level(char_id, evolved=evolved, has_ultimate_weapon=ultimate_weapon)
                starting_level = min(previous_level, max_level)
            else:
                # Normal start
                starting_level = char_data['initial_level']

            characters[char_id] = {
                'level': starting_level,
                'exp': 0,
                'hp': 0,  # Will be calculated
                'mp': 0,  # Will be calculated
                'max_hp': 0,
                'max_mp': 0,
                'stats': {},
                'equipment': {
                    'weapon': None,
                    'armor': None,
                    'shield': None,
                    'accessory': None,
                    'special': None
                },
                'learned_spells': [],
                'learned_abilities': [],
                'status_effects': []
            }

            # Calculate stats
            self._recalculate_character_stats(char_id, characters[char_id])

        return characters

    def _recalculate_character_stats(self, char_id, char=None):
        """Recalculate character stats based on level"""
        from data.characters import get_character_stats_at_level

        if char is None:
            char = self.characters[char_id]
        level = char['level']

        stats = get_character_stats_at_level(char_id, level)
        char['max_hp'] = int(stats['hp'])
        char['max_mp'] = int(stats['mp'])
        char['stats'] = {
            'attack': int(stats['attack']),
            'defense': int(stats['defense']),
            'magic_power': int(stats['magic_power']),
            'spell_resistance': int(stats['spell_resistance']),
            'speed': int(stats['speed'])
        }

        # Set current HP/MP to max if not set
        if char['hp'] == 0:
            char['hp'] = char['max_hp']
        if char['mp'] == 0:
            char['mp'] = char['max_mp']

    def _determine_yipp_spawn(self):
        """
        Randomly determine which dungeon Yipp will spawn in
        MUST be a pre-Orisia accessible dungeon
        """
        # List of dungeons accessible before Orisia
        pre_orisia_dungeons = [
            'abandoned_mine_1',
            'forest_cave',
            'bandit_hideout',
            'old_catacombs_section_1',
            'undead_crypt',
            'desert_ruins_entrance'  # Accessible early
        ]

        # Randomly select one
        self.story_flags['yipp_spawn_dungeon'] = random.choice(pre_orisia_dungeons)
        self.story_flags['yipp_dungeon_determined'] = True

    def recruit_character(self, char_id):
        """
        Recruit a character to the party

        Args:
            char_id: Character identifier

        Returns:
            bool: Success
        """
        if char_id in self.characters_recruited:
            return False

        if self.story_flags.get('recruitment_deadline_passed'):
            # Too late!
            return False

        self.characters_recruited.append(char_id)

        # Add to reserves if active party is full
        if len(self.active_party) < 3:
            self.active_party.append(char_id)
        else:
            self.reserve_party.append(char_id)

        return True

    def lose_character(self, char_id):
        """
        Mark character as lost (becomes zombie in final battle)

        Args:
            char_id: Character identifier
        """
        if char_id not in self.characters_recruited and char_id not in self.lost_characters:
            self.lost_characters.append(char_id)

    def close_recruitment(self):
        """
        Close recruitment window (Orisia says YES to desert)
        All un-recruited optional characters become lost
        """
        self.story_flags['recruitment_deadline_passed'] = True

        # Check which optional characters were not recruited
        for char_id, char_data in CHARACTERS.items():
            if not char_data['required'] and char_id not in self.characters_recruited:
                self.lose_character(char_id)

    def add_key_item(self, key_item_id):
        """
        Add key item to inventory

        Args:
            key_item_id: Key item identifier

        Returns:
            bool: Success (False if already have it)
        """
        if key_item_id in self.key_items:
            return False

        self.key_items.append(key_item_id)
        return True

    def has_key_item(self, key_item_id):
        """Check if player has a key item"""
        return key_item_id in self.key_items

    def complete_orisia_sidequest(self, char_id):
        """
        Complete Orisia sidequest for a character

        Args:
            char_id: Character identifier

        Returns:
            bool: Success
        """
        from data.key_items import check_sidequest_requirements

        if char_id in self.orisia_sidequests_completed:
            return False

        # Check if requirements met
        if not check_sidequest_requirements(char_id, self.key_items):
            return False

        self.orisia_sidequests_completed.append(char_id)

        # Apply evolution
        char_data = CHARACTERS[char_id]
        evolved_class = char_data.get('evolved_class')

        if evolved_class:
            if isinstance(evolved_class, list):
                # Yipp's alignment choice - handled separately
                pass
            else:
                # Normal evolution
                self.character_classes[char_id] = evolved_class
                self.level_caps[char_id] = 99

        # Special cases
        if char_id in ['frostbite', 'fritzzit']:
            # Ultimate weapon sidequests - level cap increases when weapon obtained
            pass

        return True

    def evolve_yipp(self, alignment):
        """
        Evolve Yipp to Saint or Vampire

        Args:
            alignment: 'saint' or 'vampire'

        Returns:
            bool: Success
        """
        if 'yipp' not in self.characters_recruited:
            return False

        if 'yipp' in self.orisia_sidequests_completed:
            return False

        if alignment not in ['saint', 'vampire']:
            return False

        # Check key items (both required)
        if not self.has_key_item('holy_symbol') or not self.has_key_item('empty_pewter_wine_glass'):
            return False

        # Apply evolution
        self.character_classes['yipp'] = alignment
        self.level_caps['yipp'] = 99
        self.story_flags['yipp_alignment'] = alignment
        self.orisia_sidequests_completed.append('yipp')

        return True

    def kill_flood(self):
        """
        Permanently kill Flood (story event)
        """
        if self.story_flags.get('flood_dead'):
            return  # Already dead

        self.story_flags['flood_dead'] = True
        self.story_flags['flood_death_cutscene'] = True

        # Remove from party
        if 'flood' in self.active_party:
            self.active_party.remove('flood')
        if 'flood' in self.reserve_party:
            self.reserve_party.remove('flood')

        # Drop equipment to inventory
        flood_equipment = self.characters['flood']['equipment']
        for slot, item_id in flood_equipment.items():
            if item_id:
                self.add_item_to_inventory(item_id)

        # Clear equipment
        self.characters['flood']['equipment'] = {
            'weapon': None,
            'armor': None,
            'shield': None,
            'accessory': None,
            'special': None
        }

    def trigger_iris_berserk(self):
        """
        Trigger Iris berserk mode (Fei died)
        """
        if 'iris' not in self.active_party:
            return

        if 'fei' not in self.active_party:
            return

        # Check if Fei is dead (0 HP)
        if self.characters['fei']['hp'] <= 0:
            self.fei_dead = True
            self.iris_berserk = True

    def end_iris_berserk(self):
        """
        End Iris berserk mode (Fei raised)
        """
        if self.characters['fei']['hp'] > 0:
            self.fei_dead = False
            self.iris_berserk = False

    def add_item_to_inventory(self, item_id, quantity=1):
        """Add item to inventory"""
        if item_id in self.items:
            self.items[item_id] += quantity
        else:
            self.items[item_id] = quantity

    def remove_item_from_inventory(self, item_id, quantity=1):
        """Remove item from inventory"""
        if item_id not in self.items:
            return False

        if self.items[item_id] < quantity:
            return False

        self.items[item_id] -= quantity
        if self.items[item_id] <= 0:
            del self.items[item_id]

        return True

    def has_item_in_inventory(self, item_id, quantity=1):
        """
        Check if player has item in inventory

        Args:
            item_id: Item ID to check
            quantity: Minimum quantity required (default 1)

        Returns:
            bool: True if player has enough of the item
        """
        if item_id not in self.items:
            return False
        return self.items[item_id] >= quantity

    def check_ending_requirements(self):
        """
        Determine which ending the player gets

        Returns:
            str: Ending type ('best', 'good', 'normal', 'bad')
        """
        # Bad Ending
        if not self.story_flags.get('cure_found'):
            return 'bad'

        # Check Yipp alignment
        yipp_alignment = self.story_flags.get('yipp_alignment')
        if yipp_alignment == 'vampire':
            return 'bad'  # Vampire Yipp locks to bad ending

        # Best Ending Requirements
        # 1. Yipp recruited AND became Saint
        # 2. Cure found (Kella saved)
        # 3. Slaver Island completed
        if (yipp_alignment == 'saint' and
            self.story_flags.get('cure_found') and
            self.story_flags.get('slaver_island_completed')):
            return 'best'

        # Good Ending
        # All characters recruited, Yipp is Saint OR not recruited, cure found
        all_optional_recruited = all(
            char_id in self.characters_recruited
            for char_id, char_data in CHARACTERS.items()
            if not char_data['required']
        )

        if (all_optional_recruited and
            self.story_flags.get('cure_found') and
            (yipp_alignment == 'saint' or yipp_alignment is None)):
            return 'good'

        # Normal Ending
        return 'normal'

    def export_state(self):
        """
        Export game state for saving

        Returns:
            dict: Game state
        """
        return {
            'new_game_plus': self.new_game_plus,
            'playthrough_count': self.playthrough_count,
            'active_party': self.active_party,
            'reserve_party': self.reserve_party,
            'characters': self.characters,
            'characters_recruited': self.characters_recruited,
            'lost_characters': self.lost_characters,
            'character_classes': self.character_classes,
            'level_caps': self.level_caps,
            'items': self.items,
            'equipment': self.equipment,
            'key_items': self.key_items,
            'gil': self.gil,
            'story_flags': self.story_flags,
            'orisia_sidequests_completed': self.orisia_sidequests_completed,
            'ultimate_weapons': self.ultimate_weapons,
            'fei_dead': self.fei_dead,
            'iris_berserk': self.iris_berserk,
            'current_location': self.current_location,
            'player_position': self.player_position,
            'playtime_seconds': self.playtime_seconds,
        }

    def import_state(self, save_data):
        """
        Import game state from save data

        Args:
            save_data: Saved game state
        """
        self.new_game_plus = save_data.get('new_game_plus', False)
        self.playthrough_count = save_data.get('playthrough_count', 1)
        self.active_party = save_data['party']['active']
        self.reserve_party = save_data['party']['reserves']
        self.characters = save_data['party']['characters']
        self.characters_recruited = save_data.get('characters_recruited', [])
        self.lost_characters = save_data.get('lost_characters', [])
        self.character_classes = save_data.get('character_classes', {})
        self.level_caps = save_data.get('level_caps', {})
        self.items = save_data['inventory']['items']
        self.equipment = save_data['inventory']['equipment']
        self.key_items = save_data['inventory']['key_items']
        self.gil = save_data['inventory']['gil']
        self.story_flags = save_data['story_flags']
        self.orisia_sidequests_completed = save_data.get('orisia_sidequests_completed', [])
        self.ultimate_weapons = save_data.get('ultimate_weapons', [])
        self.fei_dead = save_data.get('fei_dead', False)
        self.iris_berserk = save_data.get('iris_berserk', False)
        self.current_location = save_data['current_location']
        self.player_position = save_data['player_position']
        self.playtime_seconds = save_data.get('playtime_seconds', 0)
