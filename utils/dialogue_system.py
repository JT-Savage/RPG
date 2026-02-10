"""
Dialogue System
Handles NPC conversations, story dialogue, and player choices
"""

class DialogueSystem:
    """Manages dialogue trees and conversations"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.current_dialogue = None
        self.current_node_index = 0
        self.dialogue_history = []

    def start_dialogue(self, dialogue_id):
        """
        Start a dialogue sequence

        Args:
            dialogue_id: Dialogue identifier

        Returns:
            dict: Initial dialogue node
        """
        from data.dialogues import DIALOGUES

        dialogue = DIALOGUES.get(dialogue_id)
        if not dialogue:
            return None

        self.current_dialogue = dialogue
        self.current_node_index = 0
        self.dialogue_history = [dialogue_id]

        return self.get_current_node()

    def get_current_node(self):
        """
        Get current dialogue node

        Returns:
            dict: Current node
        """
        if not self.current_dialogue:
            return None

        nodes = self.current_dialogue.get('nodes', [])
        if self.current_node_index >= len(nodes):
            return None

        return nodes[self.current_node_index]

    def advance_dialogue(self):
        """
        Advance to next dialogue node

        Returns:
            dict: Next node or None if dialogue ended
        """
        if not self.current_dialogue:
            return None

        self.current_node_index += 1

        node = self.get_current_node()

        if node is None:
            # Dialogue ended
            self.end_dialogue()

        return node

    def select_choice(self, choice_index):
        """
        Select dialogue choice

        Args:
            choice_index: Choice index

        Returns:
            dict: Next node
        """
        node = self.get_current_node()
        if not node:
            return None

        choices = node.get('choices')
        if not choices or choice_index >= len(choices):
            return None

        choice = choices[choice_index]

        # Apply choice effects
        if 'effects' in choice:
            self.apply_effects(choice['effects'])

        # Jump to next node
        if 'next_node' in choice:
            self.current_node_index = choice['next_node']
        elif 'next_dialogue' in choice:
            # Jump to different dialogue
            return self.start_dialogue(choice['next_dialogue'])
        else:
            # End dialogue
            self.end_dialogue()
            return None

        return self.get_current_node()

    def apply_effects(self, effects):
        """
        Apply dialogue choice effects

        Args:
            effects: Effects dict
        """
        # Story flags
        if 'set_flag' in effects:
            flag = effects['set_flag']
            value = effects.get('value', True)
            self.game_state.story_flags[flag] = value

        # Gil changes
        if 'give_gil' in effects:
            self.game_state.gil += effects['give_gil']
        elif 'take_gil' in effects:
            self.game_state.gil -= effects['take_gil']

        # Items
        if 'give_item' in effects:
            item_id = effects['give_item']
            count = effects.get('count', 1)
            self.game_state.add_item_to_inventory(item_id, count)

        if 'take_item' in effects:
            item_id = effects['take_item']
            count = effects.get('count', 1)
            self.game_state.remove_item_from_inventory(item_id, count)

        # Key items
        if 'give_key_item' in effects:
            self.game_state.add_key_item(effects['give_key_item'])

        # Recruitment
        if 'recruit_character' in effects:
            self.game_state.recruit_character(effects['recruit_character'])

        # Party changes
        if 'add_to_party' in effects:
            char_id = effects['add_to_party']
            if char_id not in self.game_state.active_party and len(self.game_state.active_party) < 4:
                self.game_state.active_party.append(char_id)

        if 'remove_from_party' in effects:
            char_id = effects['remove_from_party']
            if char_id in self.game_state.active_party:
                self.game_state.active_party.remove(char_id)

        # Character alignment (Yipp)
        if 'set_alignment' in effects:
            char_id = effects.get('character')
            alignment = effects['set_alignment']
            if char_id == 'yipp':
                self.game_state.story_flags['yipp_alignment'] = alignment
                # Rebuild character class
                if alignment == 'necromancer':
                    self.game_state.character_classes['yipp'] = 'necromancer'
                elif alignment == 'vampire':
                    self.game_state.character_classes['yipp'] = 'vampire'
                elif alignment == 'druid':
                    self.game_state.character_classes['yipp'] = 'druid'

        # Iris berserk trigger
        if 'trigger_iris_berserk' in effects:
            self.game_state.trigger_iris_berserk()

        # Character death (Flood)
        if 'kill_character' in effects:
            char_id = effects['kill_character']
            if char_id == 'flood':
                self.game_state.story_flags['flood_dead'] = True
                self.game_state.characters['flood']['hp'] = 0

        # Start battle
        if 'start_battle' in effects:
            # Would trigger battle scene
            pass

        # Teleport
        if 'teleport' in effects:
            self.game_state.current_location = effects['teleport']

    def end_dialogue(self):
        """End current dialogue"""
        # Check for dialogue completion effects
        if self.current_dialogue:
            completion_effects = self.current_dialogue.get('completion_effects')
            if completion_effects:
                self.apply_effects(completion_effects)

        self.current_dialogue = None
        self.current_node_index = 0

    def is_dialogue_active(self):
        """Check if dialogue is active"""
        return self.current_dialogue is not None

    def get_speaker_name(self, node):
        """
        Get speaker name from node

        Args:
            node: Dialogue node

        Returns:
            str: Speaker name
        """
        speaker = node.get('speaker')
        if not speaker:
            return None

        # Handle character IDs
        if speaker in self.game_state.characters:
            return speaker.title()

        return speaker

    def check_dialogue_conditions(self, dialogue_id):
        """
        Check if dialogue can be started (conditions met)

        Args:
            dialogue_id: Dialogue identifier

        Returns:
            bool: Can start
        """
        from data.dialogues import DIALOGUES

        dialogue = DIALOGUES.get(dialogue_id)
        if not dialogue:
            return False

        conditions = dialogue.get('conditions', {})

        # Check required flags
        if 'required_flags' in conditions:
            for flag in conditions['required_flags']:
                if not self.game_state.story_flags.get(flag):
                    return False

        # Check forbidden flags
        if 'forbidden_flags' in conditions:
            for flag in conditions['forbidden_flags']:
                if self.game_state.story_flags.get(flag):
                    return False

        # Check character in party
        if 'character_in_party' in conditions:
            char_id = conditions['character_in_party']
            if char_id not in self.game_state.active_party and char_id not in self.game_state.reserve_party:
                return False

        # Check character not in party
        if 'character_not_in_party' in conditions:
            char_id = conditions['character_not_in_party']
            if char_id in self.game_state.active_party or char_id in self.game_state.reserve_party:
                return False

        # Check item
        if 'has_item' in conditions:
            item_id = conditions['has_item']
            count = conditions.get('item_count', 1)
            if not self.game_state.has_item_in_inventory(item_id, count):
                return False

        # Check key item
        if 'has_key_item' in conditions:
            if not self.game_state.has_key_item(conditions['has_key_item']):
                return False

        # Check Gil
        if 'min_gil' in conditions:
            if self.game_state.gil < conditions['min_gil']:
                return False

        return True

    def format_dialogue_text(self, text):
        """
        Format dialogue text with variable substitution

        Args:
            text: Raw text

        Returns:
            str: Formatted text
        """
        # Replace variables
        replacements = {
            '{player_gil}': str(self.game_state.gil),
            '{party_size}': str(len(self.game_state.active_party)),
            '{frostbite}': 'Frostbite' if 'frostbite' in self.game_state.characters_recruited else 'your ally',
            '{fei}': 'Fei' if 'fei' in self.game_state.characters_recruited else 'your ally'
        }

        for key, value in replacements.items():
            text = text.replace(key, value)

        return text


class DialogueNode:
    """Dialogue node data structure"""

    def __init__(self, speaker, text, choices=None, next_node=None):
        """
        Initialize dialogue node

        Args:
            speaker: Speaker name/ID
            text: Dialogue text
            choices: List of choice dicts (text, next_node, effects)
            next_node: Auto-advance to next node (if no choices)
        """
        self.speaker = speaker
        self.text = text
        self.choices = choices or []
        self.next_node = next_node

    def to_dict(self):
        """Convert to dict"""
        return {
            'speaker': self.speaker,
            'text': self.text,
            'choices': self.choices,
            'next_node': self.next_node
        }


def create_simple_dialogue(speaker, lines):
    """
    Create simple linear dialogue (no choices)

    Args:
        speaker: Speaker name
        lines: List of text lines

    Returns:
        dict: Dialogue data
    """
    nodes = []

    for i, line in enumerate(lines):
        node = {
            'speaker': speaker,
            'text': line
        }

        # Auto-advance to next, except last
        if i < len(lines) - 1:
            node['next_node'] = i + 1

        nodes.append(node)

    return {
        'nodes': nodes
    }


def create_choice_dialogue(speaker, question, choices):
    """
    Create dialogue with player choice

    Args:
        speaker: Speaker name
        question: Question text
        choices: List of (text, effects) tuples

    Returns:
        dict: Dialogue data
    """
    choice_list = []

    for text, effects in choices:
        choice_list.append({
            'text': text,
            'effects': effects
        })

    return {
        'nodes': [
            {
                'speaker': speaker,
                'text': question,
                'choices': choice_list
            }
        ]
    }


def create_recruitment_dialogue(char_id, greeting, question, accept_text, decline_text):
    """
    Create recruitment dialogue with loop

    Args:
        char_id: Character identifier
        greeting: Greeting text
        question: Recruitment question
        accept_text: Accept response
        decline_text: Decline response (loops back)

    Returns:
        dict: Dialogue data
    """
    return {
        'nodes': [
            # Node 0: Greeting
            {
                'speaker': char_id,
                'text': greeting,
                'next_node': 1
            },
            # Node 1: Question (loops back on NO)
            {
                'speaker': char_id,
                'text': question,
                'choices': [
                    {
                        'text': 'Yes',
                        'effects': {
                            'recruit_character': char_id,
                            'set_flag': f'{char_id}_recruited'
                        },
                        'next_node': 2
                    },
                    {
                        'text': 'No',
                        'next_node': 3
                    }
                ]
            },
            # Node 2: Accept
            {
                'speaker': char_id,
                'text': accept_text
            },
            # Node 3: Decline (loops back to question)
            {
                'speaker': char_id,
                'text': decline_text,
                'next_node': 1  # Loop back to question
            }
        ]
    }
