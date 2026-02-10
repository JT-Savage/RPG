"""
Main Game Class
Central game loop and scene management
"""

from scene import *
import ui

# Import all systems
from utils.game_state import GameState
from utils.save_system import save_game, load_game
from utils.dialogue_system import DialogueSystem
from utils.shop_system import ShopSystem
from utils.menu_system import MenuSystem
from utils.recruitment_system import RecruitmentSystem
from utils.story_event_system import StoryEventSystem
from utils.encounter_system import EncounterSystem
from utils.map_system import MapSystem, NPCSystem
from utils.battle_engine import BattleEngine
from utils.level_up_system import distribute_battle_exp

# Import scenes
from scenes.battle import BattleScene


class GameRoot:
    """Main game controller"""

    def __init__(self):
        # Game state
        self.game_state = None

        # Systems
        self.dialogue_system = None
        self.shop_system = None
        self.menu_system = None
        self.recruitment_system = None
        self.story_event_system = None
        self.encounter_system = None
        self.map_system = None
        self.npc_system = None

        # Scene management
        self.current_scene = None
        self.scene_stack = []

        # Input state
        self.keys_pressed = set()

        # Game running
        self.running = True

    def new_game(self):
        """Start new game"""
        # Initialize game state
        self.game_state = GameState()
        self.game_state.initialize_new_game()

        # Initialize systems
        self.initialize_systems()

        # Start tutorial
        self.start_tutorial()

    def load_game_from_file(self, filename='autosave.json'):
        """Load game from save file"""
        self.game_state = load_game(filename)

        if self.game_state:
            self.initialize_systems()
            # Load map position
            self.map_system.enter_location(self.game_state.current_location)
            return True

        return False

    def initialize_systems(self):
        """Initialize all game systems"""
        self.dialogue_system = DialogueSystem(self.game_state)
        self.shop_system = ShopSystem(self.game_state)
        self.menu_system = MenuSystem(self.game_state)
        self.recruitment_system = RecruitmentSystem(self.game_state)
        self.story_event_system = StoryEventSystem(self.game_state)
        self.encounter_system = EncounterSystem(self.game_state)
        self.map_system = MapSystem(self.game_state)
        self.npc_system = NPCSystem(self.game_state)

    def start_tutorial(self):
        """Start tutorial sequence"""
        # Trigger intro event
        event = self.story_event_system.trigger_event('intro_cutscene')

        # Show intro dialogue
        self.dialogue_system.start_dialogue('intro_tutorial')

        # Start in tutorial warren
        self.map_system.enter_location('tutorial_warren')

    def update(self, dt):
        """
        Main game update loop

        Args:
            dt: Delta time
        """
        if not self.running:
            return

        # Update current scene if any
        if self.current_scene:
            if hasattr(self.current_scene, 'update'):
                self.current_scene.update()

            # Check if scene ended
            if hasattr(self.current_scene, 'scene_ended'):
                if self.current_scene.scene_ended:
                    self.pop_scene()

        # Update dialogue if active
        elif self.dialogue_system.is_dialogue_active():
            # Dialogue handling (advance with action button)
            pass

        # Update menu if open
        elif self.menu_system.is_menu_open():
            # Menu handling
            pass

        # Update exploration
        else:
            self.update_exploration(dt)

    def update_exploration(self, dt):
        """Update exploration mode"""
        # Handle movement
        dx, dy = 0, 0

        if 'w' in self.keys_pressed or 'up' in self.keys_pressed:
            dy = -1
        if 's' in self.keys_pressed or 'down' in self.keys_pressed:
            dy = 1
        if 'a' in self.keys_pressed or 'left' in self.keys_pressed:
            dx = -1
        if 'd' in self.keys_pressed or 'right' in self.keys_pressed:
            dx = 1

        if dx != 0 or dy != 0:
            # Move player
            moved = self.map_system.move_player(dx, dy)

            if moved:
                # Check for random encounter
                encounter = self.encounter_system.update_step()

                if encounter:
                    self.start_battle(encounter)

                # Check for location trigger
                trigger = self.map_system.check_location_trigger()

                if trigger:
                    self.handle_location_trigger(trigger)

    def start_battle(self, enemy_ids):
        """
        Start battle

        Args:
            enemy_ids: List of enemy IDs
        """
        # Create battle scene
        background = self.encounter_system.get_encounter_background()
        can_flee = self.encounter_system.can_flee_current_region()

        battle_scene = BattleScene(
            self,
            self.game_state,
            enemy_ids,
            can_flee=can_flee,
            background=background
        )

        self.push_scene(battle_scene)

    def handle_location_trigger(self, trigger):
        """Handle location trigger"""
        trigger_type = trigger.get('type')

        if trigger_type == 'door' or trigger_type == 'warp':
            target_location = trigger.get('target_location')
            self.map_system.enter_location(target_location)

        elif trigger_type == 'event':
            event_id = trigger.get('event_id')
            self.story_event_system.trigger_event(event_id)

    def interact(self):
        """Handle interaction (talk to NPC, open chest, etc.)"""
        # Check for NPC
        npc_id = self.map_system.check_npc_interaction()

        if npc_id:
            result = self.npc_system.interact_with_npc(npc_id)

            if result:
                interaction_type = result.get('type')

                if interaction_type == 'dialogue':
                    self.dialogue_system.start_dialogue(result['dialogue_id'])

                elif interaction_type == 'shop':
                    self.shop_system.open_shop(result['shop_id'])

                elif interaction_type == 'recruitment':
                    # Show recruitment dialogue
                    char_id = result['character_id']
                    dialogue_id = f'recruit_{char_id}'
                    self.dialogue_system.start_dialogue(dialogue_id)

                elif interaction_type == 'quest':
                    # Start quest
                    pass

                elif interaction_type == 'generic':
                    # Show message
                    print(result['message'])

    def open_menu(self):
        """Open main menu"""
        self.menu_system.open_menu('main')

    def push_scene(self, scene):
        """Push new scene"""
        if self.current_scene:
            self.scene_stack.append(self.current_scene)

        self.current_scene = scene

    def pop_scene(self):
        """Pop scene"""
        if self.scene_stack:
            self.current_scene = self.scene_stack.pop()
        else:
            self.current_scene = None

    def save_game_to_file(self, filename='autosave.json'):
        """Save game"""
        # Save map position
        position_data = self.map_system.save_position()
        self.game_state.map_position = position_data

        return save_game(self.game_state, filename)

    def quit_game(self):
        """Quit game"""
        # Autosave
        self.save_game_to_file('autosave.json')
        self.running = False

    # Input handlers
    def key_down(self, key):
        """Handle key down"""
        self.keys_pressed.add(key)

        # Special keys
        if key == 'escape':
            if self.menu_system.is_menu_open():
                self.menu_system.close_menu()
            elif self.dialogue_system.is_dialogue_active():
                pass  # Cannot cancel dialogue
            else:
                self.open_menu()

        elif key == 'return' or key == 'space':
            # Interact / Advance dialogue
            if self.dialogue_system.is_dialogue_active():
                self.dialogue_system.advance_dialogue()
            else:
                self.interact()

    def key_up(self, key):
        """Handle key up"""
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)


