extends Node
## RecruitmentSystem - Handles all character recruitment, deadline, zombie conversion

signal character_recruited(char_id: String)
signal recruitment_deadline_passed
signal character_lost(char_id: String)

# Characters that can be missed permanently
const OPTIONAL_CHARACTERS := ["cookie", "iris", "fritzzit", "crankpot", "yipp"]

# Required characters (story guarantees encounter)
const REQUIRED_CHARACTERS := ["javin", "frostbite", "fei", "michael", "flood", "hannah", "warghoul"]

# Backup locations for optional characters
const BACKUP_LOCATIONS := {
	"cookie": ["halfling_village", "army_camp", "imperial_city"],
	"iris": ["halfling_village", "army_camp", "imperial_city"],
	"fritzzit": ["imperial_city_inn", "army_camp"],
	"crankpot": ["imperial_city_inn", "army_camp"],
	"yipp": ["yipp_spawn_dungeon", "imperial_city_magic_shop"],
}

func attempt_recruit(char_id: String) -> void:
	if FlagManager.is_flag(char_id + "_recruited"):
		return  # Already recruited

	if FlagManager.is_flag("recruitment_deadline_passed"):
		# Too late - character becomes zombie
		_convert_to_zombie(char_id)
		return

	# Start recruitment dialogue
	DialogueManager.start_dialogue(char_id + "_recruitment")
	await DialogueManager.dialogue_ended

func confirm_recruit(char_id: String) -> bool:
	if FlagManager.is_flag("recruitment_deadline_passed"):
		return false

	# Special case: Fritzzit and Crankpot must be recruited together
	if char_id == "fritzzit":
		return _recruit_pair("fritzzit", "crankpot")
	if char_id == "crankpot":
		return _recruit_pair("fritzzit", "crankpot")

	_do_recruit(char_id)
	return true

func _recruit_pair(char_a: String, char_b: String) -> bool:
	_do_recruit(char_a)
	_do_recruit(char_b)
	return true

func _do_recruit(char_id: String) -> void:
	if FlagManager.is_flag(char_id + "_recruited"):
		return

	FlagManager.set_flag(char_id + "_recruited", true)
	GameManager.characters_recruited.append(char_id)

	# Add to reserve party if active party full
	if GameManager.active_party.size() < 3:
		GameManager.active_party.append(char_id)
	else:
		GameManager.reserve_party.append(char_id)

	AudioManager.play_sfx("character_join")
	character_recruited.emit(char_id)

	# Special: Michael auto-gets Sentimental Traveler's Pouch
	if char_id == "michael" and not GameManager.has_key_item("sentimental_pouch"):
		GameManager.add_key_item("sentimental_pouch")

func trigger_deadline() -> void:
	if FlagManager.is_flag("recruitment_deadline_passed"):
		return

	FlagManager.set_flag("recruitment_deadline_passed", true)

	# Convert all un-recruited optionals to zombies
	for char_id in OPTIONAL_CHARACTERS:
		if not FlagManager.is_flag(char_id + "_recruited"):
			_convert_to_zombie(char_id)

	# Warghoul is required by deadline - if not recruited, auto-recruit
	if not FlagManager.is_flag("warghoul_recruited"):
		_do_recruit("warghoul")

	recruitment_deadline_passed.emit()

func _convert_to_zombie(char_id: String) -> void:
	var lost: Array = FlagManager.get_flag("lost_characters")
	if not char_id in lost:
		lost.append(char_id)
		FlagManager.set_flag("lost_characters", lost)
		GameManager.lost_characters.append(char_id)
	character_lost.emit(char_id)

func get_lost_characters() -> Array:
	return FlagManager.get_flag("lost_characters")

func is_available(char_id: String) -> bool:
	if FlagManager.is_flag(char_id + "_recruited"):
		return false
	if FlagManager.is_flag("recruitment_deadline_passed"):
		return false
	return true

# Check if Yipp should be at magic shop (declined in dungeon)
func yipp_at_magic_shop() -> bool:
	return (FlagManager.is_flag("yipp_encountered") and
			not FlagManager.is_flag("yipp_recruited") and
			not FlagManager.is_flag("recruitment_deadline_passed"))

# Determine Yipp's spawn dungeon at game start (random pre-Orisia dungeon)
func determine_yipp_spawn() -> String:
	var pre_orisia_dungeons := [
		"undead_lands_dungeon",
		"halfling_caves",
		"kobold_warren_depths",
		"surface_ruins",
		"imperial_sewers"
	]
	var spawn := pre_orisia_dungeons[randi() % pre_orisia_dungeons.size()]
	FlagManager.set_flag("yipp_spawn_dungeon", spawn)
	FlagManager.set_flag("yipp_dungeon_determined", true)

	# Key items (Holy Symbol and Wine Glass) spawn in the OTHER pre-Orisia dungeons
	var remaining := pre_orisia_dungeons.filter(func(d): return d != spawn)
	remaining.shuffle()
	FlagManager.set_flag("holy_symbol_dungeon", remaining[0])
	FlagManager.set_flag("wine_glass_dungeon", remaining[1])

	return spawn

# NG+ commentary trigger
func check_ng_plus_yipp_comment(current_location: String) -> void:
	if not FlagManager.is_flag("new_game_plus_active"):
		return
	var prev_spawn: String = FlagManager.get_flag("previous_yipp_spawn")
	if prev_spawn == "" or current_location != prev_spawn:
		return
	if not FlagManager.is_flag("frostbite_recruited"):
		return

	# Frostbite comments at Yipp's previous spawn location
	DialogueManager.start_dialogue_direct([
		{"type": "text", "speaker": "Frostbite",
		 "text": "Why does this smell like dead rat?",
		 "portrait": "frostbite"},
		{"type": "end"}
	])

# NG+ baby dragon commentary
func check_ng_plus_baby_dragon_comment() -> void:
	if not FlagManager.is_flag("new_game_plus_active"):
		return
	if FlagManager.is_flag("previous_baby_dragon_obtained"):
		return  # Got it last time, no comment needed
	# Javin hears baby dragon
	DialogueManager.start_dialogue_direct([
		{"type": "text", "speaker": "Javin",
		 "text": "I hear a baby dragon somewhere nearby...",
		 "portrait": "javin"},
		{"type": "end"}
	])
