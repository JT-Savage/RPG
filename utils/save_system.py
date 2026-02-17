"""
Save/Load system with quicksave, manual saves (5-100 slots), and autosave
Stores party, inventory, story flags, New Game+ data
"""

import json
import os
from datetime import datetime

class SaveSystem:
    """Handles all save/load operations"""

    def __init__(self, save_directory='saves'):
        self.save_directory = save_directory
        self.max_save_slots = 100
        self.min_save_slots = 5

        # Create save directory if it doesn't exist
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        self.autosave_file = os.path.join(save_directory, 'autosave.json')
        self.quicksave_file = os.path.join(save_directory, 'quicksave.json')
        self.new_game_plus_file = os.path.join(save_directory, 'ng_plus_data.json')

    def create_save_data(self, game_state):
        """
        Create save data dict from game state

        Args:
            game_state: Current game state dict

        Returns:
            dict: Save data
        """
        # Support both dict and GameState object
        def _get(key, default=None):
            if isinstance(game_state, dict):
                return game_state.get(key, default)
            else:
                return getattr(game_state, key, default)

        # Get story flags (stored as a nested dict in GameState)
        story_flags = _get('story_flags', {})
        def _flag(key, default=False):
            if isinstance(story_flags, dict):
                return story_flags.get(key, default)
            return default

        save_data = {
            'timestamp': datetime.now().isoformat(),
            'version': '0.1.0',

            # Party data
            'party': {
                'active': _get('active_party', []),
                'reserves': _get('reserve_party', []),
                'characters': _get('characters', {}),  # Character states
                'formation': _get('formation', 'default')
            },

            # Inventory
            'inventory': {
                'items': _get('items', {}),
                'equipment': _get('equipment', {}),
                'key_items': _get('key_items', []),
                'gil': _get('gil', 0)
            },

            # Story flags - CRITICAL for game progression
            'story_flags': {
                # Tutorial
                'tutorial_complete': _flag('tutorial_complete'),
                'baby_dragon_saved': _flag('baby_dragon_saved'),

                # Warren events
                'warren_infected': _flag('warren_infected'),
                'kella_went_to_wake_dragons': _flag('kella_went_to_wake_dragons'),

                # Surface events
                'met_frostbite': _flag('met_frostbite'),
                'met_fei': _flag('met_fei'),

                # Imperial City
                'imperial_city_visited': _flag('imperial_city_visited'),
                'shotgun_blueprint_purchased': _flag('shotgun_blueprint_purchased'),
                'sniper_rifle_blueprint_purchased': _flag('sniper_rifle_blueprint_purchased'),
                'met_michael': _flag('met_michael'),
                'met_flood': _flag('met_flood'),
                'met_hannah': _flag('met_hannah'),

                # Imperial Warren
                'imperial_warren_explored': _flag('imperial_warren_explored'),
                'imperial_warren_escape': _flag('imperial_warren_escape'),
                'kobolds_released': _flag('kobolds_released'),

                # Recruitment windows
                'fritzzit_crankpot_available': _flag('fritzzit_crankpot_available'),

                # Jerod's House
                'crown_of_flowers_comment_triggered': _flag('crown_of_flowers_comment_triggered'),
                'jerod_house_explored': _flag('jerod_house_explored'),
                'jerod_boss_defeated': _flag('jerod_boss_defeated'),
                'jerod_house_explosion': _flag('jerod_house_explosion'),
                'fungal_enemies_removed': _flag('fungal_enemies_removed'),

                # Halfling rescue
                'cookie_iris_rescued': _flag('cookie_iris_rescued'),
                'fei_grooming_cutscene': _flag('fei_grooming_cutscene'),
                'panda_fur_available': _flag('panda_fur_available'),

                # Yipp
                'yipp_dungeon_determined': _flag('yipp_dungeon_determined'),
                'yipp_spawn_dungeon': _flag('yipp_spawn_dungeon', None),
                'yipp_encountered': _flag('yipp_encountered'),

                # Warghoul
                'warghoul_recruited_early': _flag('warghoul_recruited_early'),

                # Orisia and Recruitment Deadline
                'met_orisia': _flag('met_orisia'),
                'orisia_ready_warning_given': _flag('orisia_ready_warning_given'),
                'recruitment_deadline_passed': _flag('recruitment_deadline_passed'),

                # Desert
                'desert_entered': _flag('desert_entered'),
                'army_blocks_return': _flag('army_blocks_return'),

                # Dragon Bosses
                'first_dragon_defeated': _flag('first_dragon_defeated'),
                'second_dragon_defeated': _flag('second_dragon_defeated'),
                'flood_dead': _flag('flood_dead'),
                'flood_death_cutscene': _flag('flood_death_cutscene'),
                'hannah_scream_triggered': _flag('hannah_scream_triggered'),

                # Catacombs
                'catacombs_unlocked': _flag('catacombs_unlocked'),

                # Cure and Endings
                'cure_found': _flag('cure_found'),
                'kella_saved': _flag('kella_saved'),

                # Final Battle
                'necromancer_defeated': _flag('necromancer_defeated'),
                'yipp_alignment': _flag('yipp_alignment', None),  # 'saint', 'vampire', or None
                'yipp_betrayed': _flag('yipp_betrayed'),

                # Secret Boss
                'kella_double_infected': _flag('kella_double_infected'),
                'secret_boss_defeated': _flag('secret_boss_defeated'),

                # Post-credits
                'post_credits_unlocked': _flag('post_credits_unlocked'),
                'slaver_island_completed': _flag('slaver_island_completed'),
                'captain_donald_defeated': _flag('captain_donald_defeated'),

                # Endings achieved
                'ending_achieved': _flag('ending_achieved', None),  # 'best', 'good', 'normal', 'bad'
            },

            # Character recruitment tracking
            'characters_recruited': _get('characters_recruited', []),
            'lost_characters': _get('lost_characters', []),  # Un-recruited, become zombies

            # Orisia sidequests completed
            'orisia_sidequests_completed': _get('orisia_sidequests_completed', []),

            # Character evolutions
            'character_classes': _get('character_classes', {}),  # character_id: current_class

            # Level caps
            'level_caps': _get('level_caps', {}),  # character_id: max_level

            # Ultimate weapons obtained
            'ultimate_weapons': _get('ultimate_weapons', []),

            # Fei and Iris special tracking
            'fei_dead': _get('fei_dead', False),  # For Iris berserk
            'iris_berserk': _get('iris_berserk', False),

            # Position and location
            'current_location': _get('current_location', 'warren'),
            'player_position': _get('player_position', {'x': 0, 'y': 0}),
            'map_data': _get('map_data', {}),

            # Playtime
            'playtime_seconds': _get('playtime_seconds', 0),

            # New Game+ data
            'new_game_plus': _get('new_game_plus', False),
            'playthrough_count': _get('playthrough_count', 1),
        }

        return save_data

    def save_game(self, game_state, slot=None, save_type='manual'):
        """
        Save game to file

        Args:
            game_state: Current game state
            slot: Save slot number (None for autosave/quicksave)
            save_type: 'manual', 'auto', 'quick'

        Returns:
            bool: Success
        """
        save_data = self.create_save_data(game_state)
        save_data['save_type'] = save_type

        # Determine filename
        if save_type == 'auto':
            filename = self.autosave_file
        elif save_type == 'quick':
            filename = self.quicksave_file
        else:  # manual
            if slot is None:
                raise ValueError("Manual save requires slot number")
            if slot < 1 or slot > self.max_save_slots:
                raise ValueError(f"Save slot must be between 1 and {self.max_save_slots}")

            filename = os.path.join(self.save_directory, f'save_{slot:03d}.json')

        # Write save file
        try:
            with open(filename, 'w') as f:
                json.dump(save_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self, slot=None, save_type='manual'):
        """
        Load game from file

        Args:
            slot: Save slot number (None for autosave/quicksave)
            save_type: 'manual', 'auto', 'quick'

        Returns:
            dict: Game state or None if failed
        """
        # Determine filename
        if save_type == 'auto':
            filename = self.autosave_file
        elif save_type == 'quick':
            filename = self.quicksave_file
        else:  # manual
            if slot is None:
                raise ValueError("Manual load requires slot number")
            filename = os.path.join(self.save_directory, f'save_{slot:03d}.json')

        # Check if file exists
        if not os.path.exists(filename):
            return None

        # Load save file
        try:
            with open(filename, 'r') as f:
                save_data = json.load(f)
            return save_data
        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    def get_save_info(self, slot):
        """
        Get save file info without loading full data

        Args:
            slot: Save slot number

        Returns:
            dict: Save info (timestamp, playtime, location, etc.) or None
        """
        filename = os.path.join(self.save_directory, f'save_{slot:03d}.json')

        if not os.path.exists(filename):
            return None

        try:
            with open(filename, 'r') as f:
                save_data = json.load(f)

            return {
                'slot': slot,
                'timestamp': save_data.get('timestamp'),
                'playtime': save_data.get('playtime_seconds', 0),
                'location': save_data.get('current_location'),
                'party_size': len(save_data.get('party', {}).get('active', [])),
                'gil': save_data.get('inventory', {}).get('gil', 0),
                'new_game_plus': save_data.get('new_game_plus', False),
                'playthrough_count': save_data.get('playthrough_count', 1)
            }
        except Exception as e:
            print(f"Error reading save info: {e}")
            return None

    def list_saves(self):
        """
        List all available save files

        Returns:
            list: List of save info dicts
        """
        saves = []
        for slot in range(1, self.max_save_slots + 1):
            info = self.get_save_info(slot)
            if info:
                saves.append(info)
        return saves

    def delete_save(self, slot):
        """
        Delete a save file

        Args:
            slot: Save slot number

        Returns:
            bool: Success
        """
        filename = os.path.join(self.save_directory, f'save_{slot:03d}.json')

        if not os.path.exists(filename):
            return False

        try:
            os.remove(filename)
            return True
        except Exception as e:
            print(f"Error deleting save: {e}")
            return False

    def save_new_game_plus_data(self, game_state):
        """
        Save New Game+ data for next playthrough

        Args:
            game_state: Completed game state

        Returns:
            bool: Success
        """
        # Support both dict and GameState object
        def _get(key, default=None):
            if isinstance(game_state, dict):
                return game_state.get(key, default)
            else:
                return getattr(game_state, key, default)

        # Story flags are stored in a nested dict on GameState
        story_flags = _get('story_flags', {})
        def _flag(key, default=None):
            if isinstance(story_flags, dict):
                return story_flags.get(key, default)
            return default

        ng_plus_data = {
            'timestamp': datetime.now().isoformat(),
            'playthrough_count': _get('playthrough_count', 1),

            # Characters recruited this playthrough
            'characters_recruited': _get('characters_recruited', []),
            'lost_characters': _get('lost_characters', []),

            # Yipp alignment choice
            'yipp_alignment_previous': _flag('yipp_alignment'),

            # Key choices
            'baby_dragon_saved': _flag('baby_dragon_saved', False),
            'cure_found': _flag('cure_found', False),
            'flood_died': _flag('flood_dead', False),

            # Ending achieved
            'ending_achieved': _flag('ending_achieved'),

            # Yipp spawn location (for Frostbite comment)
            'yipp_spawn_dungeon': _flag('yipp_spawn_dungeon'),

            # Character final levels and classes
            'character_levels': {},
            'character_classes': _get('character_classes', {}),

            # Ultimate weapons obtained
            'ultimate_weapons': _get('ultimate_weapons', []),

            # Sidequests completed
            'orisia_sidequests_completed': _get('orisia_sidequests_completed', [])
        }

        # Extract character levels
        characters = _get('characters', {})
        for char_id, char_data in characters.items():
            ng_plus_data['character_levels'][char_id] = char_data.get('level', 1)

        try:
            with open(self.new_game_plus_file, 'w') as f:
                json.dump(ng_plus_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving NG+ data: {e}")
            return False

    def load_new_game_plus_data(self):
        """
        Load New Game+ data from previous playthrough

        Returns:
            dict: NG+ data or None
        """
        if not os.path.exists(self.new_game_plus_file):
            return None

        try:
            with open(self.new_game_plus_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading NG+ data: {e}")
            return None

    def has_completed_playthrough(self):
        """
        Check if player has completed at least one playthrough

        Returns:
            bool: True if NG+ data exists
        """
        return os.path.exists(self.new_game_plus_file)


# Module-level wrapper functions for convenience
_save_system_instance = None

def get_save_system():
    """Get or create the global SaveSystem instance"""
    global _save_system_instance
    if _save_system_instance is None:
        _save_system_instance = SaveSystem()
    return _save_system_instance


def save_game(game_state, filename=None):
    """
    Save game to file

    Args:
        game_state: GameState object
        filename: Optional filename (e.g., 'autosave.json')

    Returns:
        bool: True if save successful
    """
    system = get_save_system()

    # Determine save type and slot based on filename
    if filename == 'autosave.json':
        return system.save_game(game_state, save_type='autosave')
    elif filename == 'quicksave.json':
        return system.save_game(game_state, save_type='quicksave')
    elif filename:
        # Extract slot number if present (e.g., 'save_01.json' -> slot 1)
        import re
        match = re.search(r'save_(\d+)\.json', filename)
        if match:
            slot = int(match.group(1))
            return system.save_game(game_state, slot=slot, save_type='manual')
        else:
            # Default to autosave if filename format not recognized
            return system.save_game(game_state, save_type='autosave')
    else:
        # No filename provided, use autosave
        return system.save_game(game_state, save_type='autosave')


def load_game(filename=None):
    """
    Load game from file

    Args:
        filename: Optional filename (e.g., 'autosave.json')

    Returns:
        GameState: Loaded game state or None if failed
    """
    from utils.game_state import GameState

    system = get_save_system()

    # Determine save type and slot based on filename
    if filename == 'autosave.json' or filename is None:
        save_data = system.load_game(save_type='autosave')
    elif filename == 'quicksave.json':
        save_data = system.load_game(save_type='quicksave')
    else:
        # Extract slot number if present
        import re
        match = re.search(r'save_(\d+)\.json', filename)
        if match:
            slot = int(match.group(1))
            save_data = system.load_game(slot=slot, save_type='manual')
        else:
            # Default to autosave
            save_data = system.load_game(save_type='autosave')

    if not save_data:
        return None

    # Create GameState from save data
    game_state = GameState()

    # Restore party data
    game_state.active_party = save_data['party']['active']
    game_state.reserve_party = save_data['party']['reserves']
    game_state.characters = save_data['party']['characters']

    # Restore inventory
    game_state.items = save_data['inventory']['items']
    game_state.equipment = save_data['inventory']['equipment']
    game_state.key_items = save_data['inventory']['key_items']
    game_state.gil = save_data['inventory'].get('gil', 0)

    # Restore story flags
    game_state.story_flags = save_data.get('story_flags', {})

    # Restore character/party tracking
    game_state.characters_recruited = save_data.get('characters_recruited', [])
    game_state.lost_characters = save_data.get('lost_characters', [])
    game_state.orisia_sidequests_completed = save_data.get('orisia_sidequests_completed', [])
    game_state.character_classes = save_data.get('character_classes', {})
    game_state.level_caps = save_data.get('level_caps', {})
    game_state.ultimate_weapons = save_data.get('ultimate_weapons', [])

    # Restore special flags
    game_state.fei_dead = save_data.get('fei_dead', False)
    game_state.iris_berserk = save_data.get('iris_berserk', False)

    # Restore position and world state
    game_state.current_location = save_data.get('current_location', 'tutorial_warren')
    game_state.player_position = save_data.get('player_position', {'x': 0, 'y': 0})

    # Restore playtime
    game_state.playtime_seconds = save_data.get('playtime_seconds', 0)

    # Restore NG+ data
    game_state.new_game_plus = save_data.get('new_game_plus', False)
    game_state.playthrough_count = save_data.get('playthrough_count', 1)

    return game_state
