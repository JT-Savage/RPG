extends Node
## StoryEventSystem - Triggers cutscenes, story events, ending checks

signal story_event_triggered(event_id: String)
signal ending_determined(ending_type: String)
signal flood_death_started
signal hannah_scream_triggered
signal fungal_enemies_removed

# ===== MAIN STORY TRIGGERS =====

func check_location_triggers(location_id: String) -> void:
	match location_id:
		"tutorial_warren":
			_check_tutorial_triggers()
		"surface_forest":
			_check_surface_triggers()
		"imperial_city":
			_check_imperial_city_triggers()
		"kobold_warren_beneath_city":
			_check_underground_warren_triggers()
		"imperial_city_inn":
			_check_inn_triggers()
		"army_camp":
			_check_army_camp_triggers()
		"second_dragon_dungeon":
			_check_second_dragon_triggers()
		"necromancer_sanctum":
			_check_final_battle_triggers()

func _check_tutorial_triggers() -> void:
	# NG+: baby dragon comment if not obtained last run
	RecruitmentSystem.check_ng_plus_baby_dragon_comment()

func _check_surface_triggers() -> void:
	if not FlagManager.is_flag("met_frostbite"):
		_trigger_frostbite_encounter()

func _trigger_frostbite_encounter() -> void:
	# Frostbite encounter is mandatory (lycanthrope battle)
	FlagManager.set_flag("met_frostbite", true)
	story_event_triggered.emit("frostbite_encounter")

func _check_imperial_city_triggers() -> void:
	FlagManager.set_flag("imperial_city_visited", true)

	# Check if Fritzzit/Crankpot should appear at inn
	if (FlagManager.is_flag("kobolds_released") and
		not FlagManager.is_flag("army_blocks_return") and
		not FlagManager.is_flag("fritzzit_recruited")):
		FlagManager.set_flag("fritzzit_crankpot_available", true)

func _check_underground_warren_triggers() -> void:
	if not FlagManager.is_flag("kobolds_released"):
		_trigger_kobold_release()

func _trigger_kobold_release() -> void:
	FlagManager.set_flag("kobolds_released", true)
	FlagManager.set_flag("imperial_warren_escape", true)
	story_event_triggered.emit("kobolds_released")
	# Change battle music to kobold-heavy variant
	AudioManager.play_music("battle_kobold_heavy")

func _check_inn_triggers() -> void:
	# Fei grooming cutscene (after Cookie/Iris meet/join)
	if (not FlagManager.is_flag("fei_grooming_cutscene_triggered") and
		FlagManager.is_flag("cookie_iris_rescued") and
		FlagManager.is_flag("fei_recruited")):
		_trigger_fei_grooming_cutscene()

func _trigger_fei_grooming_cutscene() -> void:
	FlagManager.set_flag("fei_grooming_cutscene_triggered", true)
	DialogueManager.start_dialogue("fei_grooming")
	await DialogueManager.dialogue_ended
	# Panda fur is now lootable
	FlagManager.set_flag("panda_fur_available", true)
	story_event_triggered.emit("fei_grooming_complete")

func _check_army_camp_triggers() -> void:
	if not FlagManager.is_flag("orisia_met"):
		_trigger_orisia_meeting()

func _trigger_orisia_meeting() -> void:
	FlagManager.set_flag("orisia_met", true)
	DialogueManager.start_dialogue("orisia_meeting")
	await DialogueManager.dialogue_ended
	story_event_triggered.emit("orisia_meeting_complete")

func _check_second_dragon_triggers() -> void:
	if (FlagManager.is_flag("second_dragon_defeated") and
		not FlagManager.is_flag("flood_death_cutscene") and
		FlagManager.is_flag("flood_recruited")):
		_trigger_flood_death()

func _trigger_flood_death() -> void:
	FlagManager.set_flag("flood_death_cutscene", true)
	flood_death_started.emit()
	AudioManager.play_music("sad_theme", 0.5)
	DialogueManager.start_dialogue("flood_death_cutscene")
	await DialogueManager.dialogue_ended

	# Hannah scream effect
	FlagManager.set_flag("hannah_scream_triggered", true)
	hannah_scream_triggered.emit()
	AudioManager.play_hannah_scream()
	SceneTransition.flash(Color.WHITE, 1.0)
	await get_tree().create_timer(3.0).timeout

	# Flood permanently dies
	FlagManager.set_flag("flood_dead", true)
	PartyManager.flood_permanent_death()
	story_event_triggered.emit("flood_death")

func _check_final_battle_triggers() -> void:
	pass  # Handled by battle scene

# ===== JEROD HOUSE EXPLOSION =====

func trigger_jerod_explosion() -> void:
	FlagManager.set_flag("jerod_boss_defeated", true)
	FlagManager.set_flag("jerod_house_explosion", true)
	FlagManager.set_flag("fungal_enemies_removed", true)
	fungal_enemies_removed.emit()
	story_event_triggered.emit("jerod_explosion")
	# Screen shake + flash
	SceneTransition.flash(Color(1.0, 0.6, 0.0), 0.5)

# ===== ORISIA DEADLINE =====

