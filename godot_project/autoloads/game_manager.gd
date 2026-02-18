extends Node
## GameManager - Global game state, playtime, current location tracking

signal playtime_updated(seconds: float)

# Current game state
var current_location: String = "tutorial_warren"
var player_position: Vector2 = Vector2.ZERO
var playtime_seconds: float = 0.0
var is_paused: bool = false
var atb_paused_in_menu: bool = true  # Pause ATB during menus (setting)
var turn_based_mode: bool = false     # Fallback turn-based mode (setting)

# Inventory
var items: Dictionary = {"potion": 5}         # item_id -> count
var equipment: Dictionary = {}                  # char_id -> {slot: equip_id}
var key_items: Array = []                       # list of key item IDs
var gil: int = 100

# Character party state
var active_party: Array = ["javin"]            # Up to 3 char IDs
var reserve_party: Array = []
var characters_recruited: Array = ["javin"]
var lost_characters: Array = []

# Map data
var map_data: Dictionary = {}

# New Game+
var new_game_plus_active: bool = false
var playthrough_count: int = 1
var ng_plus_data: Dictionary = {}

# Mobile/platform
var is_mobile: bool = false
var ads_removed: bool = false

func _ready() -> void:
	_detect_platform()
	_load_premium_status()

func _process(delta: float) -> void:
	if not is_paused:
		playtime_seconds += delta
		playtime_updated.emit(playtime_seconds)

func _detect_platform() -> void:
	var os_name := OS.get_name()
	is_mobile = os_name in ["Android", "iOS"]

func _load_premium_status() -> void:
	var cfg := ConfigFile.new()
	if cfg.load("user://premium.cfg") == OK:
		ads_removed = cfg.get_value("premium", "ads_removed", false)

func remove_ads() -> void:
	ads_removed = true
	var cfg := ConfigFile.new()
	cfg.set_value("premium", "ads_removed", true)
	cfg.save("user://premium.cfg")

# ===== INVENTORY MANAGEMENT =====

func add_item(item_id: String, quantity: int = 1) -> void:
	items[item_id] = items.get(item_id, 0) + quantity

func remove_item(item_id: String, quantity: int = 1) -> bool:
	if not items.has(item_id):
		return false
	if items[item_id] < quantity:
		return false
	items[item_id] -= quantity
	if items[item_id] <= 0:
		items.erase(item_id)
	return true

func has_item(item_id: String, quantity: int = 1) -> bool:
	return items.get(item_id, 0) >= quantity

func get_item_quantity(item_id: String) -> int:
	return items.get(item_id, 0)

func get_all_items() -> Dictionary:
	return items.duplicate()

## Equipment inventory (separate from consumables)
func add_equipment(equip_id: String) -> void:
	if not equip_id in equipment:
		equipment[equip_id] = 0
	equipment[equip_id] += 1

func remove_equipment(equip_id: String) -> bool:
	if not equip_id in equipment or equipment[equip_id] <= 0:
		return false
	equipment[equip_id] -= 1
	if equipment[equip_id] <= 0:
		equipment.erase(equip_id)
	return true

func has_equipment(equip_id: String) -> bool:
	return equipment.get(equip_id, 0) > 0

func add_key_item(key_item_id: String) -> void:
	if not key_item_id in key_items:
		key_items.append(key_item_id)
		FlagManager.set_flag("ki_" + key_item_id, true)
		AudioManager.play_sfx("key_item_get")

func has_key_item(key_item_id: String) -> bool:
	return key_item_id in key_items

# ===== GIL MANAGEMENT =====

func spend_gil(amount: int) -> bool:
	if gil < amount:
		return false
	gil -= amount
	return true

func earn_gil(amount: int) -> void:
	gil += amount

# ===== PARTY MANAGEMENT =====

func get_active_characters() -> Array:
	return active_party.duplicate()

func get_all_party() -> Array:
	return active_party + reserve_party

func is_in_active_party(char_id: String) -> bool:
	return char_id in active_party

func swap_party_member(bench_id: String, active_id: String) -> bool:
	if not bench_id in reserve_party:
		return false
	if not active_id in active_party:
		return false
	var bench_idx := reserve_party.find(bench_id)
	var active_idx := active_party.find(active_id)
	reserve_party[bench_idx] = active_id
	active_party[active_idx] = bench_id
	return true

# ===== LOCATION =====

func change_location(location_id: String) -> void:
	current_location = location_id
	FlagManager.set_flag("current_location", location_id)

# ===== SAVE DATA EXPORT =====

func export_state() -> Dictionary:
	return {
		"current_location": current_location,
		"player_position": {"x": player_position.x, "y": player_position.y},
		"playtime_seconds": playtime_seconds,
		"items": items.duplicate(),
		"equipment": equipment.duplicate(),
		"key_items": key_items.duplicate(),
		"gil": gil,
		"active_party": active_party.duplicate(),
		"reserve_party": reserve_party.duplicate(),
		"characters_recruited": characters_recruited.duplicate(),
		"lost_characters": lost_characters.duplicate(),
		"new_game_plus_active": new_game_plus_active,
		"playthrough_count": playthrough_count,
		"ng_plus_data": ng_plus_data.duplicate(),
		"map_data": map_data.duplicate(),
		"atb_paused_in_menu": atb_paused_in_menu,
		"turn_based_mode": turn_based_mode,
	}

func import_state(data: Dictionary) -> void:
	current_location = data.get("current_location", "tutorial_warren")
	var pos = data.get("player_position", {"x": 0, "y": 0})
	player_position = Vector2(pos.get("x", 0), pos.get("y", 0))
	playtime_seconds = data.get("playtime_seconds", 0.0)
	items = data.get("items", {"potion": 5})
	equipment = data.get("equipment", {})
	key_items = data.get("key_items", [])
	gil = data.get("gil", 100)
	active_party = data.get("active_party", ["javin"])
	reserve_party = data.get("reserve_party", [])
	characters_recruited = data.get("characters_recruited", ["javin"])
	lost_characters = data.get("lost_characters", [])
	new_game_plus_active = data.get("new_game_plus_active", false)
	playthrough_count = data.get("playthrough_count", 1)
	ng_plus_data = data.get("ng_plus_data", {})
	map_data = data.get("map_data", {})
	atb_paused_in_menu = data.get("atb_paused_in_menu", true)
	turn_based_mode = data.get("turn_based_mode", false)

func new_game(ng_plus: Dictionary = {}) -> void:
	current_location = "tutorial_warren"
	player_position = Vector2.ZERO
	playtime_seconds = 0.0
	items = {"potion": 5}
	equipment = {}
	key_items = []
	gil = 100
	active_party = ["javin"]
	reserve_party = []
	characters_recruited = ["javin"]
	lost_characters = []
	map_data = {}
	new_game_plus_active = not ng_plus.is_empty()
	ng_plus_data = ng_plus
	playthrough_count = ng_plus.get("playthrough_count", 1) + (1 if not ng_plus.is_empty() else 0)
	FlagManager.reset_flags(ng_plus)
	PartyManager.initialize_party(ng_plus)
