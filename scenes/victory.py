"""
Victory Screen
Displayed after defeating the final boss
"""

from scene import *
import ui


class VictoryScreen:
    """Victory/Ending scene"""

    def __init__(self, game_root):
        self.game_root = game_root
        self.scene_ended = False
        self.credits_scroll = 0
        self.credits_speed = 0.5
        self.show_post_credits_prompt = False

        # Ending text based on game state
        self.ending_text = self.generate_ending_text()

        # Credits
        self.credits = [
            '',
            'THERE WILL BE KOBOLDS',
            '',
            'Created by Claude & User',
            '',
            '',
            'STORY',
            'Necromantic Plague',
            'Kobold Liberation',
            'Lost Allies',
            '',
            '',
            'CHARACTERS',
            'Frostbite - The Gunner',
            'Fei - The Monk Panda',
            'Michael - The Cleric',
            'Flood - The Ice Mage',
            'Hannah - The Elementalist',
            'Warghoul - The Necromancer',
            'Cookie - The Druidess',
            'Iris - The Shapeshifter',
            'Javin - The Dragon Knight',
            'Fritzzit - The Sniper',
            'Crankpot - The Arsonist',
            'Yipp - The ???',
            '',
            '',
            'SPECIAL THANKS',
            'To all who helped save the kobolds',
            '',
            '',
            '--- THE END ---',
            '',
            '',
            'But wait...',
            'One more challenge remains...',
            '',
            'Press ENTER to face Captain Donald'
        ]

    def generate_ending_text(self):
        """Generate ending text based on game state"""
        game_state = self.game_root.game_state

        lines = [
            'The necromancer has been defeated.',
            'The undead plague is ended.',
            ''
        ]

        # Check for lost characters
        if game_state.lost_characters:
            lines.append(f'However, {len(game_state.lost_characters)} allies were lost...')
            for char_id in game_state.lost_characters:
                lines.append(f'  {char_id.title()} - Fallen')
            lines.append('')

        # Check if Flood sacrificed
        if game_state.story_flags.get('flood_sacrificed'):
            lines.append('Flood gave his life to seal the evil.')
            lines.append('His sacrifice will not be forgotten.')
            lines.append('')

        # Check Yipp alignment
        yipp_alignment = game_state.story_flags.get('yipp_alignment')
        if yipp_alignment == 'vampire':
            lines.append('Yipp betrayed the party and joined the Lich.')
            lines.append('But even that could not stop you.')
            lines.append('')

        # Check party size
        party_count = len(game_state.characters_recruited)
        if party_count == 12:
            lines.append('You recruited all allies!')
            lines.append('PERFECT ENDING')
            lines.append('')
        elif party_count >= 8:
            lines.append('You saved most of the allies.')
            lines.append('GOOD ENDING')
            lines.append('')
        else:
            lines.append('Many potential allies were lost.')
            lines.append('NORMAL ENDING')
            lines.append('')

        lines.append('The kobolds are free.')
        lines.append('Peace has returned to the land.')
        lines.append('')
        lines.append('Thank you for playing!')

        return lines

    def update(self):
        """Update victory screen"""
        # Scroll credits
        self.credits_scroll += self.credits_speed

        # Check if credits finished
        if self.credits_scroll > len(self.credits) * 15 + 240:
            self.show_post_credits_prompt = True

    def draw(self):
        """Draw victory screen"""
        # Background
        fill(0.05, 0.05, 0.1)
        rect(0, 0, 256, 224)

        if self.credits_scroll < 200:
            # Show ending text
            fill(1, 1, 1)
            for i, line in enumerate(self.ending_text):
                y = 180 - i * 12 - self.credits_scroll
                if 0 <= y <= 224:
                    text(line, 'Futura', 10, 128, y, alignment=5)

        else:
            # Show scrolling credits
            fill(1, 1, 1)
            for i, line in enumerate(self.credits):
                y = 224 - (self.credits_scroll - 200) + i * 15
                if 0 <= y <= 224:
                    if line == 'THERE WILL BE KOBOLDS':
                        text(line, 'Futura', 16, 128, y, alignment=5)
                    elif line in ['STORY', 'CHARACTERS', 'SPECIAL THANKS']:
                        fill(1, 1, 0.5)  # Yellow headers
                        text(line, 'Futura', 12, 128, y, alignment=5)
                        fill(1, 1, 1)  # Back to white
                    else:
                        text(line, 'Futura', 10, 128, y, alignment=5)

        # Post-credits prompt
        if self.show_post_credits_prompt:
            fill(0.1, 0.1, 0.2, 0.9)
            rect(0, 0, 256, 224)

            fill(1, 1, 0.5)
            text('SECRET BOSS UNLOCKED', 'Futura', 16, 128, 140, alignment=5)

            fill(1, 1, 1)
            text('Face Captain Donald', 'Futura', 12, 128, 115, alignment=5)
            text('The slaver who started it all', 'Futura', 10, 128, 100, alignment=5)

            fill(0.8, 0.8, 0.8)
            text('Press ENTER to continue', 'Futura', 10, 128, 60, alignment=5)
            text('Press ESC to return to title', 'Futura', 10, 128, 45, alignment=5)

    def handle_input(self, key):
        """Handle keyboard input"""
        if self.show_post_credits_prompt:
            if key == 'return' or key == 'space':
                # Start post-credits boss
                self.trigger_post_credits_boss()

            elif key == 'escape':
                # Return to title
                from scenes.title_screen import TitleScreen
                self.game_root.current_scene = TitleScreen(self.game_root)
                self.scene_ended = True

        else:
            # Skip credits
            if key == 'return' or key == 'space':
                self.credits_scroll = len(self.credits) * 15 + 240
                self.show_post_credits_prompt = True

    def trigger_post_credits_boss(self):
        """Trigger Captain Donald post-credits boss"""
        # Trigger story event
        self.game_root.story_event_system.trigger_captain_donald_reveal()

        # Start battle
        from utils.encounter_system import EncounterSystem
        encounter_system = EncounterSystem(self.game_root.game_state)
        boss_encounter = encounter_system.post_credits_boss_encounter()

        self.game_root.start_battle(boss_encounter['enemies'])
        self.scene_ended = True

    def touch_began(self, touch, logical_x, logical_y):
        """Handle touch input"""
        if self.show_post_credits_prompt:
            # Tapping anywhere triggers boss
            self.trigger_post_credits_boss()
        else:
            # Skip credits
            self.credits_scroll = len(self.credits) * 15 + 240
            self.show_post_credits_prompt = True
