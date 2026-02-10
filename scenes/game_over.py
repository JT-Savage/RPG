"""
Game Over Screen
Displayed when party is defeated
"""

from scene import *
import ui


class GameOverScreen:
    """Game over scene"""

    def __init__(self, game_root):
        self.game_root = game_root
        self.menu_options = ['Load Last Save', 'Return to Title', 'Quit']
        self.selected_index = 0
        self.scene_ended = False
        self.fade_alpha = 0.0
        self.fade_in_complete = False

    def update(self):
        """Update game over screen"""
        # Fade in effect
        if not self.fade_in_complete:
            self.fade_alpha += 0.02
            if self.fade_alpha >= 1.0:
                self.fade_alpha = 1.0
                self.fade_in_complete = True

    def draw(self):
        """Draw game over screen"""
        # Dark background
        fill(0.05, 0.05, 0.1, self.fade_alpha)
        rect(0, 0, 256, 224)

        # Game Over text
        fill(0.8, 0.2, 0.2, self.fade_alpha)  # Red
        text('GAME OVER', 'Futura', 28, 128, 160, alignment=5)

        # Flavor text
        if self.fade_in_complete:
            fill(0.7, 0.7, 0.7)
            text('Your party has been defeated...', 'Futura', 12, 128, 135, alignment=5)

            # Menu options
            for i, option in enumerate(self.menu_options):
                y = 100 - i * 22

                # Highlight selected
                if i == self.selected_index:
                    fill(0.3, 0.3, 0.5)
                    rect(68, y - 2, 120, 20)

                # Draw option
                fill(1, 1, 1)
                text(option, 'Futura', 14, 128, y + 12, alignment=5)

    def handle_input(self, key):
        """Handle keyboard input"""
        if not self.fade_in_complete:
            return

        if key == 'up' or key == 'w':
            self.selected_index = (self.selected_index - 1) % len(self.menu_options)

        elif key == 'down' or key == 's':
            self.selected_index = (self.selected_index + 1) % len(self.menu_options)

        elif key == 'return' or key == 'space':
            self.select_option()

    def select_option(self):
        """Select menu option"""
        option = self.menu_options[self.selected_index]

        if option == 'Load Last Save':
            success = self.game_root.load_game_from_file('autosave.json')
            if success:
                self.scene_ended = True
            else:
                print("No save file found")

        elif option == 'Return to Title':
            # Reset to title screen
            from scenes.title_screen import TitleScreen
            self.game_root.current_scene = TitleScreen(self.game_root)
            self.scene_ended = True

        elif option == 'Quit':
            self.game_root.quit_game()

    def touch_began(self, touch, logical_x, logical_y):
        """Handle touch input"""
        if not self.fade_in_complete:
            return

        # Check menu options
        for i in range(len(self.menu_options)):
            y = 100 - i * 22

            if 68 <= logical_x <= 188 and y - 2 <= logical_y <= y + 18:
                self.selected_index = i
                self.select_option()
                break
