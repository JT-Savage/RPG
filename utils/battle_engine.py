"""
Battle Engine - Turn-based combat system
Handles combat flow, turn order, actions, and battle state
"""

import random
from data.enemies import get_enemy_stats
from data.spells import calculate_spell_damage, calculate_spell_healing
from utils.status_effects import apply_status_effect, process_status_effects, has_status

class BattleEngine:
    """Manages turn-based combat"""

    def __init__(self, game_state, enemy_ids, can_flee=True):
        """
        Initialize battle

        Args:
            game_state: GameState instance
            enemy_ids: List of enemy IDs to fight
            can_flee: Whether player can flee (False for bosses)
        """
        self.game_state = game_state
        self.can_flee = can_flee
        self.battle_over = False
        self.victory = False
        self.fled = False

        # Initialize party
        self.party = []
        for char_id in game_state.active_party:
            char_data = game_state.characters[char_id]
            if char_data['hp'] > 0:  # Only alive characters
                self.party.append({
                    'id': char_id,
                    'type': 'player',
                    'data': char_data,
                    'speed': char_data['stats']['speed'],
                    'turn_ready': False,
                    'atb_gauge': 0  # For ATB system (if implemented)
                })

        # Initialize enemies
        self.enemies = []
        for i, enemy_id in enumerate(enemy_ids):
            enemy_stats = get_enemy_stats(enemy_id)
            if enemy_stats:
                self.enemies.append({
                    'id': enemy_id,
                    'index': i,
                    'type': 'enemy',
                    'hp': enemy_stats['hp'],
                    'mp': enemy_stats['mp'],
                    'max_hp': enemy_stats['hp'],
                    'max_mp': enemy_stats['mp'],
                    'stats': {
                        'attack': enemy_stats['attack'],
                        'defense': enemy_stats['defense'],
                        'magic_power': enemy_stats['magic_power'],
                        'spell_resistance': enemy_stats['spell_resistance'],
                        'speed': enemy_stats['speed']
                    },
                    'level': enemy_stats['level'],
                    'abilities': enemy_stats.get('abilities', []),
                    'resistances': enemy_stats.get('resistances', {}),
                    'weaknesses': enemy_stats.get('weaknesses', {}),
                    'status_effects': [],
                    'speed': enemy_stats['speed'],
                    'turn_ready': False,
                    'atb_gauge': 0
                })

        # Battle state
        self.turn_order = []
        self.current_turn_index = 0
        self.round_number = 1

        # Special mechanics tracking
        self.burn_spread_queue = []  # Enemies with Burn to potentially spread
        self.javin_attack_counter = {}  # For Baby Dragon every 4th attack

        # Initialize turn order
        self.calculate_turn_order()

    def calculate_turn_order(self):
        """Calculate turn order based on speed"""
        # Combine all combatants
        all_combatants = self.party + self.enemies

        # Sort by speed (highest first)
        self.turn_order = sorted(all_combatants, key=lambda x: x['speed'], reverse=True)

        # Add some randomness for same-speed characters
        for i in range(len(self.turn_order) - 1):
            if self.turn_order[i]['speed'] == self.turn_order[i + 1]['speed']:
                if random.random() < 0.5:
                    self.turn_order[i], self.turn_order[i + 1] = self.turn_order[i + 1], self.turn_order[i]

        self.current_turn_index = 0

    def get_current_actor(self):
        """Get the current actor whose turn it is"""
        if not self.turn_order:
            return None

        return self.turn_order[self.current_turn_index]

    def next_turn(self):
        """Advance to next turn"""
        self.current_turn_index += 1

        if self.current_turn_index >= len(self.turn_order):
            # New round
            self.current_turn_index = 0
            self.round_number += 1

            # Process status effects at end of round
            self.process_all_status_effects()

            # Check for Burn spread
            self.process_burn_spread()

        # Skip dead/incapacitated characters
        while self.current_turn_index < len(self.turn_order):
            actor = self.turn_order[self.current_turn_index]

            if actor['type'] == 'player':
                if actor['data']['hp'] <= 0:
                    self.current_turn_index += 1
                    continue
            else:  # enemy
                if actor['hp'] <= 0:
                    self.current_turn_index += 1
                    continue

            # Check if controlled (not berserk for player)
            if actor['type'] == 'player':
                # Check Iris berserk
                if actor['id'] == 'iris' and self.game_state.iris_berserk:
                    # Iris is berserk - AI controlled
                    return self.execute_iris_berserk_turn(actor)

            break

        # Check battle end conditions
        self.check_battle_end()

    def process_all_status_effects(self):
        """Process status effects for all combatants"""
        from utils.status_effects import process_status_effects

        # Process party
        for member in self.party:
            if member['data']['hp'] > 0:
                process_status_effects(member['data'])

        # Process enemies
        for enemy in self.enemies:
            if enemy['hp'] > 0:
                process_status_effects(enemy)

    def process_burn_spread(self):
        """Process Burn status spreading (15% chance to adjacent enemies)"""
        from utils.status_effects import has_status, apply_status_effect

        for enemy in self.enemies:
            if enemy['hp'] <= 0:
                continue

            if has_status(enemy, 'burn'):
                # 15% chance to spread to adjacent enemies
                if random.random() < 0.15:
                    # Find adjacent enemies (adjacent indices)
                    enemy_index = enemy['index']

                    adjacent_indices = []
                    if enemy_index > 0:
                        adjacent_indices.append(enemy_index - 1)
                    if enemy_index < len(self.enemies) - 1:
                        adjacent_indices.append(enemy_index + 1)

                    # Spread to one random adjacent enemy
                    if adjacent_indices:
                        target_index = random.choice(adjacent_indices)
                        target_enemy = self.enemies[target_index]

                        if target_enemy['hp'] > 0 and not has_status(target_enemy, 'burn'):
                            apply_status_effect(target_enemy, 'burn', duration=3)
                            print(f"Burn spread to {target_enemy['id']}!")

    def execute_iris_berserk_turn(self, iris):
        """
        Execute Iris's turn while berserk

        Args:
            iris: Iris actor dict

        Returns:
            Action result
        """
        # Find who killed Fei
        fei_killer = None
        for enemy in self.enemies:
            if enemy['hp'] > 0:
                # Assume first living enemy (would need tracking in real implementation)
                fei_killer = enemy
                break

        if not fei_killer:
            # No enemies left, attack random
            fei_killer = random.choice([e for e in self.enemies if e['hp'] > 0])

        # Check if Shapeshifter
        iris_class = self.game_state.character_classes.get('iris', 'nature_bound_druid')

        if iris_class == 'shapeshifter':
            # Panda form: 3 attacks (2 claws + 1 bite)
            result = {
                'actor': iris,
                'action': 'berserk_panda_attack',
                'target': fei_killer,
                'attacks': []
            }

            # Claw 1
            damage1 = self.calculate_physical_damage(iris, fei_killer, bonus_multiplier=1.5)
            fei_killer['hp'] -= damage1
            result['attacks'].append({'type': 'claw', 'damage': damage1})

            # Claw 2
            damage2 = self.calculate_physical_damage(iris, fei_killer, bonus_multiplier=1.5)
            fei_killer['hp'] -= damage2
            result['attacks'].append({'type': 'claw', 'damage': damage2})

            # Bite
            damage3 = self.calculate_physical_damage(iris, fei_killer, bonus_multiplier=1.5)
            fei_killer['hp'] -= damage3
            result['attacks'].append({'type': 'bite', 'damage': damage3})

            return result
        else:
            # Nature Bound Druid: Random ability
            # For simplicity, just attack
            result = self.execute_attack(iris, fei_killer)
            result['berserk'] = True
            return result

    def execute_attack(self, attacker, target):
        """
        Execute physical attack

        Args:
            attacker: Attacker dict
            target: Target dict

        Returns:
            Action result dict
        """
        damage = self.calculate_physical_damage(attacker, target)

        # Apply damage
        if target['type'] == 'player':
            target['data']['hp'] -= damage
            target['data']['hp'] = max(0, target['data']['hp'])

            # Check if Fei died (trigger Iris berserk)
            if target['id'] == 'fei' and target['data']['hp'] <= 0:
                self.game_state.trigger_iris_berserk()

        else:  # enemy
            target['hp'] -= damage
            target['hp'] = max(0, target['hp'])

        # Check for critical hit
        crit = random.random() < 0.05  # 5% base crit chance

        # Javin baby dragon counter
        if attacker['type'] == 'player' and attacker['id'] == 'javin':
            self.increment_javin_attack_counter()

        result = {
            'actor': attacker,
            'action': 'attack',
            'target': target,
            'damage': damage,
            'critical': crit
        }

        return result

    def calculate_physical_damage(self, attacker, target, bonus_multiplier=1.0):
        """
        Calculate physical damage

        Args:
            attacker: Attacker dict
            target: Target dict
            bonus_multiplier: Damage multiplier

        Returns:
            int: Damage amount
        """
        if attacker['type'] == 'player':
            attack = attacker['data']['stats']['attack']
        else:
            attack = attacker['stats']['attack']

        if target['type'] == 'player':
            defense = target['data']['stats']['defense']
        else:
            defense = target['stats']['defense']

        # Basic damage formula (FF-style)
        base_damage = attack * 2 - defense
        base_damage = max(1, base_damage)  # Minimum 1 damage

        # Add randomness (±10%)
        variance = random.uniform(0.9, 1.1)
        damage = int(base_damage * variance * bonus_multiplier)

        return max(1, damage)

    def execute_magic(self, caster, spell_id, targets):
        """
        Execute magic spell

        Args:
            caster: Caster dict
            spell_id: Spell identifier
            targets: List of target dicts

        Returns:
            Action result dict
        """
        from data.spells import SPELLS

        spell = SPELLS.get(spell_id)
        if not spell:
            return None

        # Check MP cost
        mp_cost = spell['level']

        if caster['type'] == 'player':
            if caster['data']['mp'] < mp_cost:
                return {'error': 'Not enough MP'}

            caster['data']['mp'] -= mp_cost
        else:
            if caster['mp'] < mp_cost:
                return {'error': 'Not enough MP'}

            caster['mp'] -= mp_cost

        result = {
            'actor': caster,
            'action': 'magic',
            'spell': spell_id,
            'targets': [],
            'mp_cost': mp_cost
        }

        # Get caster magic power
        if caster['type'] == 'player':
            magic_power = caster['data']['stats']['magic_power']
        else:
            magic_power = caster['stats']['magic_power']

        # Apply spell effects
        for target in targets:
            target_result = {'target': target}

            # Damage spell
            if 'base_damage' in spell:
                # Get target spell resistance
                if target['type'] == 'player':
                    spell_resistance = target['data']['stats']['spell_resistance']
                else:
                    spell_resistance = target['stats']['spell_resistance']

                # Psychic damage cannot be resisted
                if spell.get('descriptor') == 'psychic':
                    spell_resistance = 0

                damage = calculate_spell_damage(spell_id, magic_power, spell_resistance)

                # Apply damage
                if target['type'] == 'player':
                    target['data']['hp'] -= damage
                    target['data']['hp'] = max(0, target['data']['hp'])
                else:
                    target['hp'] -= damage
                    target['hp'] = max(0, target['hp'])

                target_result['damage'] = damage

                # Check for Burn status (Arsonist)
                if spell.get('element') == 'fire':
                    caster_class = self.game_state.character_classes.get(caster['id'], '')
                    if caster_class == 'arsonist':
                        from utils.status_effects import apply_status_effect
                        apply_status_effect(target, 'burn', duration=3)
                        target_result['burn_applied'] = True

            # Healing spell
            elif 'base_healing' in spell:
                healing = calculate_spell_healing(spell_id, magic_power)

                if target['type'] == 'player':
                    target['data']['hp'] += healing
                    target['data']['hp'] = min(target['data']['hp'], target['data']['max_hp'])
                else:
                    target['hp'] += healing
                    target['hp'] = min(target['hp'], target['max_hp'])

                target_result['healing'] = healing

            # Status effect spell
            if 'status_effect' in spell:
                from utils.status_effects import apply_status_effect
                status = spell['status_effect']
                duration = spell.get('duration', 3)

                if isinstance(status, list):
                    for s in status:
                        apply_status_effect(target, s, duration)
                else:
                    apply_status_effect(target, status, duration)

                target_result['status_applied'] = status

            result['targets'].append(target_result)

        return result

    def execute_item(self, user, item_id, target):
        """
        Use item in battle

        Args:
            user: User dict
            item_id: Item identifier
            target: Target dict

        Returns:
            Action result dict
        """
        from data.items import ITEMS

        item = ITEMS.get(item_id)
        if not item:
            return None

        # Check if have item
        if not self.game_state.remove_item_from_inventory(item_id, 1):
            return {'error': 'No items'}

        result = {
            'actor': user,
            'action': 'item',
            'item': item_id,
            'target': target
        }

        # Apply item effects
        effect = item.get('effect', {})

        # HP restore
        if 'hp_restore' in effect:
            if effect['hp_restore'] == 'full':
                healing = target['data']['max_hp'] - target['data']['hp']
                target['data']['hp'] = target['data']['max_hp']
            else:
                healing = effect['hp_restore']
                target['data']['hp'] += healing
                target['data']['hp'] = min(target['data']['hp'], target['data']['max_hp'])

            result['healing'] = healing

        # MP restore
        if 'mp_restore' in effect:
            if effect['mp_restore'] == 'full':
                mp_restored = target['data']['max_mp'] - target['data']['mp']
                target['data']['mp'] = target['data']['max_mp']
            else:
                mp_restored = effect['mp_restore']
                target['data']['mp'] += mp_restored
                target['data']['mp'] = min(target['data']['mp'], target['data']['max_mp'])

            result['mp_restored'] = mp_restored

        # Status cure
        if 'removes_status' in effect:
            from utils.status_effects import remove_status_effect
            status_to_remove = effect['removes_status']

            if status_to_remove == 'all':
                target['data']['status_effects'] = []
            else:
                remove_status_effect(target['data'], status_to_remove)

            result['status_removed'] = status_to_remove

        # Revival
        if effect.get('revive'):
            if target['data']['hp'] <= 0:
                hp_restore = int(target['data']['max_hp'] * effect.get('hp_restore_percent', 0.5))
                target['data']['hp'] = hp_restore
                result['revived'] = True

        return result

    def execute_defend(self, defender):
        """
        Execute defend action (reduces damage until next turn)

        Args:
            defender: Defender dict

        Returns:
            Action result dict
        """
        from utils.status_effects import apply_status_effect

        # Apply Defend status (reduces damage by 50%)
        if defender['type'] == 'player':
            apply_status_effect(defender['data'], 'defend', duration=1)
        else:
            apply_status_effect(defender, 'defend', duration=1)

        return {
            'actor': defender,
            'action': 'defend'
        }

    def attempt_flee(self):
        """
        Attempt to flee from battle

        Returns:
            bool: Success
        """
        if not self.can_flee:
            return False

        # 50% base flee chance, higher if party is faster
        party_speed = sum(m['speed'] for m in self.party) / len(self.party)
        enemy_speed = sum(e['speed'] for e in self.enemies if e['hp'] > 0) / len([e for e in self.enemies if e['hp'] > 0])

        flee_chance = 0.5
        if party_speed > enemy_speed:
            flee_chance += 0.2

        if random.random() < flee_chance:
            self.fled = True
            self.battle_over = True
            return True

        return False

    def increment_javin_attack_counter(self):
        """Increment Javin's attack counter for Baby Dragon"""
        if 'javin' not in self.javin_attack_counter:
            self.javin_attack_counter['javin'] = 0

        self.javin_attack_counter['javin'] += 1

        # Check if 4th attack
        if self.javin_attack_counter['javin'] >= 4:
            # Reset counter
            self.javin_attack_counter['javin'] = 0

            # Trigger Baby Dragon attack (if equipped)
            if self.game_state.has_key_item('baby_dragon'):
                # Baby Dragon attacks (Level 2 fire spell)
                return True

        return False

    def check_battle_end(self):
        """Check if battle has ended"""
        # Check if all enemies dead
        alive_enemies = [e for e in self.enemies if e['hp'] > 0]
        if not alive_enemies:
            self.battle_over = True
            self.victory = True
            return

        # Check if all party dead
        alive_party = [p for p in self.party if p['data']['hp'] > 0]
        if not alive_party:
            self.battle_over = True
            self.victory = False
            return

    def get_battle_rewards(self):
        """
        Calculate battle rewards (EXP and Gil)

        Returns:
            dict: Rewards (exp, gil)
        """
        if not self.victory:
            return {'exp': 0, 'gil': 0}

        total_exp = 0
        total_gil = 0

        for enemy in self.enemies:
            enemy_stats = get_enemy_stats(enemy['id'])
            if enemy_stats:
                total_exp += enemy_stats.get('exp_reward', 0)
                total_gil += enemy_stats.get('gil_reward', 0)

        return {
            'exp': total_exp,
            'gil': total_gil
        }

    def ai_select_action(self, enemy):
        """
        AI selects action for enemy

        Args:
            enemy: Enemy dict

        Returns:
            Action dict
        """
        # Simple AI: Random action from abilities
        abilities = enemy.get('abilities', [])

        if not abilities:
            # Default attack
            target = random.choice([p for p in self.party if p['data']['hp'] > 0])
            return {
                'action': 'attack',
                'target': target
            }

        # Choose random ability
        ability = random.choice(abilities)

        # Determine target
        if 'heal' in ability or 'buff' in ability:
            # Target self or ally
            target = enemy
        else:
            # Target random alive party member
            alive_party = [p for p in self.party if p['data']['hp'] > 0]
            target = random.choice(alive_party) if alive_party else None

        return {
            'action': 'ability',
            'ability': ability,
            'target': target
        }
