"""
Title Screen scene
"""

from scene import *
import ui

class TitleScreen:
    """Title screen with menu options"""

    def __init__(self, game_root):
        self.game_root = game_root
        self.menu_options = [
            'New Game',
            'Continue',
            'Load Game',
            'Settings',
            'Exit'
        ]
        self.selected_index = 0
        self.title_text = "THERE WILL BE KOBOLDS"
        self.subtitle_text = "A Dark Fantasy JRPG"

        # Touch regions for menu buttons
        self.button_height = 20
        self.button_spacing = 8
        self.menu_start_y = 80

    def update(self):
        """Update title screen logic"""
        pass

    def draw(self):
        """Draw title screen"""
        # Background
        fill(0.1, 0.1, 0.15)  # Dark blue-gray
        rect(0, 0, 256, 224)

        # Title
        fill(1, 1, 1)  # White
        text(self.title_text, 'Futura', 20, 128, 180, alignment=5)

        # Subtitle
        fill(0.8, 0.8, 0.8)  # Light gray
        text(self.subtitle_text, 'Futura', 12, 128, 160, alignment=5)

        # Menu options
        for i, option in enumerate(self.menu_options):
            y = self.menu_start_y - (i * (self.button_height + self.button_spacing))

            # Highlight selected option
            if i == self.selected_index:
                fill(0.3, 0.3, 0.5)  # Blue highlight
                rect(48, y, 160, self.button_height)

            # Draw option text
            fill(1, 1, 1)
            text(option, 'Futura', 14, 128, y + self.button_height/2, alignment=5)

    def touch_began(self, touch, logical_x, logical_y):
        """Handle touch input"""
        # Check which menu option was touched
        for i, option in enumerate(self.menu_options):
            y = self.menu_start_y - (i * (self.button_height + self.button_spacing))

            if (48 <= logical_x <= 208 and
                y <= logical_y <= y + self.button_height):
                self.selected_index = i
                self.handle_menu_selection(option)
                break

    def touch_moved(self, touch, logical_x, logical_y):
        """Handle touch movement"""
        pass

    def touch_ended(self, touch, logical_x, logical_y):
        """Handle touch end"""
        pass

    def handle_menu_selection(self, option):
        """Handle menu option selection"""
        if option == 'New Game':
            print("Starting new game...")
            # TODO: Transition to game start
        elif option == 'Continue':
            print("Continuing from autosave...")
            # TODO: Load autosave
        elif option == 'Load Game':
            print("Opening load menu...")
            # TODO: Open load game menu
        elif option == 'Settings':
            print("Opening settings...")
            # TODO: Open settings
        elif option == 'Exit':
            print("Exiting game...")
            # TODO: Exit application
