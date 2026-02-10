"""
Random Encounter System
Handles enemy encounters based on region, story flags, and spawn rates
"""

import random
from data.enemies import ENCOUNTER_TABLES, get_encounter_table, SPAWN_MODIFICATIONS

class EncounterSystem:
    """Manages random enemy encounters"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.steps_since_last_encounter = 0
        self.encounter_rate_modifier = 1.0

    def update_step(self):
        """
        Update step counter and check for encounter

        Returns:
            list: Enemy IDs if encounter triggered, None otherwise
        """
        self.steps_since_last_encounter += 1

        # Check for encounter
        if self.check_encounter():
            self.steps_since_last_encounter = 0
            return self.generate_encounter()

        return None

    def check_encounter(self):
        """
        Check if random encounter should trigger

        Returns:
            bool: Encounter triggered
        """
        region = self.game_state.current_location
        encounter_table = get_encounter_table(region, self.game_state.story_flags)

        if not encounter_table:
            return False

        base_rate = encounter_table.get('encounter_rate', 0.20)
        rate = base_rate * self.encounter_rate_modifier

        # Increase chance with more steps
        if self.steps_since_last_encounter > 5:
            rate += 0.05 * (self.steps_since_last_encounter - 5)

        rate = min(rate, 0.90)  # Cap at 90%

        return random.random() < rate

    def generate_encounter(self):
        """
        Generate enemy encounter for current region

        Returns:
            list: Enemy IDs
        """
        region = self.game_state.current_location
        encounter_table = get_encounter_table(region, self.game_state.story_flags)

        if not encounter_table:
            return []

        enemies_data = encounter_table.get('enemies')
        max_group_size = encounter_table.get('max_group_size', 3)

        # Handle weighted spawns (dict) vs simple list
        if isinstance(enemies_data, dict):
            # Weighted spawn rates (post-imperial, desert, etc.)
            enemy_pool = []
            for enemy_id, weight in enemies_data.items():
                # Add enemy multiple times based on weight
                count = int(weight * 100)  # Convert 0.5 to 50, etc.
                enemy_pool.extend([enemy_id] * count)

            if not enemy_pool:
                return []

            # Select enemies
            num_enemies = random.randint(1, max_group_size)
            selected = []

            for _ in range(num_enemies):
                enemy_id = random.choice(enemy_pool)
                selected.append(enemy_id)

            return selected

        elif isinstance(enemies_data, list):
            # Simple list (equal weights)
            if not enemies_data:
                return []

            num_enemies = random.randint(1, min(max_group_size, len(enemies_data)))
            return random.sample(enemies_data, num_enemies)

        return []

    def get_infected_kobold_spawn_rate(self):
        """
        Get current infected kobold spawn rate

        Returns:
            float: Spawn rate (0.0 to 1.0)
        """
        # Check story flags
        if self.game_state.story_flags.get('kobolds_released'):
            if self.game_state.story_flags.get('desert_entered'):
                # Desert: 50/50 kobolds vs other undead
                return 0.50
            else:
                # Post-imperial: 70% kobolds
                return 0.70

        return 0.0  # Pre-imperial warren escape

    def is_fungal_enemy_spawnable(self):
        """
        Check if fungal enemies can spawn

        Returns:
            bool: Can spawn
        """
        # Fungal enemies removed after Jerod boss
        return not self.game_state.story_flags.get('fungal_enemies_removed', False)

    def force_encounter(self, enemy_ids):
        """
        Force specific encounter (for story battles)

        Args:
            enemy_ids: List of enemy IDs

        Returns:
            list: Enemy IDs
        """
        self.steps_since_last_encounter = 0
        return enemy_ids

    def set_encounter_rate_modifier(self, modifier):
        """
        Set encounter rate modifier

        Args:
            modifier: Rate multiplier (1.0 = normal, 0.5 = half, 2.0 = double)
        """
        self.encounter_rate_modifier = max(0.0, modifier)

    def can_flee_current_region(self):
        """
        Check if can flee from battles in current region

        Returns:
            bool: Can flee
        """
        region = self.game_state.current_location

        # Cannot flee from certain areas
        no_flee_regions = [
            'boss_arena',
            'final_dungeon',
            'catacombs_boss_room'
        ]

        return region not in no_flee_regions

    def get_encounter_background(self):
        """
        Get battle background for current region

        Returns:
            str: Background identifier
        """
        region = self.game_state.current_location

        backgrounds = {
            'tutorial_warren': 'kobold_warren',
            'surface_forest': 'forest',
            'undead_lands': 'graveyard',
            'imperial_city': 'city_streets',
            'post_imperial_warren': 'infected_warren',
            'desert_region': 'desert',
            'catacombs': 'catacombs',
            'boss_arena': 'dark_chamber'
        }

        return backgrounds.get(region, 'default')

    def apply_story_modifications(self):
        """
        Apply story-based spawn modifications

        Returns:
            dict: Active modifications
        """
        active_mods = {}

        # Check each modification
        for mod_id, mod_data in SPAWN_MODIFICATIONS.items():
            trigger = mod_data.get('trigger')

            if trigger in self.game_state.story_flags:
                if self.game_state.story_flags[trigger]:
                    active_mods[mod_id] = mod_data

        return active_mods

    def get_random_enemy_group(self, enemy_type, count):
        """
        Get random group of specific enemy type

        Args:
            enemy_type: Enemy type identifier
            count: Number of enemies

        Returns:
            list: Enemy IDs
        """
        return [enemy_type] * count

    def boss_encounter(self, boss_id):
        """
        Trigger boss encounter

        Args:
            boss_id: Boss identifier

        Returns:
            dict: Boss encounter data
        """
        from data.enemies import BOSSES

        boss_data = BOSSES.get(boss_id)

        if not boss_data:
            return None

        return {
            'type': 'boss',
            'enemies': [boss_id],
            'can_flee': False,
            'background': 'boss_arena',
            'music': 'boss_theme',
            'name': boss_data['name']
        }

    def yipp_dungeon_encounter(self):
        """
        Trigger Yipp dungeon encounter (NPC ally)

        Returns:
            dict: Encounter data with Yipp as ally
        """
        # Random undead enemies
        undead_enemies = ['skeleton', 'wraith', 'zombie_orc']
        num_enemies = random.randint(2, 3)
        enemies = random.choices(undead_enemies, k=num_enemies)

        return {
            'type': 'yipp_rescue',
            'enemies': enemies,
            'npc_ally': 'yipp',
            'can_flee': False,
            'description': 'Yipp is fighting undead and losing!'
        }

    def final_battle_with_lost_characters(self):
        """
        Generate final battle with lost characters as zombies

        Returns:
            dict: Final battle encounter
        """
        # Main boss
        enemies = ['necromancer_lich']

        # Add lost characters as zombies
        for char_id in self.game_state.lost_characters:
            zombie_id = f'zombie_{char_id}'
            enemies.append(zombie_id)

        # Check if Yipp is vampire (betrays party)
        if self.game_state.story_flags.get('yipp_alignment') == 'vampire':
            # Yipp fights with Lich
            enemies.append('yipp_vampire_enemy')
            self.game_state.story_flags['yipp_betrayed'] = True

        return {
            'type': 'final_boss',
            'enemies': enemies,
            'can_flee': False,
            'background': 'necromancer_sanctum',
            'music': 'final_boss_theme',
            'lost_allies': self.game_state.lost_characters,
            'yipp_betrayed': self.game_state.story_flags.get('yipp_betrayed', False)
        }

    def secret_boss_encounter(self):
        """
        Generate secret boss encounter (Kella + Red Dragon)

        Returns:
            dict: Secret boss encounter
        """
        return {
            'type': 'secret_boss',
            'enemies': ['double_infected_kella', 'infected_red_dragon'],
            'can_flee': False,
            'background': 'capitol_ruins',
            'music': 'tragic_boss_theme',
            'description': 'Queen Kella has been transformed...'
        }

    def post_credits_boss_encounter(self):
        """
        Generate post-credits boss encounter (Captain Donald)

        Returns:
            dict: Post-credits boss encounter
        """
        return {
            'type': 'post_credits_boss',
            'enemies': ['captain_donald'],
            'can_flee': False,
            'background': 'slaver_ship_deck',
            'music': 'final_showdown_theme',
            'description': 'The slaver captain stands in your way!'
        }
