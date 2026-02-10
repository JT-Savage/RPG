"""
Map and Exploration System
Handles world map, locations, NPCs, and navigation
"""

class MapSystem:
    """Manages world map and exploration"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.player_position = [128, 112]  # Center of 256x224 screen
        self.camera_position = [0, 0]
        self.move_speed = 2

    def move_player(self, dx, dy):
        """
        Move player

        Args:
            dx: Delta X
            dy: Delta Y

        Returns:
            bool: Movement successful
        """
        new_x = self.player_position[0] + dx * self.move_speed
        new_y = self.player_position[1] + dy * self.move_speed

        # Check boundaries
        if not self.is_position_walkable(new_x, new_y):
            return False

        # Update position
        self.player_position[0] = new_x
        self.player_position[1] = new_y

        # Update camera to follow player
        self.update_camera()

        return True

    def is_position_walkable(self, x, y):
        """
        Check if position is walkable

        Args:
            x: X position
            y: Y position

        Returns:
            bool: Walkable
        """
        # TODO: Check collision map
        # For now, just check screen bounds
        return 0 <= x < 256 and 0 <= y < 224

    def update_camera(self):
        """Update camera to follow player"""
        # Simple camera follow (centered on player)
        self.camera_position[0] = self.player_position[0] - 128
        self.camera_position[1] = self.player_position[1] - 112

    def check_npc_interaction(self):
        """
        Check for NPC interaction at player position

        Returns:
            str: NPC ID or None
        """
        from data.locations import get_location_npcs

        location = self.game_state.current_location
        npcs = get_location_npcs(location)

        for npc_id, npc_data in npcs.items():
            npc_pos = npc_data.get('position', [0, 0])

            # Check distance
            distance = self.calculate_distance(
                self.player_position,
                npc_pos
            )

            if distance < 20:  # Interaction range
                return npc_id

        return None

    def check_location_trigger(self):
        """
        Check for location trigger (door, warp, etc.)

        Returns:
            dict: Trigger data or None
        """
        from data.locations import get_location_triggers

        location = self.game_state.current_location
        triggers = get_location_triggers(location)

        for trigger_id, trigger_data in triggers.items():
            trigger_pos = trigger_data.get('position', [0, 0])
            trigger_size = trigger_data.get('size', [16, 16])

            # Check if player is in trigger area
            if self.is_in_area(
                self.player_position,
                trigger_pos,
                trigger_size
            ):
                return trigger_data

        return None

    def calculate_distance(self, pos1, pos2):
        """Calculate distance between two positions"""
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        return (dx * dx + dy * dy) ** 0.5

    def is_in_area(self, pos, area_pos, area_size):
        """Check if position is in area"""
        return (area_pos[0] <= pos[0] < area_pos[0] + area_size[0] and
                area_pos[1] <= pos[1] < area_pos[1] + area_size[1])

    def enter_location(self, location_id):
        """
        Enter new location

        Args:
            location_id: Location identifier

        Returns:
            bool: Success
        """
        from data.locations import LOCATIONS

        location = LOCATIONS.get(location_id)
        if not location:
            return False

        # Check if unlocked
        if location.get('requires_flag'):
            if not self.game_state.story_flags.get(location['requires_flag']):
                return False

        # Update location
        self.game_state.current_location = location_id

        # Set spawn position
        spawn_pos = location.get('spawn_position', [128, 112])
        self.player_position = list(spawn_pos)

        # Trigger location events
        from utils.story_event_system import StoryEventSystem
        event_system = StoryEventSystem(self.game_state)
        event_id = event_system.check_location_events(location_id)

        if event_id:
            event_system.trigger_event(event_id)

        return True

    def get_available_locations(self):
        """
        Get list of available locations (for fast travel)

        Returns:
            list: Location IDs
        """
        from data.locations import LOCATIONS

        available = []

        for location_id, location in LOCATIONS.items():
            # Check if unlocked
            if location.get('requires_flag'):
                if not self.game_state.story_flags.get(location['requires_flag']):
                    continue

            # Check if can fast travel to
            if location.get('fast_travel', True):
                available.append(location_id)

        return available

    def fast_travel(self, location_id):
        """
        Fast travel to location

        Args:
            location_id: Location identifier

        Returns:
            bool: Success
        """
        # Check if can fast travel
        if not self.can_fast_travel():
            return False

        # Check if location is available
        if location_id not in self.get_available_locations():
            return False

        # Travel
        return self.enter_location(location_id)

    def can_fast_travel(self):
        """Check if fast travel is allowed"""
        # Cannot fast travel in certain situations
        if self.game_state.in_battle:
            return False

        if self.game_state.story_flags.get('fast_travel_disabled'):
            return False

        return True

    def get_current_location_name(self):
        """Get current location name"""
        from data.locations import LOCATIONS

        location = LOCATIONS.get(self.game_state.current_location)
        if location:
            return location.get('name', 'Unknown')

        return 'Unknown'

    def get_location_description(self, location_id):
        """Get location description"""
        from data.locations import LOCATIONS

        location = LOCATIONS.get(location_id)
        if location:
            return location.get('description', '')

        return ''

    def save_position(self):
        """Save player position"""
        return {
            'location': self.game_state.current_location,
            'position': list(self.player_position)
        }

    def load_position(self, data):
        """Load player position"""
        self.game_state.current_location = data.get('location', 'surface_forest')
        self.player_position = list(data.get('position', [128, 112]))
        self.update_camera()


class NPCSystem:
    """Manages NPC interactions"""

    def __init__(self, game_state):
        self.game_state = game_state

    def interact_with_npc(self, npc_id):
        """
        Interact with NPC

        Args:
            npc_id: NPC identifier

        Returns:
            dict: Interaction result
        """
        from data.npcs import NPCS
        from utils.dialogue_system import DialogueSystem

        npc = NPCS.get(npc_id)
        if not npc:
            return None

        # Check if NPC has dialogue
        dialogue_id = npc.get('dialogue_id')

        if dialogue_id:
            dialogue_system = DialogueSystem(self.game_state)

            # Check conditions
            if dialogue_system.check_dialogue_conditions(dialogue_id):
                return {
                    'type': 'dialogue',
                    'dialogue_id': dialogue_id,
                    'npc': npc
                }

        # Check if NPC is a shop
        shop_id = npc.get('shop_id')
        if shop_id:
            return {
                'type': 'shop',
                'shop_id': shop_id,
                'npc': npc
            }

        # Check if NPC is recruitable character
        if npc.get('recruitable'):
            char_id = npc.get('character_id')
            from utils.recruitment_system import RecruitmentSystem

            recruitment = RecruitmentSystem(self.game_state)

            if recruitment.is_character_recruitable(char_id):
                return {
                    'type': 'recruitment',
                    'character_id': char_id,
                    'npc': npc
                }

        # Check if NPC gives quest
        quest_id = npc.get('quest_id')
        if quest_id:
            if not self.game_state.story_flags.get(f'{quest_id}_started'):
                return {
                    'type': 'quest',
                    'quest_id': quest_id,
                    'npc': npc
                }

        # Generic NPC
        return {
            'type': 'generic',
            'message': npc.get('message', 'Hello, traveler.'),
            'npc': npc
        }

    def get_npc_name(self, npc_id):
        """Get NPC name"""
        from data.npcs import NPCS

        npc = NPCS.get(npc_id)
        if npc:
            return npc.get('name', 'NPC')

        return 'NPC'


class DungeonSystem:
    """Manages dungeon exploration"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.current_floor = 1
        self.dungeon_layout = None

    def enter_dungeon(self, dungeon_id):
        """
        Enter dungeon

        Args:
            dungeon_id: Dungeon identifier

        Returns:
            bool: Success
        """
        from data.dungeons import DUNGEONS

        dungeon = DUNGEONS.get(dungeon_id)
        if not dungeon:
            return False

        # Generate or load layout
        if dungeon.get('random_layout'):
            self.dungeon_layout = self.generate_dungeon_layout(dungeon)
        else:
            self.dungeon_layout = dungeon.get('layout')

        self.current_floor = 1

        return True

    def generate_dungeon_layout(self, dungeon):
        """
        Generate random dungeon layout

        Args:
            dungeon: Dungeon data

        Returns:
            dict: Layout
        """
        # Simple random dungeon generation
        import random

        num_floors = dungeon.get('num_floors', 3)
        rooms_per_floor = dungeon.get('rooms_per_floor', 5)

        layout = {
            'floors': []
        }

        for floor in range(num_floors):
            floor_data = {
                'floor': floor + 1,
                'rooms': []
            }

            for room in range(rooms_per_floor):
                room_data = {
                    'id': f'floor_{floor + 1}_room_{room + 1}',
                    'connections': []
                }

                # Connect to adjacent rooms
                if room > 0:
                    room_data['connections'].append(f'floor_{floor + 1}_room_{room}')
                if room < rooms_per_floor - 1:
                    room_data['connections'].append(f'floor_{floor + 1}_room_{room + 2}')

                floor_data['rooms'].append(room_data)

            layout['floors'].append(floor_data)

        return layout

    def check_for_yipp_spawn(self, dungeon_id):
        """
        Check if this dungeon should spawn Yipp

        Args:
            dungeon_id: Dungeon identifier

        Returns:
            bool: Should spawn
        """
        # Check if Yipp already encountered
        if self.game_state.story_flags.get('yipp_encountered'):
            return False

        # Check if met Orisia (too late)
        if self.game_state.story_flags.get('met_orisia'):
            return False

        # Check if this is the designated Yipp dungeon
        yipp_dungeon = self.game_state.story_flags.get('yipp_spawn_dungeon')
        return yipp_dungeon == dungeon_id
