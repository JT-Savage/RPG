extends Node
## SaveSystem - Handles quicksave, autosave, and 100 manual save slots

const SAVE_DIR := "user://saves/"
const MAX_SLOTS := 100
const MIN_SLOTS := 5
const AUTOSAVE_FILE := "user://saves/autosave.dat"
const QUICKSAVE_FILE := "user://saves/quicksave.dat"
const VERSION := "1.0.0"

signal save_completed(slot: int)
signal load_completed(success: bool)

func _ready() -> void:
	DirAccess.make_dir_recursive_absolute(SAVE_DIR)

# ===== SAVE =====

func save_slot(slot: int) -> bool:
	var data := _collect_save_data(slot, "manual")
	var path := SAVE_DIR + "save_slot_%03d.dat" % slot
	return _write_save(path, data)

func autosave() -> bool:
	var data := _collect_save_data(-1, "autosave")
	return _write_save(AUTOSAVE_FILE, data)

func quicksave() -> bool:
	var data := _collect_save_data(-1, "quicksave")
	AudioManager.play_sfx("save_point")
	return _write_save(QUICKSAVE_FILE, data)

# ===== LOAD =====

func load_slot(slot: int) -> bool:
	var path := SAVE_DIR + "save_slot_%03d.dat" % slot
	return _read_and_apply(path)

func load_autosave() -> bool:
	return _read_and_apply(AUTOSAVE_FILE)

func load_quicksave() -> bool:
	return _read_and_apply(QUICKSAVE_FILE)

func has_autosave() -> bool:
	return FileAccess.file_exists(AUTOSAVE_FILE)

func has_quicksave() -> bool:
	return FileAccess.file_exists(QUICKSAVE_FILE)

func has_save_slot(slot: int) -> bool:
	return FileAccess.file_exists(SAVE_DIR + "save_slot_%03d.dat" % slot)

func delete_slot(slot: int) -> bool:
	var path := SAVE_DIR + "save_slot_%03d.dat" % slot
	if FileAccess.file_exists(path):
		return DirAccess.remove_absolute(path) == OK
	return false

# ===== SAVE SLOT INFO (for display) =====

func get_slot_info(slot: int) -> Dictionary:
	var path := SAVE_DIR + "save_slot_%03d.dat" % slot
	if not FileAccess.file_exists(path):
		return {}
	var data := _read_save(path)
	if data.is_empty():
		return {}
	return {
		"slot": slot,
		"timestamp": data.get("timestamp", ""),
		"location": data.get("current_location", ""),
		"playtime": data.get("playtime_seconds", 0.0),
		"playthrough": data.get("playthrough_count", 1),
		"new_game_plus": data.get("new_game_plus_active", false),
		"party": data.get("active_party", []),
	}

func get_all_slot_infos() -> Array:
	var slots := []
	for i in range(1, MAX_SLOTS + 1):
		if has_save_slot(i):
			slots.append(get_slot_info(i))
	return slots

# ===== INTERNAL =====

func _collect_save_data(slot: int, save_type: String) -> Dictionary:
	var gm := GameManager.export_state()
	var fm := FlagManager.get_all_flags()
	var pm := PartyManager.export_state()

	return {
		"version": VERSION,
		"timestamp": Time.get_datetime_string_from_system(),
		"slot": slot,
		"save_type": save_type,

		# Game Manager data
		"current_location": gm.get("current_location", "tutorial_warren"),
		"player_position": gm.get("player_position", {"x": 0, "y": 0}),
		"playtime_seconds": gm.get("playtime_seconds", 0.0),
		"items": gm.get("items", {}),
		"equipment": gm.get("equipment", {}),
		"key_items": gm.get("key_items", []),
		"gil": gm.get("gil", 100),
		"active_party": gm.get("active_party", ["javin"]),
		"reserve_party": gm.get("reserve_party", []),
		"characters_recruited": gm.get("characters_recruited", ["javin"]),
		"lost_characters": gm.get("lost_characters", []),
		"new_game_plus_active": gm.get("new_game_plus_active", false),
		"playthrough_count": gm.get("playthrough_count", 1),
		"ng_plus_data": gm.get("ng_plus_data", {}),
		"map_data": gm.get("map_data", {}),
		"atb_paused_in_menu": gm.get("atb_paused_in_menu", true),
		"turn_based_mode": gm.get("turn_based_mode", false),

		# Story flags
		"flags": fm,

		# Party character stats
		"party_data": pm,
	}

