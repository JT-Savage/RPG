## overworld.gd
## The world map for "There Will Be Kobolds".
## Displays all regions as icons on a scrollable 256x224 map.
## Player selects a destination icon to fast-travel (once unlocked).
extends Node2D
class_name Overworld

# ---------------------------------------------------------------------------
# Signals
# ---------------------------------------------------------------------------
signal location_selected(location_id: String)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
const MUSIC_TRACK: String = "overworld_map"
const CURSOR_SPEED: float = 120.0

# All map locations with pixel positions on the overworld map sprite
const MAP_LOCATIONS: Dictionary = {
	"tutorial_warren": {
		"label": "Kobold Warren",
		"position": Vector2(40, 160),
		"icon": "warren",
		"scene": "res://scenes/locations/tutorial_warren.tscn",
		"spawn": "default",
		"unlock_flag": ""          # Always accessible
	},
	"surface_forest": {
		"label": "Surface Forest",
		"position": Vector2(80, 130),
		"icon": "forest",
		"scene": "res://scenes/locations/surface_forest.tscn",
		"spawn": "default",
		"unlock_flag": "escaped_warren"
	},
	"kobold_village": {
		"label": "Kobold Village",
		"position": Vector2(60, 110),
		"icon": "village",
		"scene": "res://scenes/locations/kobold_village.tscn",
		"spawn": "default",
		"unlock_flag": "found_kobold_village"
	},
	"imperial_city": {
		"label": "Imperial City",
		"position": Vector2(140, 100),
		"icon": "city",
		"scene": "res://scenes/locations/imperial_city.tscn",
		"spawn": "city_gate",
		"unlock_flag": "reached_imperial_city"
	},
	"catacomb_entrance": {
		"label": "Catacombs",
		"position": Vector2(155, 130),
		"icon": "dungeon",
		"scene": "res://scenes/locations/catacomb_entrance.tscn",
		"spawn": "default",
		"unlock_flag": "found_catacombs"
	},
	"swamp_village": {
		"label": "Swamp Village",
		"position": Vector2(100, 170),
		"icon": "swamp",
		"scene": "res://scenes/locations/swamp_village.tscn",
		"spawn": "default",
		"unlock_flag": "crossed_swamp"
	},
	"mountain_pass": {
		"label": "Mountain Pass",
		"position": Vector2(180, 80),
		"icon": "mountain",
		"scene": "res://scenes/locations/mountain_pass.tscn",
		"spawn": "default",
		"unlock_flag": "found_mountain_pass"
	},
	"army_camp": {
		"label": "Army Camp",
		"position": Vector2(200, 120),
		"icon": "camp",
		"scene": "res://scenes/locations/army_camp.tscn",
		"spawn": "default",
		"unlock_flag": "reached_army_camp"
	},
	"floating_island": {
		"label": "Floating Island",
		"position": Vector2(210, 50),
		"icon": "island",
		"scene": "res://scenes/locations/floating_island.tscn",
		"spawn": "default",
		"unlock_flag": "found_floating_island"
	},
	"orisia_island": {
		"label": "Orisia",
		"position": Vector2(230, 30),
		"icon": "orisia",
		"scene": "res://scenes/locations/orisia_island.tscn",
		"spawn": "default",
		"unlock_flag": "orisia_island_unlocked"
	},
	"final_dungeon": {
		"label": "Void Spire",
		"position": Vector2(128, 20),
		"icon": "final",
		"scene": "res://scenes/locations/final_dungeon.tscn",
		"spawn": "default",
		"unlock_flag": "void_spire_appeared"
	},
	"slaver_island": {
		"label": "Slaver Island",
		"position": Vector2(30, 30),
		"icon": "skull",
		"scene": "res://scenes/locations/slaver_island.tscn",
		"spawn": "default",
		"unlock_flag": "best_ending_achieved"
	}
}

# ---------------------------------------------------------------------------
# Node references
# ---------------------------------------------------------------------------
@onready var map_sprite: Sprite2D = $MapSprite
@onready var cursor: Sprite2D = $Cursor
@onready var location_label: Label = $UI/LocationLabel
@onready var party_info: Control = $UI/PartyInfo
@onready var location_icons: Node2D = $LocationIcons
@onready var confirm_dialog: Control = $UI/ConfirmDialog

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
var _locations: Array[Dictionary] = []   # Filtered to unlocked locations
var _selected_index: int = 0
var _input_cooldown: float = 0.0
const INPUT_COOLDOWN: float = 0.18

# ---------------------------------------------------------------------------
# _ready
# ---------------------------------------------------------------------------
func _ready() -> void:
	AudioManager.play_music(MUSIC_TRACK)
	_build_location_list()
	_build_location_icons()
	_update_party_info()
	_select_nearest_to_current_location()
	_update_cursor()
	_update_label()


func _build_location_list() -> void:
	_locations.clear()
	for loc_id in MAP_LOCATIONS:
		var data: Dictionary = MAP_LOCATIONS[loc_id]
		var flag: String = data.get("unlock_flag", "")
		if flag.is_empty() or FlagManager.is_flag(flag):
			var entry: Dictionary = data.duplicate()
			entry["id"] = loc_id
			_locations.append(entry)


