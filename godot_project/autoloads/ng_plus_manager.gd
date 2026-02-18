## ng_plus_manager.gd
## Handles New Game Plus commentary and state carry-over.
## Loads ng_plus_commentary.json and injects lines based on flag conditions.
## Called by location scenes and dialogue_manager when on_ng_plus is active.
extends Node

const COMMENTARY_PATH: String = "res://data/dialogues/ng_plus_commentary.json"

var _commentary: Dictionary = {}
var _loaded: bool = false


# ---------------------------------------------------------------------------
# _ready
# ---------------------------------------------------------------------------
func _ready() -> void:
	_load_commentary()


func _load_commentary() -> void:
	if not FileAccess.file_exists(COMMENTARY_PATH):
		return
	var f := FileAccess.open(COMMENTARY_PATH, FileAccess.READ)
	if f == null:
		return
	var text := f.get_as_text()
	f.close()
	var parsed = JSON.parse_string(text)
	if parsed is Dictionary and "commentary" in parsed:
		_commentary = parsed["commentary"]
		_loaded = true


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

## Returns true if New Game+ is active
func is_ng_plus() -> bool:
	return GameManager.new_game_plus_active


## Get the best matching commentary line for a given trigger key.
## Returns a Dictionary with "speaker" and "text", or empty dict if none match.
func get_commentary(trigger_key: String) -> Dictionary:
	if not is_ng_plus() or not _loaded:
		return {}

	var entry: Dictionary = _commentary.get(trigger_key, {})
	if entry.is_empty():
		return {}

	if _check_condition(entry.get("condition", "")):
		return entry

	return {}


## Check if a commentary condition string evaluates to true.
## Supports: "flag_name", "NOT flag_name", "A AND B", "A OR B"
func _check_condition(condition: String) -> bool:
	if condition.is_empty():
		return true

	# Handle AND
	if " AND " in condition:
		var parts := condition.split(" AND ")
		for part in parts:
			if not _check_single(part.strip_edges()):
				return false
		return true

	# Handle OR
	if " OR " in condition:
		var parts := condition.split(" OR ")
		for part in parts:
			if _check_single(part.strip_edges()):
				return true
		return false

	return _check_single(condition.strip_edges())


func _check_single(condition: String) -> bool:
	if condition.begins_with("NOT "):
		var flag: String = condition.substr(4).strip_edges()
		return not _resolve_flag(flag)
	return _resolve_flag(condition)


func _resolve_flag(flag_name: String) -> bool:
	match flag_name:
		"ng_plus_active":
			return GameManager.new_game_plus_active
		"previous_all_recruited":
			return GameManager.ng_plus_data.get("all_recruited", false)
		"previous_michael_recruited":
			return GameManager.ng_plus_data.get("michael_recruited", false)
		"previous_hannah_recruited":
			return GameManager.ng_plus_data.get("hannah_recruited", false)
		"previous_flood_died":
			return GameManager.ng_plus_data.get("flood_died", false)
		"previous_ending_good":
			return GameManager.ng_plus_data.get("ending", "") == "good"
		"previous_ending_normal":
			return GameManager.ng_plus_data.get("ending", "") == "normal"
		"previous_ending_bad":
			return GameManager.ng_plus_data.get("ending", "") == "bad"
		"previous_best_ending":
			return GameManager.ng_plus_data.get("ending", "") == "best"
		"previous_vampire_recruited":
			return GameManager.ng_plus_data.get("vampire_recruited", false)
		"yipp_dungeon_differs_from_previous":
			var prev_yipp: String = GameManager.ng_plus_data.get("yipp_dungeon", "")
			var current_yipp: String = FlagManager.get_flag("yipp_spawn_location")
			return prev_yipp != current_yipp and not prev_yipp.is_empty()
		_:
			return FlagManager.is_flag(flag_name)


# ---------------------------------------------------------------------------
# Inject commentary into a location scene
# ---------------------------------------------------------------------------

## Called by location scripts to potentially inject a NG+ commentary line.
## location_trigger: e.g. "warren_entry_ng"
## Returns true if commentary was shown (caller can skip normal trigger).
func try_inject(location_trigger: String) -> bool:
	var data: Dictionary = get_commentary(location_trigger)
	if data.is_empty():
		return false

	# Also try variant with "_ng" suffix if base key doesn't match
	if data.is_empty():
		data = get_commentary(location_trigger + "_ng")
	if data.is_empty():
		return false

	# Show the commentary as a brief dialogue pop
	var speaker: String = data.get("speaker", "")
	var text: String = data.get("text", "")
	if text.is_empty():
		return false

	DialogueManager.start_dialogue_direct(speaker, text)
	return true


# ---------------------------------------------------------------------------
# Save NG+ carry-over data before starting NG+
# ---------------------------------------------------------------------------

## Collect all data to carry into a New Game Plus run
func collect_ng_plus_data() -> Dictionary:
	var recruited: Array = GameManager.characters_recruited.duplicate()
	return {
		"playthrough_count": GameManager.playthrough_count,
		"ending": FlagManager.get_flag("ending_achieved"),
		"all_recruited": recruited.size() >= 12,
		"michael_recruited": "michael" in recruited,
		"hannah_recruited": "hannah" in recruited,
		"flood_died": FlagManager.is_flag("flood_permanent_death"),
		"vampire_recruited": "vampire" in recruited,
		"yipp_dungeon": FlagManager.get_flag("yipp_spawn_location"),
		"characters_recruited": recruited,
		"completed_orisia_sidequest": FlagManager.is_flag("orisia_sidequest_complete"),
		"best_ending": FlagManager.is_flag("best_ending_achieved"),
		# Starting level based on ending
		"starting_level": 99 if FlagManager.is_flag("orisia_sidequest_complete") else 75
	}