func trigger_orisia_ready() -> void:
	RecruitmentSystem.trigger_deadline()
	FlagManager.set_flag("desert_entered", true)
	FlagManager.set_flag("army_blocks_return", true)
	AudioManager.play_music("desert")
	story_event_triggered.emit("deadline_passed")

# ===== YIPP SIDEQUEST RESOLUTION =====

func resolve_yipp_alignment(choice: String) -> void:
	# choice = "saint" or "vampire"
	FlagManager.set_flag("yipp_alignment", choice)
	if choice == "saint" or choice == "vampire":
		PartyManager.evolve_character("yipp")
	story_event_triggered.emit("yipp_alignment_chosen")

# ===== CLASS EVOLUTION (Orisia sidequests) =====

func complete_orisia_sidequest(char_id: String) -> void:
	if not FlagManager.can_do_orisia_sidequest(char_id):
		return

	PartyManager.evolve_character(char_id)

	# Grant level cap increase and special rewards
	match char_id:
		"frostbite":
			FlagManager.set_flag("frostbite_ultimate_weapon", true)
			# Grant Ultimate Shotgun to inventory
			GameManager.equipment.get_or_add("frostbite", {})["weapon"] = "ultimate_shotgun"
		"fritzzit":
			FlagManager.set_flag("fritzzit_ultimate_weapon", true)
			GameManager.equipment.get_or_add("fritzzit", {})["weapon"] = "ultimate_sniper_rifle"

	story_event_triggered.emit("orisia_sidequest_complete_" + char_id)
	_check_all_orisia_complete()

func _check_all_orisia_complete() -> void:
	var all_chars := ["javin","frostbite","fei","hannah","michael","warghoul",
					  "cookie","iris","fritzzit","crankpot","yipp"]
	for char_id in all_chars:
		if not FlagManager.is_flag(char_id + "_recruited"):
			continue
		# Skip Flood (no sidequest by design)
		if char_id == "flood":
			continue
		if not PartyManager.get_character(char_id).get("has_evolved", false):
			# Yipp exception: necromancer with no key items is still "complete" if no items found
			if char_id != "yipp":
				return

	FlagManager.set_flag("all_orisia_sidequests_complete", true)

# ===== ENDING DETERMINATION =====

func determine_ending() -> String:
	var cure_found := FlagManager.is_flag("cure_found")
	var yipp_alignment: String = FlagManager.get_flag("yipp_alignment")
	var all_recruited := _check_all_optional_recruited()

	var ending_type := ""

	if not cure_found:
		ending_type = "bad"
	elif yipp_alignment == "vampire":
		# Vampire Yipp forces bad ending (betrayal locks good/best)
		ending_type = "bad"
	elif cure_found and all_recruited:
		ending_type = "good"
	else:
		ending_type = "normal"

	FlagManager.set_flag("ending_type", ending_type)
	ending_determined.emit(ending_type)

	# Unlock best ending if good + Yipp saint
	if ending_type == "good" and yipp_alignment == "saint":
		FlagManager.set_flag("post_credits_unlocked", true)

	return ending_type

func _check_all_optional_recruited() -> bool:
	for char_id in RecruitmentSystem.OPTIONAL_CHARACTERS:
		if not FlagManager.is_flag(char_id + "_recruited"):
			return false
	return true

func get_lost_character_zombie_formations() -> Array:
	var lost := FlagManager.get_flag("lost_characters")
	var formations := []
	for char_id in lost:
		formations.append({
			"name": "Zombie %s" % char_id.capitalize(),
			"sprite": "zombie_" + char_id,
			"max_hp": 800,
			"current_hp": 800,
			"attack": 60,
			"defense": 30,
			"speed": 10,
			"exp_reward": 200,
			"gil_reward": 100,
			"actions": [{"type": "attack", "weight": 100}],
			"elemental_weaknesses": ["light"],
			"is_undead": true,
		})
	return formations

# ===== CURE FOUND =====

func mark_cure_found() -> void:
	FlagManager.set_flag("cure_found", true)
	FlagManager.set_flag("kella_saved", true)
	story_event_triggered.emit("cure_found")

# ===== POST-CREDITS SEQUENCE =====

func start_best_ending_sequence() -> void:
	FlagManager.set_flag("slaver_island_completed", false)
	SceneTransition.change_scene("res://scenes/locations/slaver_island.tscn", "start")

# ===== KEY ITEM TRIGGERS =====

func on_key_item_obtained(item_id: String) -> void:
	match item_id:
		"baby_dragon":
			# Explain key item system to player
			DialogueManager.start_dialogue_direct([
				{"type": "text", "speaker": "Javin",
				 "text": "A baby dragon! It seems drawn to me... I should keep it safe.",
				 "portrait": "javin"},
				{"type": "text", "speaker": "System",
				 "text": "Key Items cannot be sold or destroyed. They may unlock hidden potential in your companions.",
				 "portrait": ""},
				{"type": "end"}
			])
		"crown_of_flowers":
			if FlagManager.is_flag("cookie_recruited"):
				FlagManager.set_flag("cookie_crown_comment_triggered", true)
		"tuft_of_panda_fur":
			if FlagManager.is_flag("iris_recruited"):
				var iris := PartyManager.get_character("iris")
				iris["panda_form_available"] = true