func _build_location_icons() -> void:
	for child in location_icons.get_children():
		child.queue_free()

	for loc in _locations:
		var icon_sprite: Sprite2D = Sprite2D.new()
		icon_sprite.name = loc["id"]
		icon_sprite.position = loc["position"]
		# Texture loaded by generate_assets; fallback to white 8x8 rect
		var tex_path: String = "res://assets/sprites/overworld/%s.png" % loc["icon"]
		if ResourceLoader.exists(tex_path):
			icon_sprite.texture = load(tex_path)
		else:
			var img: Image = Image.create(8, 8, false, Image.FORMAT_RGBA8)
			img.fill(Color.WHITE)
			icon_sprite.texture = ImageTexture.create_from_image(img)
		location_icons.add_child(icon_sprite)


func _select_nearest_to_current_location() -> void:
	var current: String = GameManager.current_location
	for i in range(_locations.size()):
		if _locations[i]["id"] == current:
			_selected_index = i
			return
	_selected_index = 0


# ---------------------------------------------------------------------------
# _process
# ---------------------------------------------------------------------------
func _process(delta: float) -> void:
	if _input_cooldown > 0.0:
		_input_cooldown -= delta
		return

	if confirm_dialog and confirm_dialog.visible:
		_handle_dialog_input()
		return

	var moved: bool = false
	if InputManager.is_action_just_pressed("ui_right"):
		_selected_index = (_selected_index + 1) % _locations.size()
		moved = true
	elif InputManager.is_action_just_pressed("ui_left"):
		_selected_index = (_selected_index - 1 + _locations.size()) % _locations.size()
		moved = true
	elif InputManager.is_action_just_pressed("ui_down"):
		_select_next_by_y(1)
		moved = true
	elif InputManager.is_action_just_pressed("ui_up"):
		_select_next_by_y(-1)
		moved = true

	if moved:
		_update_cursor()
		_update_label()
		_input_cooldown = INPUT_COOLDOWN
		AudioManager.play_sfx("cursor_move")

	if InputManager.is_action_just_pressed("ui_accept"):
		_confirm_travel()
	elif InputManager.is_action_just_pressed("ui_cancel"):
		# No cancel on overworld – open pause menu instead
		get_tree().paused = true
		var pm: PackedScene = load("res://scenes/ui/pause_menu.tscn")
		if pm:
			var menu: Node = pm.instantiate()
			add_child(menu)


func _select_next_by_y(direction: int) -> void:
	# Find the location icon closest in Y direction from current selection
	if _locations.is_empty():
		return
	var current_pos: Vector2 = _locations[_selected_index]["position"]
	var best_idx: int = _selected_index
	var best_score: float = INF

	for i in range(_locations.size()):
		if i == _selected_index:
			continue
		var pos: Vector2 = _locations[i]["position"]
		var dy: float = pos.y - current_pos.y
		if direction > 0 and dy > 4.0:
			var score: float = dy + abs(pos.x - current_pos.x) * 0.5
			if score < best_score:
				best_score = score
				best_idx = i
		elif direction < 0 and dy < -4.0:
			var score: float = -dy + abs(pos.x - current_pos.x) * 0.5
			if score < best_score:
				best_score = score
				best_idx = i

	_selected_index = best_idx


func _update_cursor() -> void:
	if _locations.is_empty() or not cursor:
		return
	var target_pos: Vector2 = _locations[_selected_index]["position"]
	cursor.position = target_pos


func _update_label() -> void:
	if _locations.is_empty() or not location_label:
		return
	location_label.text = _locations[_selected_index]["label"]


func _update_party_info() -> void:
	if not party_info:
		return
	# Display first 4 party members with HP/MP
	var party: Array = PartyManager.get_active_party()
	for child in party_info.get_children():
		child.queue_free()
	for member in party:
		var stats: Dictionary = PartyManager.get_character_stats(member)
		if stats.is_empty():
			continue
		var lbl: Label = Label.new()
		lbl.text = "%s  HP:%d/%d" % [stats.get("name", member), stats.get("current_hp", 0), stats.get("max_hp", 1)]
		party_info.add_child(lbl)


func _confirm_travel() -> void:
	if _locations.is_empty():
		return
	var dest: Dictionary = _locations[_selected_index]
	if dest["id"] == GameManager.current_location:
		AudioManager.play_sfx("error")
		return

	if confirm_dialog:
		confirm_dialog.visible = true
		var label: Label = confirm_dialog.get_node_or_null("Label")
		if label:
			label.text = "Travel to %s?" % dest["label"]
	else:
		_do_travel()


func _handle_dialog_input() -> void:
	if Input.is_action_just_pressed("ui_accept"):
		confirm_dialog.visible = false
		_do_travel()
	elif Input.is_action_just_pressed("ui_cancel"):
		confirm_dialog.visible = false


func _do_travel() -> void:
	var dest: Dictionary = _locations[_selected_index]
	AudioManager.play_sfx("confirm")
	SceneTransition.change_scene(dest["scene"], dest["spawn"])
