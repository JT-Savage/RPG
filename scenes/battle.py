"""
Battle Scene
Turn-based combat UI and flow
"""

from scene import *
import ui
from utils.battle_engine import BattleEngine
from utils.level_up_system import distribute_battle_exp

class BattleScene:
    """Battle scene with turn-based combat"""

    def __init__(self, game_root, game_state, enemy_ids, can_flee=True, background='default'):
        self.game_root = game_root
        self.game_state = game_state
        self.background_type = background

        # Initialize battle engine
        self.battle = BattleEngine(game_state, enemy_ids, can_flee)

        # UI state
        self.selected_action = None
        self.selected_target = None
        self.selected_spell = None
        self.selected_item = None

        self.menu_state = 'main'  # 'main', 'magic', 'item', 'target'
        self.menu_selection = 0

        # Battle log
        self.battle_log = []
        self.max_log_lines = 5

        # Animation state
        self.animating = False
        self.animation_timer = 0

    def update(self):
        """Update battle logic"""
        if self.battle.battle_over:
            self.handle_battle_end()
            return

        if self.animating:
            self.animation_timer -= 1
            if self.animation_timer <= 0:
                self.animating = False
            return

        # Get current actor
        actor = self.battle.get_current_actor()

        if not actor:
            return

        # Handle actor turn
        if actor['type'] == 'enemy':
            self.execute_enemy_turn(actor)
        else:  # player
            # Wait for player input
            pass

    def execute_enemy_turn(self, enemy):
        """
        Execute enemy AI turn

        Args:
            enemy: Enemy actor
        """
        action = self.battle.ai_select_action(enemy)

        if action['action'] == 'attack':
            result = self.battle.execute_attack(enemy, action['target'])
            self.log_action(result)

        elif action['action'] == 'ability':
            # Execute ability (simplified)
            result = self.battle.execute_attack(enemy, action['target'])
            result['action'] = 'ability'
            result['ability_name'] = action['ability']
            self.log_action(result)

        # Animate
        self.animating = True
        self.animation_timer = 30  # 0.5 seconds at 60 FPS

        # Next turn
        self.battle.next_turn()

    def execute_player_action(self, action_type, target=None, spell_id=None, item_id=None):
        """
        Execute player action

        Args:
            action_type: 'attack', 'magic', 'item', 'defend', 'flee'
            target: Target dict
            spell_id: Spell ID (if magic)
            item_id: Item ID (if item)
        """
        actor = self.battle.get_current_actor()

        if not actor or actor['type'] != 'player':
            return

        result = None

        if action_type == 'attack':
            result = self.battle.execute_attack(actor, target)

        elif action_type == 'magic':
            targets = [target] if target else []
            result = self.battle.execute_magic(actor, spell_id, targets)

        elif action_type == 'item':
            result = self.battle.execute_item(actor, item_id, target)

        elif action_type == 'defend':
            result = self.battle.execute_defend(actor)

        elif action_type == 'flee':
            if self.battle.attempt_flee():
                self.log_message("Fled from battle!")
                self.handle_battle_end()
                return
            else:
                self.log_message("Couldn't escape!")

        if result:
            self.log_action(result)

        # Animate
        self.animating = True
        self.animation_timer = 30

        # Next turn
        self.battle.next_turn()

        # Reset menu
        self.menu_state = 'main'
        self.menu_selection = 0

    def log_action(self, result):
        """
        Log battle action to battle log

        Args:
            result: Action result dict
        """
        actor = result.get('actor')
        action = result.get('action')

        actor_name = actor['id'] if actor['type'] == 'player' else actor['id']

        if action == 'attack':
            target = result.get('target')
            target_name = target['id'] if target['type'] == 'player' else target['id']
            damage = result.get('damage', 0)

            msg = f"{actor_name} attacks {target_name} for {damage} damage!"

            if result.get('critical'):
                msg += " CRITICAL!"

            self.log_message(msg)

        elif action == 'magic':
            spell = result.get('spell')
            msg = f"{actor_name} casts {spell}!"
            self.log_message(msg)

            for target_result in result.get('targets', []):
                target = target_result['target']
                target_name = target['id'] if target['type'] == 'player' else target['id']

                if 'damage' in target_result:
                    self.log_message(f"  {target_name} takes {target_result['damage']} damage!")
                if 'healing' in target_result:
                    self.log_message(f"  {target_name} heals {target_result['healing']} HP!")

        elif action == 'item':
            item = result.get('item')
            target = result.get('target')
            target_name = target['id'] if target['type'] == 'player' else target['id']

            self.log_message(f"{actor_name} uses {item} on {target_name}!")

        elif action == 'defend':
            self.log_message(f"{actor_name} defends!")

    def log_message(self, message):
        """Add message to battle log"""
        self.battle_log.append(message)

        if len(self.battle_log) > self.max_log_lines:
            self.battle_log.pop(0)

    def handle_battle_end(self):
        """Handle battle end (victory, defeat, flee)"""
        if self.battle.fled:
            # Return to map
            self.game_root.current_scene = None  # Would switch to map scene
            return

        if self.battle.victory:
            # Get rewards
            rewards = self.battle.get_battle_rewards()

            # Award EXP and Gil
            self.game_state.gil += rewards['gil']
            exp_results = distribute_battle_exp(self.game_state, rewards['exp'])

            # Show victory screen
            self.log_message(f"Victory! Gained {rewards['exp']} EXP and {rewards['gil']} Gil!")

            # Check level-ups
            for char_id, result in exp_results.items():
                if result['leveled_up']:
                    self.log_message(f"{char_id} reached level {result['new_level']}!")

                    for ability in result.get('abilities_learned', []):
                        self.log_message(f"{char_id} learned {ability['name']}!")

            # TODO: Show victory screen UI
            # For now, just return
            self.game_root.current_scene = None

        else:  # defeat
            # Game over
            self.log_message("Party defeated...")
            # TODO: Show game over screen
            self.game_root.current_scene = None

    def draw(self):
        """Draw battle scene"""
        # Background
        self.draw_background()

        # Enemies
        self.draw_enemies()

        # Party
        self.draw_party()

        # Battle menu
        self.draw_battle_menu()

        # Battle log
        self.draw_battle_log()

        # Turn indicator
        actor = self.battle.get_current_actor()
        if actor:
            self.draw_turn_indicator(actor)

    def draw_background(self):
        """Draw battle background"""
        # Simple colored background based on type
        backgrounds = {
            'default': (0.2, 0.2, 0.3),
            'forest': (0.1, 0.3, 0.1),
            'desert': (0.4, 0.35, 0.2),
            'graveyard': (0.15, 0.15, 0.2),
            'catacombs': (0.1, 0.1, 0.15)
        }

        color = backgrounds.get(self.background_type, (0.2, 0.2, 0.3))
        fill(*color)
        rect(0, 0, 256, 224)

    def draw_enemies(self):
        """Draw enemy sprites and HP bars"""
        alive_enemies = [e for e in self.battle.enemies if e['hp'] > 0]

        for i, enemy in enumerate(alive_enemies):
            # Enemy position (right side)
            x = 180 + (i % 2) * 30
            y = 150 - (i // 2) * 40

            # Enemy sprite (placeholder rectangle)
            fill(0.8, 0.2, 0.2)
            rect(x, y, 24, 24)

            # HP bar
            hp_percent = enemy['hp'] / enemy['max_hp']
            self.draw_hp_bar(x, y - 8, 24, hp_percent)

    def draw_party(self):
        """Draw party member sprites and HP/MP bars"""
        for i, member in enumerate(self.battle.party):
            if member['data']['hp'] <= 0:
                continue  # Skip dead members

            # Party position (left side)
            x = 20
            y = 150 - i * 50

            # Character sprite (placeholder)
            fill(0.2, 0.6, 0.8)
            rect(x, y, 24, 24)

            # Name
            fill(1, 1, 1)
            text(member['id'], 'Futura', 10, x + 30, y + 18)

            # HP bar
            hp_percent = member['data']['hp'] / member['data']['max_hp']
            self.draw_hp_bar(x + 30, y + 10, 60, hp_percent)

            # MP bar
            if member['data']['max_mp'] > 0:
                mp_percent = member['data']['mp'] / member['data']['max_mp']
                self.draw_mp_bar(x + 30, y + 4, 60, mp_percent)

            # HP/MP text
            fill(1, 1, 1)
            text(f"HP: {member['data']['hp']}/{member['data']['max_hp']}",
                 'Futura', 8, x + 30, y + 8)
            text(f"MP: {member['data']['mp']}/{member['data']['max_mp']}",
                 'Futura', 8, x + 30, y + 2)

    def draw_hp_bar(self, x, y, width, percent):
        """Draw HP bar"""
        # Background
        fill(0.3, 0.3, 0.3)
        rect(x, y, width, 4)

        # HP fill
        if percent > 0.5:
            fill(0.2, 0.8, 0.2)  # Green
        elif percent > 0.25:
            fill(0.8, 0.8, 0.2)  # Yellow
        else:
            fill(0.8, 0.2, 0.2)  # Red

        rect(x, y, width * percent, 4)

    def draw_mp_bar(self, x, y, width, percent):
        """Draw MP bar"""
        # Background
        fill(0.3, 0.3, 0.3)
        rect(x, y, width, 3)

        # MP fill
        fill(0.2, 0.4, 0.8)  # Blue
        rect(x, y, width * percent, 3)

    def draw_battle_menu(self):
        """Draw battle command menu"""
        # Menu background
        fill(0.1, 0.1, 0.2, 0.9)
        rect(10, 10, 100, 60)

        # Menu options
        options = ['Attack', 'Magic', 'Item', 'Defend']
        if self.battle.can_flee:
            options.append('Flee')

        for i, option in enumerate(options):
            y = 60 - i * 12

            # Highlight selected
            if i == self.menu_selection and self.menu_state == 'main':
                fill(0.3, 0.3, 0.5)
                rect(12, y - 1, 96, 11)

            # Draw option
            fill(1, 1, 1)
            text(option, 'Futura', 10, 15, y + 8)

    def draw_battle_log(self):
        """Draw battle log"""
        fill(0.1, 0.1, 0.2, 0.8)
        rect(120, 10, 126, 50)

        fill(1, 1, 1)
        for i, message in enumerate(reversed(self.battle_log)):
            if i >= self.max_log_lines:
                break

            y = 54 - i * 10
            text(message, 'Futura', 8, 122, y)

    def draw_turn_indicator(self, actor):
        """Draw turn indicator"""
        actor_name = actor['id'] if actor['type'] == 'player' else actor['id']

        fill(0.9, 0.9, 0.2)
        text(f"Turn: {actor_name}", 'Futura', 10, 128, 200)

    def touch_began(self, touch, logical_x, logical_y):
        """Handle touch input"""
        # Handle menu selection
        if self.menu_state == 'main':
            # Check menu options
            options_count = 4 if not self.battle.can_flee else 5

            for i in range(options_count):
                y = 60 - i * 12

                if 12 <= logical_x <= 108 and y - 1 <= logical_y <= y + 10:
                    self.menu_selection = i
                    self.handle_menu_selection(i)
                    break

    def handle_menu_selection(self, index):
        """Handle battle menu selection"""
        options = ['attack', 'magic', 'item', 'defend', 'flee']

        if index >= len(options):
            return

        action = options[index]

        if action == 'attack':
            # Select target
            if self.battle.enemies:
                alive_enemies = [e for e in self.battle.enemies if e['hp'] > 0]
                if alive_enemies:
                    target = alive_enemies[0]  # For simplicity, attack first enemy
                    self.execute_player_action('attack', target)

        elif action == 'defend':
            self.execute_player_action('defend')

        elif action == 'flee':
            self.execute_player_action('flee')

        # TODO: Implement magic and item selection menus

    def touch_moved(self, touch, logical_x, logical_y):
        """Handle touch movement"""
        pass

    def touch_ended(self, touch, logical_x, logical_y):
        """Handle touch end"""
        pass
