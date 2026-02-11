"""
There Will Be Kobolds - A Final Fantasy Style JRPG
Main entry point for the game

Technical Specs:
- Pythonista scene module exclusively
- Logical Resolution: 256x224 pixels (scaled to device)
- Landscape orientation only
- Touch controls, two-handed gameplay
- 16x16 pixel tiles, 16x24 character sprites
"""

from scene import *
import sound
import random
import ui
from scenes.title_screen import TitleScreen

# Import game systems
try:
    from utils.game_state import GameState
    from utils.save_system import save_game, load_game
    from utils.dialogue_system import DialogueSystem
    from utils.shop_system import ShopSystem
    from utils.menu_system import MenuSystem
    from utils.recruitment_system import RecruitmentSystem
    from utils.story_event_system import StoryEventSystem
    from utils.encounter_system import EncounterSystem
    from utils.map_system import MapSystem, NPCSystem
    from scenes.battle import BattleScene
    SYSTEMS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import game systems: {e}")
    SYSTEMS_AVAILABLE = False

class GameRoot(Scene):
    """Root scene that manages all game scenes"""

    def setup(self):
        """Initialize the game"""
        self.logical_width = 256
        self.logical_height = 224

        # Calculate scaling factor to fit device screen
        self.scale = min(
            self.size.width / self.logical_width,
            self.size.height / self.logical_height
        )

        # Calculate offset to center the game
        self.offset_x = (self.size.width - (self.logical_width * self.scale)) / 2
        self.offset_y = (self.size.height - (self.logical_height * self.scale)) / 2

        # Initialize game state
        self.game_state_data = None
        self.game_systems_initialized = False

        # Game systems (initialized when starting new game)
        self.dialogue_system = None
        self.shop_system = None
        self.menu_system = None
        self.recruitment_system = None
        self.story_event_system = None
        self.encounter_system = None
        self.map_system = None
        self.npc_system = None

        # Load title screen
        self.current_scene = TitleScreen(self)

    def update(self):
        """Update current scene"""
        if self.current_scene:
            self.current_scene.update()

    def draw(self):
        """Draw current scene with scaling"""
        background(0, 0, 0)  # Black background

        # Apply transformation for logical resolution
        with GState():
            translate(self.offset_x, self.offset_y)
            scale(self.scale, self.scale)

            if self.current_scene:
                self.current_scene.draw()
            elif self.game_systems_initialized:
                # Draw exploration mode
                self.draw_exploration()

    def touch_began(self, touch):
        """Handle touch input"""
        # Convert touch coordinates to logical coordinates
        logical_x = (touch.location.x - self.offset_x) / self.scale
        logical_y = (touch.location.y - self.offset_y) / self.scale

        if self.current_scene:
            self.current_scene.touch_began(touch, logical_x, logical_y)

    def touch_moved(self, touch):
        """Handle touch movement"""
        logical_x = (touch.location.x - self.offset_x) / self.scale
        logical_y = (touch.location.y - self.offset_y) / self.scale

        if self.current_scene:
            self.current_scene.touch_moved(touch, logical_x, logical_y)

    def touch_ended(self, touch):
        """Handle touch end"""
        logical_x = (touch.location.x - self.offset_x) / self.scale
        logical_y = (touch.location.y - self.offset_y) / self.scale

        if self.current_scene:
            self.current_scene.touch_ended(touch, logical_x, logical_y)

    def switch_scene(self, scene_name, **kwargs):
        """Switch to a different scene"""
        # Import and instantiate the appropriate scene
        # This will be expanded as we add more scenes
        pass

    def new_game(self):
        """Start new game"""
        if not SYSTEMS_AVAILABLE:
            print("Game systems not available. Cannot start game.")
            return

        print("Initializing new game...")

        # Initialize game state
        self.game_state_data = GameState()
        self.game_state_data.reset_new_game()

        # Initialize systems
        self.initialize_game_systems()

        # Close title screen
        self.current_scene = None
        self.game_systems_initialized = True

        print("Game started! (Exploration mode)")

    def load_game_from_file(self, filename='autosave.json'):
        """Load game from save file"""
        if not SYSTEMS_AVAILABLE:
            print("Game systems not available. Cannot load game.")
            return False

        print(f"Loading game from {filename}...")

        self.game_state_data = load_game(filename)

        if self.game_state_data:
            self.initialize_game_systems()
            self.current_scene = None
            self.game_systems_initialized = True
            print("Game loaded!")
            return True
        else:
            print("No save file found")
            return False

    def initialize_game_systems(self):
        """Initialize all game systems"""
        if not SYSTEMS_AVAILABLE or not self.game_state_data:
            return

        self.dialogue_system = DialogueSystem(self.game_state_data)
        self.shop_system = ShopSystem(self.game_state_data)
        self.menu_system = MenuSystem(self.game_state_data)
        self.recruitment_system = RecruitmentSystem(self.game_state_data)
        self.story_event_system = StoryEventSystem(self.game_state_data)
        self.encounter_system = EncounterSystem(self.game_state_data)
        self.map_system = MapSystem(self.game_state_data)
        self.npc_system = NPCSystem(self.game_state_data)

        # Enter starting location
        if hasattr(self.map_system, 'enter_location'):
            self.map_system.enter_location(self.game_state_data.current_location)

        print("Game systems initialized")

    def quit_game(self):
        """Quit game"""
        print("Quitting game...")

        # Autosave if game is running
        if self.game_systems_initialized and self.game_state_data:
            print("Autosaving...")
            save_game(self.game_state_data, 'autosave.json')

        self.close()

    def draw_exploration(self):
        """Draw exploration mode"""
        # Background (grass/ground)
        fill(0.2, 0.4, 0.2)
        rect(0, 0, self.logical_width, self.logical_height)

        # Player (centered)
        if self.map_system and hasattr(self.map_system, 'player_position'):
            player_x, player_y = self.map_system.player_position
        else:
            player_x, player_y = self.logical_width // 2, self.logical_height // 2

        fill(1, 0.8, 0.2)  # Yellow for player
        ellipse(player_x - 8, player_y - 12, 16, 24)

        # Location name at top
        if self.map_system:
            location_name = self.map_system.get_current_location_name()
        else:
            location_name = "Unknown"

        fill(1, 1, 1)
        text(location_name, 'Futura', 14, self.logical_width // 2, self.logical_height - 20, alignment=5)

        # Instructions at bottom
        fill(0.8, 0.8, 0.8)
        text("Tap to interact | Menu not yet implemented", 'Futura', 10, self.logical_width // 2, 10, alignment=5)

if __name__ == '__main__':
    run(GameRoot(), orientation=LANDSCAPE, frame_interval=2)
