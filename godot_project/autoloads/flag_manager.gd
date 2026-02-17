extends Node
## FlagManager - All story flags and game state flags
## Access with FlagManager.get_flag("flag_name") / FlagManager.set_flag("flag_name", value)

# ===== STORY FLAGS =====
var _flags: Dictionary = {
	# Tutorial / Warren
	"baby_dragon_saved": false,
	"baby_dragon_name": "Ember",
	"warren_infected": false,

	# Recruitment flags
	"frostbite_recruited": false,
	"fei_recruited": false,
	"michael_recruited": false,
	"flood_recruited": false,
	"hannah_recruited": false,
	"warghoul_recruited": false,
	"cookie_recruited": false,
	"iris_recruited": false,
	"fritzzit_recruited": false,
	"crankpot_recruited": false,
	"yipp_recruited": false,

	# Yipp special
	"yipp_alignment": "none",   # none / saint / vampire
	"yipp_spawn_dungeon": "",

	# World events
	"kobolds_released_from_city": false,
	"cookie_crown_comment_triggered": false,
	"iris_panda_fur_cutscene_triggered": false,
	"fei_grooming_cutscene_triggered": false,
	"fungal_enemies_removed": false,
	"flood_dead": false,

	# Story progression
	"orisia_met": false,
	"recruitment_deadline_passed": false,
	"lost_characters": [],
	"desert_entered": false,
	"army_blocks_return": false,

	# Dragon bosses
	"first_dragon_defeated": false,
	"second_dragon_defeated": false,

	# Endings
	"cure_found": false,
	"kella_saved": false,
	"necromancer_defeated": false,
	"ending_type": "",   # good / normal / bad / best
	"post_credits_unlocked": false,
	"slaver_island_completed": false,
	"captain_donald_defeated": false,

	# Character-specific
	"fei_dead_in_battle": false,
	"frostbite_ultimate_weapon": false,
	"fritzzit_ultimate_weapon": false,
	"all_orisia_sidequests_complete": false,

	# New Game+
	"new_game_plus_active": false,
	"previous_yipp_spawn": "",
	"previous_baby_dragon_obtained": false,
	"playthrough_count": 1,

	# Jerod's House
	"jerod_house_explored": false,
	"jerod_boss_defeated": false,
	"jerod_house_explosion": false,

	# Imperial City events
	"imperial_city_visited": false,
	"shotgun_blueprint_purchased": false,
	"sniper_rifle_blueprint_purchased": false,
	"met_michael": false,
	"met_flood": false,
	"met_hannah": false,
	"imperial_warren_explored": false,
	"imperial_warren_escape": false,
	"kobolds_released": false,

	# Misc
	"fritzzit_crankpot_available": false,
	"cookie_iris_rescued": false,
	"panda_fur_available": false,
	"warghoul_recruited_early": false,
	"orisia_ready_warning_given": false,

	# Dragon bosses detailed
	"hannah_scream_triggered": false,
	"flood_death_cutscene": false,
	"catacombs_unlocked": false,
	"kella_double_infected": false,
	"secret_boss_defeated": false,
	"yipp_betrayed": false,
	"yipp_dungeon_determined": false,

	# KEY ITEM FLAGS
	"ki_baby_dragon": false,
	"ki_sentimental_pouch": false,
	"ki_shotgun_blueprint": false,
	"ki_sniper_blueprint": false,
	"ki_grizzly_skull": false,
	"ki_orc_funeral_totem": false,
	"ki_molotov_cocktail": false,
	"ki_crown_of_flowers": false,
	"ki_tuft_of_panda_fur": false,
	"ki_holy_symbol": false,
	"ki_pewter_wine_glass": false,
}

func get_flag(flag_name: String) -> Variant:
	if _flags.has(flag_name):
		return _flags[flag_name]
	push_warning("FlagManager: Unknown flag '%s'" % flag_name)
	return null

func set_flag(flag_name: String, value: Variant) -> void:
	if _flags.has(flag_name):
		_flags[flag_name] = value
	else:
		push_warning("FlagManager: Setting unknown flag '%s'" % flag_name)
		_flags[flag_name] = value

func is_flag(flag_name: String) -> bool:
	return bool(get_flag(flag_name))

func add_to_lost_characters(char_id: String) -> void:
	var lost: Array = _flags.get("lost_characters", [])
	if not char_id in lost:
		lost.append(char_id)
	_flags["lost_characters"] = lost

func get_recruited_characters() -> Array:
	var recruited := []
	var all_chars := ["javin","frostbite","fei","michael","flood","hannah",
					  "warghoul","cookie","iris","fritzzit","crankpot","yipp"]
	for c in all_chars:
		if is_flag(c + "_recruited"):
			recruited.append(c)
	return recruited

func get_all_flags() -> Dictionary:
	return _flags.duplicate(true)

func load_flags(data: Dictionary) -> void:
	for key in data:
		_flags[key] = data[key]

func reset_flags(ng_plus_data: Dictionary = {}) -> void:
	# Store NG+ commentary data
	var prev_yipp_spawn = _flags.get("yipp_spawn_dungeon", "")
	var prev_baby_dragon = _flags.get("ki_baby_dragon", false)
	var prev_playthrough = _flags.get("playthrough_count", 1)

	# Reset all flags to defaults
	for key in _flags.keys():
		if _flags[key] is bool:
			_flags[key] = false
		elif _flags[key] is String:
			_flags[key] = ""
		elif _flags[key] is int:
			_flags[key] = 0
		elif _flags[key] is Array:
			_flags[key] = []

	_flags["yipp_alignment"] = "none"
	_flags["baby_dragon_name"] = "Ember"
	_flags["ending_type"] = ""

	if not ng_plus_data.is_empty():
		_flags["new_game_plus_active"] = true
		_flags["previous_yipp_spawn"] = prev_yipp_spawn
		_flags["previous_baby_dragon_obtained"] = prev_baby_dragon
		_flags["playthrough_count"] = prev_playthrough + 1

# Check if Orisia sidequest for a character is available
func can_do_orisia_sidequest(char_id: String) -> bool:
	if not is_flag(char_id + "_recruited"):
		return false
	if not is_flag("orisia_met"):
		return false
	# Check key item
	var key_item_map := {
		"javin": "ki_baby_dragon",
		"frostbite": "ki_shotgun_blueprint",
		"fei": "ki_grizzly_skull",
		"flood": "",          # No key item needed
		"hannah": "",         # No key item needed
		"michael": "ki_sentimental_pouch",
		"warghoul": "ki_orc_funeral_totem",
		"cookie": "ki_crown_of_flowers",
		"iris": "ki_tuft_of_panda_fur",
		"fritzzit": "ki_sniper_blueprint",
		"crankpot": "ki_molotov_cocktail",
		"yipp": ""            # Needs both holy_symbol AND wine_glass
	}
	if char_id == "yipp":
		return is_flag("ki_holy_symbol") and is_flag("ki_pewter_wine_glass")
	var ki := key_item_map.get(char_id, "")
	if ki == "":
		return true  # No key item needed (Flood, Hannah)
	return is_flag(ki)
