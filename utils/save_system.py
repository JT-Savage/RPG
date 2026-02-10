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
        save_data = {
            'timestamp': datetime.now().isoformat(),
            'version': '0.1.0',

            # Party data
            'party': {
                'active': game_state.get('active_party', []),
                'reserves': game_state.get('reserve_party', []),
                'characters': game_state.get('characters', {}),  # Character states
                'formation': game_state.get('formation', 'default')
            },

            # Inventory
            'inventory': {
                'items': game_state.get('items', {}),
                'equipment': game_state.get('equipment', {}),
                'key_items': game_state.get('key_items', []),
                'gil': game_state.get('gil', 0)
            },

            # Story flags - CRITICAL for game progression
            'story_flags': {
                # Tutorial
                'tutorial_complete': game_state.get('tutorial_complete', False),
                'baby_dragon_saved': game_state.get('baby_dragon_saved', False),

                # Warren events
                'warren_infected': game_state.get('warren_infected', False),
                'kella_went_to_wake_dragons': game_state.get('kella_went_to_wake_dragons', False),

                # Surface events
                'met_frostbite': game_state.get('met_frostbite', False),
                'met_fei': game_state.get('met_fei', False),

                # Imperial City
                'imperial_city_visited': game_state.get('imperial_city_visited', False),
                'shotgun_blueprint_purchased': game_state.get('shotgun_blueprint_purchased', False),
                'sniper_rifle_blueprint_purchased': game_state.get('sniper_rifle_blueprint_purchased', False),
                'met_michael': game_state.get('met_michael', False),
                'met_flood': game_state.get('met_flood', False),
                'met_hannah': game_state.get('met_hannah', False),

                # Imperial Warren
                'imperial_warren_explored': game_state.get('imperial_warren_explored', False),
                'imperial_warren_escape': game_state.get('imperial_warren_escape', False),
                'kobolds_released': game_state.get('kobolds_released', False),

                # Recruitment windows
                'fritzzit_crankpot_available': game_state.get('fritzzit_crankpot_available', False),

                # Jerod's House
                'crown_of_flowers_comment_triggered': game_state.get('crown_of_flowers_comment_triggered', False),
                'jerod_house_explored': game_state.get('jerod_house_explored', False),
                'jerod_boss_defeated': game_state.get('jerod_boss_defeated', False),
                'jerod_house_explosion': game_state.get('jerod_house_explosion', False),
                'fungal_enemies_removed': game_state.get('fungal_enemies_removed', False),

                # Halfling rescue
                'cookie_iris_rescued': game_state.get('cookie_iris_rescued', False),
                'fei_grooming_cutscene': game_state.get('fei_grooming_cutscene', False),
                'panda_fur_available': game_state.get('panda_fur_available', False),

                # Yipp
                'yipp_dungeon_determined': game_state.get('yipp_dungeon_determined', False),
                'yipp_spawn_dungeon': game_state.get('yipp_spawn_dungeon', None),
                'yipp_encountered': game_state.get('yipp_encountered', False),

                # Warghoul
                'warghoul_recruited_early': game_state.get('warghoul_recruited_early', False),

                # Orisia and Recruitment Deadline
                'met_orisia': game_state.get('met_orisia', False),
                'orisia_ready_warning_given': game_state.get('orisia_ready_warning_given', False),
                'recruitment_deadline_passed': game_state.get('recruitment_deadline_passed', False),

                # Desert
                'desert_entered': game_state.get('desert_entered', False),
                'army_blocks_return': game_state.get('army_blocks_return', False),

                # Dragon Bosses
                'first_dragon_defeated': game_state.get('first_dragon_defeated', False),
                'second_dragon_defeated': game_state.get('second_dragon_defeated', False),
                'flood_dead': game_state.get('flood_dead', False),
                'flood_death_cutscene': game_state.get('flood_death_cutscene', False),
                'hannah_scream_triggered': game_state.get('hannah_scream_triggered', False),

                # Catacombs
                'catacombs_unlocked': game_state.get('catacombs_unlocked', False),

                # Cure and Endings
                'cure_found': game_state.get('cure_found', False),
                'kella_saved': game_state.get('kella_saved', False),

                # Final Battle
                'necromancer_defeated': game_state.get('necromancer_defeated', False),
                'yipp_alignment': game_state.get('yipp_alignment', None),  # 'saint', 'vampire', or None
                'yipp_betrayed': game_state.get('yipp_betrayed', False),

                # Secret Boss
                'kella_double_infected': game_state.get('kella_double_infected', False),
                'secret_boss_defeated': game_state.get('secret_boss_defeated', False),

                # Post-credits
                'post_credits_unlocked': game_state.get('post_credits_unlocked', False),
                'slaver_island_completed': game_state.get('slaver_island_completed', False),
                'captain_donald_defeated': game_state.get('captain_donald_defeated', False),

                # Endings achieved
                'ending_achieved': game_state.get('ending_achieved', None),  # 'best', 'good', 'normal', 'bad'
            },

            # Character recruitment tracking
            'characters_recruited': game_state.get('characters_recruited', []),
            'lost_characters': game_state.get('lost_characters', []),  # Un-recruited, become zombies

            # Orisia sidequests completed
            'orisia_sidequests_completed': game_state.get('orisia_sidequests_completed', []),

            # Character evolutions
            'character_classes': game_state.get('character_classes', {}),  # character_id: current_class

            # Level caps
            'level_caps': game_state.get('level_caps', {}),  # character_id: max_level

            # Ultimate weapons obtained
            'ultimate_weapons': game_state.get('ultimate_weapons', []),

            # Fei and Iris special tracking
            'fei_dead': game_state.get('fei_dead', False),  # For Iris berserk
            'iris_berserk': game_state.get('iris_berserk', False),

            # Position and location
            'current_location': game_state.get('current_location', 'warren'),
            'player_position': game_state.get('player_position', {'x': 0, 'y': 0}),
            'map_data': game_state.get('map_data', {}),

            # Playtime
            'playtime_seconds': game_state.get('playtime_seconds', 0),

            # New Game+ data
            'new_game_plus': game_state.get('new_game_plus', False),
            'playthrough_count': game_state.get('playthrough_count', 1),
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
        ng_plus_data = {
            'timestamp': datetime.now().isoformat(),
            'playthrough_count': game_state.get('playthrough_count', 1),

            # Characters recruited this playthrough
            'characters_recruited': game_state.get('characters_recruited', []),
            'lost_characters': game_state.get('lost_characters', []),

            # Yipp alignment choice
            'yipp_alignment_previous': game_state.get('yipp_alignment'),

            # Key choices
            'baby_dragon_saved': game_state.get('baby_dragon_saved', False),
            'cure_found': game_state.get('cure_found', False),
            'flood_died': game_state.get('flood_dead', False),

            # Ending achieved
            'ending_achieved': game_state.get('ending_achieved'),

            # Yipp spawn location (for Frostbite comment)
            'yipp_spawn_dungeon': game_state.get('yipp_spawn_dungeon'),

            # Character final levels and classes
            'character_levels': {},
            'character_classes': game_state.get('character_classes', {}),

            # Ultimate weapons obtained
            'ultimate_weapons': game_state.get('ultimate_weapons', []),

            # Sidequests completed
            'orisia_sidequests_completed': game_state.get('orisia_sidequests_completed', [])
        }

        # Extract character levels
        for char_id, char_data in game_state.get('characters', {}).items():
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