# For Pythonista Scene framework
class GameScene(Scene):
    """Pythonista Scene wrapper for game"""

    def setup(self):
        """Setup scene"""
        self.game = GameRoot()
        self.game.new_game()

    def update(self):
        """Update scene"""
        self.game.update(1/60.0)  # 60 FPS

    def draw(self):
        """Draw scene"""
        background(0.2, 0.2, 0.3)

        # Draw current scene
        if self.game.current_scene:
            if hasattr(self.game.current_scene, 'draw'):
                self.game.current_scene.draw()
        else:
            # Draw exploration
            self.draw_exploration()

    def draw_exploration(self):
        """Draw exploration mode"""
        # Draw map (placeholder)
        fill(0.3, 0.5, 0.3)
        rect(0, 0, 256, 224)

        # Draw player
        fill(0.8, 0.8, 0.2)
        pos = self.game.map_system.player_position
        ellipse(pos[0] - 8, pos[1] - 8, 16, 16)

        # Draw location name
        fill(1, 1, 1)
        location_name = self.game.map_system.get_current_location_name()
        text(location_name, 'Futura', 14, 128, 200, alignment=5)

    def touch_began(self, touch):
        """Handle touch"""
        # Convert to logical coordinates
        logical_x = touch.location.x
        logical_y = touch.location.y

        if self.game.current_scene:
            if hasattr(self.game.current_scene, 'touch_began'):
                self.game.current_scene.touch_began(touch, logical_x, logical_y)

    def touch_moved(self, touch):
        """Handle touch move"""
        logical_x = touch.location.x
        logical_y = touch.location.y

        if self.game.current_scene:
            if hasattr(self.game.current_scene, 'touch_moved'):
                self.game.current_scene.touch_moved(touch, logical_x, logical_y)

    def touch_ended(self, touch):
        """Handle touch end"""
        logical_x = touch.location.x
        logical_y = touch.location.y

        if self.game.current_scene:
            if hasattr(self.game.current_scene, 'touch_ended'):
                self.game.current_scene.touch_ended(touch, logical_x, logical_y)


# Entry point
if __name__ == '__main__':
    run(GameScene(), PORTRAIT, show_fps=True)