func _write_save(path: String, data: Dictionary) -> bool:
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		push_error("SaveSystem: Cannot open '%s' for writing" % path)
		return false
	file.store_string(JSON.stringify(data))
	file.close()
	return true

func _read_save(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var content := file.get_as_text()
	file.close()
	var parsed := JSON.parse_string(content)
	if parsed == null:
		push_error("SaveSystem: Failed to parse save file '%s'" % path)
		return {}
	return parsed

func _read_and_apply(path: String) -> bool:
	var data := _read_save(path)
	if data.is_empty():
		load_completed.emit(false)
		return false

	# Apply to GameManager
	GameManager.import_state(data)

	# Apply flags
	if data.has("flags"):
		FlagManager.load_flags(data["flags"])

	# Apply party data
	if data.has("party_data"):
		PartyManager.import_state(data["party_data"])

	load_completed.emit(true)
	return true

# ===== NEW GAME PLUS DATA =====

func save_ng_plus_data() -> bool:
	var ng_data := {
		"timestamp": Time.get_datetime_string_from_system(),
		"playthrough_count": GameManager.playthrough_count,
		"characters_recruited": GameManager.characters_recruited.duplicate(),
		"lost_characters": GameManager.lost_characters.duplicate(),
		"yipp_alignment_previous": FlagManager.get_flag("yipp_alignment"),
		"baby_dragon_saved": FlagManager.is_flag("ki_baby_dragon"),
		"cure_found": FlagManager.is_flag("cure_found"),
		"flood_died": FlagManager.is_flag("flood_dead"),
		"ending_achieved": FlagManager.get_flag("ending_type"),
		"yipp_spawn_dungeon": FlagManager.get_flag("yipp_spawn_dungeon"),
		"frostbite_had_ultimate": FlagManager.is_flag("frostbite_ultimate_weapon"),
		"fritzzit_had_ultimate": FlagManager.is_flag("fritzzit_ultimate_weapon"),
		"character_final_levels": PartyManager.get_all_final_levels(),
		"character_classes": PartyManager.get_all_classes(),
		"ultimate_weapons": PartyManager.get_ultimate_weapons(),
	}
	return _write_save("user://saves/ng_plus_data.dat", ng_data)

func load_ng_plus_data() -> Dictionary:
	return _read_save("user://saves/ng_plus_data.dat")

func has_ng_plus_data() -> bool:
	return FileAccess.file_exists("user://saves/ng_plus_data.dat")

## Open the save-select UI in save mode
func open_save_menu() -> void:
	var save_select_scene: PackedScene = load("res://scenes/ui/save_select.tscn")
	if save_select_scene == null:
		push_error("SaveSystem.open_save_menu: Could not load save_select.tscn")
		return
	var menu: Node = save_select_scene.instantiate()
	menu.set_meta("mode", "save")
	# Add to current scene root so it overlays everything
	var root: Node = Engine.get_main_loop().root
	root.add_child(menu)

## Open the save-select UI in load mode
func open_load_menu() -> void:
	var save_select_scene: PackedScene = load("res://scenes/ui/save_select.tscn")
	if save_select_scene == null:
		push_error("SaveSystem.open_load_menu: Could not load save_select.tscn")
		return
	var menu: Node = save_select_scene.instantiate()
	menu.set_meta("mode", "load")
	var root: Node = Engine.get_main_loop().root
	root.add_child(menu)
