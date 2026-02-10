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
from scenes.title_screen import TitleScreen

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
        self.game_state = {
            'current_scene': 'title',
            'save_data': None
        }

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
        with ui.GState():
            translate(self.offset_x, self.offset_y)
            scale(self.scale, self.scale)

            if self.current_scene:
                self.current_scene.draw()

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

if __name__ == '__main__':
    run(GameRoot(), orientation=LANDSCAPE, frame_interval=2)
