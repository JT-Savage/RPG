"""
Menu System
Handles inventory, party management, equipment, and status screens
"""

class MenuSystem:
    """Manages game menus"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.current_menu = None
        self.menu_stack = []
        self.selected_index = 0
        self.selected_character = None

    def open_menu(self, menu_type):
        """
        Open menu

        Args:
            menu_type: 'main', 'inventory', 'party', 'equipment', 'status', 'save'
        """
        self.current_menu = menu_type
        self.selected_index = 0

    def push_menu(self, menu_type):
        """Push new menu onto stack"""
        if self.current_menu:
            self.menu_stack.append(self.current_menu)

        self.current_menu = menu_type
        self.selected_index = 0

    def pop_menu(self):
        """Pop menu from stack"""
        if self.menu_stack:
            self.current_menu = self.menu_stack.pop()
            self.selected_index = 0
        else:
            self.current_menu = None

    def close_menu(self):
        """Close all menus"""
        self.current_menu = None
        self.menu_stack = []
        self.selected_index = 0

    # === Inventory Management ===

    def get_inventory_items(self):
        """Get list of inventory items"""
        items = []

        for item_id, count in self.game_state.items.items():
            from data.items import ITEMS
            item_data = ITEMS.get(item_id)

            if item_data:
                items.append({
                    'id': item_id,
                    'name': item_data['name'],
                    'count': count,
                    'description': item_data['description'],
                    'usable_in_field': item_data.get('usable_in_field', False),
                    'usable_in_battle': item_data.get('usable_in_battle', False)
                })

        return sorted(items, key=lambda x: x['name'])

    def use_item_on_character(self, item_id, char_id):
        """
        Use item on character

        Args:
            item_id: Item identifier
            char_id: Character identifier

        Returns:
            dict: Result
        """
        from data.items import ITEMS

        item = ITEMS.get(item_id)
        if not item:
            return {'success': False, 'error': 'Invalid item'}

        # Check if have item
        if not self.game_state.has_item_in_inventory(item_id):
            return {'success': False, 'error': 'Don\'t have item'}

        # Check if usable in field
        if not item.get('usable_in_field', False):
            return {'success': False, 'error': 'Cannot use here'}

        # Get character
        char = self.game_state.characters.get(char_id)
        if not char:
            return {'success': False, 'error': 'Invalid character'}

        # Apply item effects
        result = {'success': True, 'effects': []}

        effect = item.get('effect', {})

        # HP restore
        if 'hp_restore' in effect:
            if effect['hp_restore'] == 'full':
                healing = char['max_hp'] - char['hp']
                char['hp'] = char['max_hp']
            else:
                healing = min(effect['hp_restore'], char['max_hp'] - char['hp'])
                char['hp'] += healing

            result['effects'].append(f"Restored {healing} HP")

        # MP restore
        if 'mp_restore' in effect:
            if effect['mp_restore'] == 'full':
                mp_restored = char['max_mp'] - char['mp']
                char['mp'] = char['max_mp']
            else:
                mp_restored = min(effect['mp_restore'], char['max_mp'] - char['mp'])
                char['mp'] += mp_restored

            result['effects'].append(f"Restored {mp_restored} MP")

        # Status cure
        if 'removes_status' in effect:
            from utils.status_effects import remove_status_effect

            status = effect['removes_status']
            if status == 'all':
                char['status_effects'] = []
                result['effects'].append("Cured all status effects")
            else:
                remove_status_effect(char, status)
                result['effects'].append(f"Cured {status}")

        # Revival
        if effect.get('revive'):
            if char['hp'] <= 0:
                hp_restore = int(char['max_hp'] * effect.get('hp_restore_percent', 0.5))
                char['hp'] = hp_restore
                result['effects'].append("Revived")

        # Remove item from inventory
        self.game_state.remove_item_from_inventory(item_id, 1)

        return result

    # === Party Management ===

    def get_party_list(self):
        """Get full party list (active + reserve)"""
        party = []

        # Active party
        for char_id in self.game_state.active_party:
            char = self.game_state.characters.get(char_id)
            if char:
                party.append({
                    'id': char_id,
                    'name': char_id.title(),
                    'level': char['level'],
                    'hp': char['hp'],
                    'max_hp': char['max_hp'],
                    'mp': char['mp'],
                    'max_mp': char['max_mp'],
                    'status': 'active'
                })

        # Reserve party
        for char_id in self.game_state.reserve_party:
            char = self.game_state.characters.get(char_id)
            if char:
                party.append({
                    'id': char_id,
                    'name': char_id.title(),
                    'level': char['level'],
                    'hp': char['hp'],
                    'max_hp': char['max_hp'],
                    'mp': char['mp'],
                    'max_mp': char['max_mp'],
                    'status': 'reserve'
                })

        return party

    def swap_party_members(self, char_id_1, char_id_2):
        """
        Swap party members between active and reserve

        Args:
            char_id_1: First character
            char_id_2: Second character

        Returns:
            bool: Success
        """
        # Find characters
        char1_in_active = char_id_1 in self.game_state.active_party
        char2_in_active = char_id_2 in self.game_state.active_party

        if char1_in_active and not char2_in_active:
            # Swap active with reserve
            active_index = self.game_state.active_party.index(char_id_1)
            reserve_index = self.game_state.reserve_party.index(char_id_2)

            self.game_state.active_party[active_index] = char_id_2
            self.game_state.reserve_party[reserve_index] = char_id_1

            return True

        elif not char1_in_active and char2_in_active:
            # Swap reserve with active
            reserve_index = self.game_state.reserve_party.index(char_id_1)
            active_index = self.game_state.active_party.index(char_id_2)

            self.game_state.reserve_party[reserve_index] = char_id_2
            self.game_state.active_party[active_index] = char_id_1

            return True

        elif char1_in_active and char2_in_active:
            # Swap positions within active party
            index1 = self.game_state.active_party.index(char_id_1)
            index2 = self.game_state.active_party.index(char_id_2)

            self.game_state.active_party[index1] = char_id_2
            self.game_state.active_party[index2] = char_id_1

            return True

        return False

    def can_swap_party_members(self):
        """Check if party swapping is allowed"""
        # Cannot swap in battle
        if self.game_state.in_battle:
            return False

        # Cannot swap in certain story moments
        if self.game_state.story_flags.get('party_locked'):
            return False

        return True

    # === Equipment Management ===

    def get_character_equipment(self, char_id):
        """
        Get character's equipped items

        Args:
            char_id: Character identifier

        Returns:
            dict: Equipment slots
        """
        char = self.game_state.characters.get(char_id)
        if not char:
            return {}

        return char.get('equipment', {
            'weapon': None,
            'armor': None,
            'accessory': None
        })

    def equip_item(self, char_id, equip_id, slot):
        """
        Equip item on character

        Args:
            char_id: Character identifier
            equip_id: Equipment identifier
            slot: 'weapon', 'armor', or 'accessory'

        Returns:
            dict: Result
        """
        from data.equipment import EQUIPMENT

        # Get character
        char = self.game_state.characters.get(char_id)
        if not char:
            return {'success': False, 'error': 'Invalid character'}

        # Get equipment
        equip_data = EQUIPMENT.get(equip_id)
        if not equip_data:
            return {'success': False, 'error': 'Invalid equipment'}

        # Check if character can equip
        can_equip_classes = equip_data.get('equippable_by')
        if can_equip_classes:
            char_class = self.game_state.character_classes.get(char_id)
            if char_class not in can_equip_classes:
                return {'success': False, 'error': 'Cannot equip'}

        # Check slot type
        if equip_data['type'] != slot:
            return {'success': False, 'error': 'Wrong slot'}

        # Unequip current item if any
        if 'equipment' not in char:
            char['equipment'] = {}

        old_equip_id = char['equipment'].get(slot)

        # Equip new item
        char['equipment'][slot] = equip_id

        # Recalculate stats
        self.recalculate_character_stats(char_id)

        return {
            'success': True,
            'equipped': equip_id,
            'unequipped': old_equip_id
        }

    def unequip_item(self, char_id, slot):
        """
        Unequip item from character

        Args:
            char_id: Character identifier
            slot: Equipment slot

        Returns:
            dict: Result
        """
        char = self.game_state.characters.get(char_id)
        if not char:
            return {'success': False, 'error': 'Invalid character'}

        if 'equipment' not in char:
            return {'success': False, 'error': 'Nothing equipped'}

        old_equip_id = char['equipment'].get(slot)
        if not old_equip_id:
            return {'success': False, 'error': 'Nothing equipped'}

        # Unequip
        char['equipment'][slot] = None

        # Recalculate stats
        self.recalculate_character_stats(char_id)

        return {
            'success': True,
            'unequipped': old_equip_id
        }

    def recalculate_character_stats(self, char_id):
        """
        Recalculate character stats with equipment bonuses

        Args:
            char_id: Character identifier
        """
        from data.equipment import EQUIPMENT
        from data.characters import get_character_stats_at_level

        char = self.game_state.characters.get(char_id)
        if not char:
            return

        # Get base stats
        base_stats = get_character_stats_at_level(char_id, char['level'])

        # Reset stats to base
        char['stats'] = {
            'attack': int(base_stats['attack']),
            'defense': int(base_stats['defense']),
            'magic_power': int(base_stats['magic_power']),
            'spell_resistance': int(base_stats['spell_resistance']),
            'speed': int(base_stats['speed'])
        }

        # Apply equipment bonuses
        equipment = char.get('equipment', {})

        for slot, equip_id in equipment.items():
            if not equip_id:
                continue

            equip_data = EQUIPMENT.get(equip_id)
            if not equip_data:
                continue

            # Add stat bonuses
            stats = equip_data.get('stats', {})
            for stat_name, value in stats.items():
                if stat_name in char['stats']:
                    char['stats'][stat_name] += value

    # === Status Screen ===

    def get_character_status(self, char_id):
        """
        Get character status for display

        Args:
            char_id: Character identifier

        Returns:
            dict: Character status
        """
        from utils.level_up_system import get_exp_to_next_level, get_level_progress

        char = self.game_state.characters.get(char_id)
        if not char:
            return None

        char_class = self.game_state.character_classes.get(char_id, 'Unknown')
        exp_to_next = get_exp_to_next_level(char['level'])
        level_progress = get_level_progress(self.game_state, char_id)

        return {
            'id': char_id,
            'name': char_id.title(),
            'class': char_class,
            'level': char['level'],
            'hp': char['hp'],
            'max_hp': char['max_hp'],
            'mp': char['mp'],
            'max_mp': char['max_mp'],
            'exp': char['exp'],
            'exp_to_next': exp_to_next,
            'level_progress': level_progress,
            'stats': char['stats'],
            'equipment': self.get_character_equipment(char_id),
            'learned_spells': char.get('learned_spells', []),
            'learned_abilities': char.get('learned_abilities', []),
            'status_effects': char.get('status_effects', [])
        }

    # === Save Menu ===

    def get_save_slots(self):
        """Get available save slots"""
        # TODO: Implement save slot system
        return [
            {'slot': 1, 'empty': True},
            {'slot': 2, 'empty': True},
            {'slot': 3, 'empty': True}
        ]

    def save_to_slot(self, slot):
        """Save game to slot"""
        from utils.save_system import save_game

        filename = f'save_{slot}.json'
        return save_game(self.game_state, filename)

    def is_menu_open(self):
        """Check if any menu is open"""
        return self.current_menu is not None
