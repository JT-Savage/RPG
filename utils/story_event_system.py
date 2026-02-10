"""
Story Event System
Handles story triggers, cutscenes, and major story moments
"""

class StoryEventSystem:
    """Manages story events and cutscenes"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.current_event = None
        self.event_queue = []

    def check_location_events(self, location):
        """
        Check for events triggered by entering location

        Args:
            location: Location identifier

        Returns:
            str: Event ID or None
        """
        from data.story_events import LOCATION_EVENTS

        location_events = LOCATION_EVENTS.get(location, [])

        for event_id in location_events:
            if self.can_trigger_event(event_id):
                return event_id

        return None

    def check_flag_events(self):
        """
        Check for events triggered by story flags

        Returns:
            str: Event ID or None
        """
        from data.story_events import FLAG_TRIGGERED_EVENTS

        for event_id, flag_data in FLAG_TRIGGERED_EVENTS.items():
            required_flags = flag_data.get('required_flags', [])
            trigger_flag = flag_data.get('trigger_flag')

            # Check if all required flags are set
            if not all(self.game_state.story_flags.get(flag) for flag in required_flags):
                continue

            # Check if trigger flag just became true
            if trigger_flag and self.game_state.story_flags.get(trigger_flag):
                # Check if event already seen
                if not self.game_state.story_flags.get(f'{event_id}_seen'):
                    return event_id

        return None

    def can_trigger_event(self, event_id):
        """
        Check if event can be triggered

        Args:
            event_id: Event identifier

        Returns:
            bool: Can trigger
        """
        from data.story_events import STORY_EVENTS

        event = STORY_EVENTS.get(event_id)
        if not event:
            return False

        # Check if already seen (for one-time events)
        if event.get('one_time', True):
            if self.game_state.story_flags.get(f'{event_id}_seen'):
                return False

        # Check required flags
        required_flags = event.get('required_flags', [])
        if not all(self.game_state.story_flags.get(flag) for flag in required_flags):
            return False

        # Check forbidden flags
        forbidden_flags = event.get('forbidden_flags', [])
        if any(self.game_state.story_flags.get(flag) for flag in forbidden_flags):
            return False

        # Check character requirements
        required_characters = event.get('required_characters', [])
        for char_id in required_characters:
            if char_id not in self.game_state.characters_recruited:
                return False

        return True

    def trigger_event(self, event_id):
        """
        Trigger story event

        Args:
            event_id: Event identifier

        Returns:
            dict: Event data
        """
        from data.story_events import STORY_EVENTS

        event = STORY_EVENTS.get(event_id)
        if not event:
            return None

        self.current_event = event_id

        # Mark as seen
        self.game_state.story_flags[f'{event_id}_seen'] = True

        # Apply event effects
        self.apply_event_effects(event)

        return event

    def apply_event_effects(self, event):
        """
        Apply event effects

        Args:
            event: Event data
        """
        effects = event.get('effects', {})

        # Set story flags
        if 'set_flags' in effects:
            for flag, value in effects['set_flags'].items():
                self.game_state.story_flags[flag] = value

        # Recruit characters
        if 'recruit_characters' in effects:
            for char_id in effects['recruit_characters']:
                self.game_state.recruit_character(char_id)

        # Force add to party
        if 'force_add_to_party' in effects:
            for char_id in effects['force_add_to_party']:
                if char_id not in self.game_state.active_party:
                    if len(self.game_state.active_party) < 4:
                        self.game_state.active_party.append(char_id)

        # Remove from party
        if 'remove_from_party' in effects:
            for char_id in effects['remove_from_party']:
                if char_id in self.game_state.active_party:
                    self.game_state.active_party.remove(char_id)
                if char_id in self.game_state.reserve_party:
                    self.game_state.reserve_party.remove(char_id)

        # Grant items
        if 'grant_items' in effects:
            for item_id, count in effects['grant_items'].items():
                self.game_state.add_item_to_inventory(item_id, count)

        # Grant key items
        if 'grant_key_items' in effects:
            for key_item_id in effects['grant_key_items']:
                self.game_state.add_key_item(key_item_id)

        # Grant Gil
        if 'grant_gil' in effects:
            self.game_state.gil += effects['grant_gil']

        # Grant EXP
        if 'grant_exp' in effects:
            from utils.level_up_system import distribute_battle_exp
            distribute_battle_exp(self.game_state, effects['grant_exp'])

        # Trigger battles
        if 'trigger_battle' in effects:
            # Would trigger battle scene
            pass

        # Teleport
        if 'teleport' in effects:
            self.game_state.current_location = effects['teleport']

        # Character death
        if 'kill_character' in effects:
            char_id = effects['kill_character']
            if char_id == 'flood':
                self.game_state.story_flags['flood_dead'] = True
                self.game_state.characters['flood']['hp'] = 0

        # Iris berserk
        if 'trigger_iris_berserk' in effects:
            self.game_state.trigger_iris_berserk()

        # Yipp alignment
        if 'set_yipp_alignment' in effects:
            alignment = effects['set_yipp_alignment']
            self.game_state.story_flags['yipp_alignment'] = alignment

            # Update class
            if alignment == 'necromancer':
                self.game_state.character_classes['yipp'] = 'necromancer'
            elif alignment == 'vampire':
                self.game_state.character_classes['yipp'] = 'vampire'
            elif alignment == 'druid':
                self.game_state.character_classes['yipp'] = 'druid'

        # Class evolution
        if 'evolve_class' in effects:
            for char_id, new_class in effects['evolve_class'].items():
                self.game_state.character_classes[char_id] = new_class

        # Unlock locations
        if 'unlock_locations' in effects:
            for location in effects['unlock_locations']:
                self.game_state.story_flags[f'{location}_unlocked'] = True

        # Start quests
        if 'start_quests' in effects:
            for quest_id in effects['start_quests']:
                if 'active_quests' not in self.game_state.__dict__:
                    self.game_state.active_quests = []
                self.game_state.active_quests.append(quest_id)

    def complete_event(self):
        """Complete current event"""
        if self.current_event:
            self.game_state.story_flags[f'{self.current_event}_completed'] = True
            self.current_event = None

    def get_current_event(self):
        """Get current event"""
        return self.current_event

    def is_event_active(self):
        """Check if event is active"""
        return self.current_event is not None

    # === Major Story Events ===

    def trigger_warren_escape(self):
        """Trigger warren escape sequence"""
        return self.trigger_event('warren_escape')

    def trigger_imperial_city_arrival(self):
        """Trigger Imperial City arrival"""
        return self.trigger_event('imperial_city_arrival')

    def trigger_fei_death(self):
        """Trigger Fei death and Iris berserk"""
        self.game_state.characters['fei']['hp'] = 0
        self.game_state.trigger_iris_berserk()
        return self.trigger_event('fei_death_iris_berserk')

    def trigger_flood_sacrifice(self):
        """Trigger Flood sacrifice scene"""
        return self.trigger_event('flood_sacrifice')

    def trigger_orisia_meeting(self):
        """Trigger Orisia meeting (recruitment deadline)"""
        return self.trigger_event('orisia_desert_warning')

    def trigger_yipp_alignment_choice(self):
        """Trigger Yipp alignment choice"""
        return self.trigger_event('yipp_alignment_choice')

    def trigger_kella_first_meeting(self):
        """Trigger first meeting with Queen Kella"""
        return self.trigger_event('kella_first_meeting')

    def trigger_kella_infected_encounter(self):
        """Trigger infected Kella secret boss"""
        return self.trigger_event('kella_infected')

    def trigger_final_boss(self):
        """Trigger final boss battle"""
        return self.trigger_event('final_boss_intro')

    def trigger_captain_donald_reveal(self):
        """Trigger Captain Donald post-credits boss"""
        return self.trigger_event('captain_donald_reveal')

    def trigger_game_ending(self):
        """Trigger game ending"""
        return self.trigger_event('game_ending')

    # === Class Evolution Events ===

    def check_class_evolution(self, char_id):
        """
        Check if character can evolve class

        Args:
            char_id: Character identifier

        Returns:
            dict: Evolution data or None
        """
        from data.characters import CLASS_EVOLUTIONS

        evolutions = CLASS_EVOLUTIONS.get(char_id, {})
        current_class = self.game_state.character_classes.get(char_id)

        evolution_data = evolutions.get(current_class)
        if not evolution_data:
            return None

        # Check level requirement
        char = self.game_state.characters.get(char_id)
        if not char:
            return None

        if char['level'] < evolution_data.get('level_requirement', 30):
            return None

        # Check if already evolved
        if self.game_state.story_flags.get(f'{char_id}_evolved'):
            return None

        return evolution_data

    def evolve_character_class(self, char_id, new_class):
        """
        Evolve character class

        Args:
            char_id: Character identifier
            new_class: New class name

        Returns:
            bool: Success
        """
        self.game_state.character_classes[char_id] = new_class
        self.game_state.story_flags[f'{char_id}_evolved'] = True

        # Trigger evolution event
        event_id = f'{char_id}_class_evolution'
        if self.can_trigger_event(event_id):
            self.trigger_event(event_id)

        return True

    # === Special Mechanics ===

    def trigger_iris_berserk_end(self):
        """End Iris berserk mode (Fei revived)"""
        if self.game_state.iris_berserk:
            self.game_state.iris_berserk = False
            return self.trigger_event('iris_berserk_end')

        return None

    def close_recruitment_window(self):
        """Close recruitment window (Orisia YES)"""
        self.game_state.close_recruitment()
        return self.trigger_event('recruitment_deadline_passed')

    def trigger_yipp_dungeon_encounter(self):
        """Trigger Yipp random dungeon encounter"""
        if self.game_state.story_flags.get('yipp_encountered'):
            return None

        if self.game_state.story_flags.get('met_orisia'):
            return None

        self.game_state.story_flags['yipp_encountered'] = True
        return self.trigger_event('yipp_dungeon_encounter')

    # === Quest Events ===

    def complete_quest(self, quest_id):
        """
        Complete quest

        Args:
            quest_id: Quest identifier

        Returns:
            dict: Quest completion rewards
        """
        from data.quests import QUESTS

        quest = QUESTS.get(quest_id)
        if not quest:
            return None

        # Mark as completed
        self.game_state.story_flags[f'{quest_id}_completed'] = True

        # Remove from active quests
        if hasattr(self.game_state, 'active_quests'):
            if quest_id in self.game_state.active_quests:
                self.game_state.active_quests.remove(quest_id)

        # Grant rewards
        rewards = quest.get('rewards', {})

        if 'gil' in rewards:
            self.game_state.gil += rewards['gil']

        if 'exp' in rewards:
            from utils.level_up_system import distribute_battle_exp
            distribute_battle_exp(self.game_state, rewards['exp'])

        if 'items' in rewards:
            for item_id, count in rewards['items'].items():
                self.game_state.add_item_to_inventory(item_id, count)

        if 'key_items' in rewards:
            for key_item_id in rewards['key_items']:
                self.game_state.add_key_item(key_item_id)

        # Trigger completion event
        completion_event = quest.get('completion_event')
        if completion_event:
            self.trigger_event(completion_event)

        return rewards

    def check_tutorial_progress(self):
        """Check tutorial progression"""
        tutorial_flags = [
            'tutorial_movement',
            'tutorial_battle',
            'tutorial_menu',
            'tutorial_recruitment'
        ]

        completed = sum(1 for flag in tutorial_flags if self.game_state.story_flags.get(flag))

        if completed == len(tutorial_flags):
            self.game_state.story_flags['tutorial_completed'] = True
            return True

        return False
