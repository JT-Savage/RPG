## base_location.gd
## Base class for all location scenes in "There Will Be Kobolds".
## Every location scene should extend this class and override handle_story_triggers()
## along with any per-location constants (MUSIC_TRACK, BATTLE_BACKGROUND, etc.).
extends Node2D
class_name BaseLocation

# ---------------------------------------------------------------------------
# Signals
# ---------------------------------------------------------------------------
signal location_ready
signal story_trigger_fired(trigger_id: String)

# ---------------------------------------------------------------------------
# Exports – child scenes set these in their own scripts or the Inspector
# ---------------------------------------------------------------------------
## Identifier used by SceneTransition to register this location as "visited".
@export var location_id: String = ""

## Music track identifier forwarded to AudioManager.
@export var music_track: String = ""

## Default battle background key used when spawning EncounterZones without an
## explicit background argument.
@export var default_battle_background: String = ""

# ---------------------------------------------------------------------------
# Internal references (resolved in _ready)
# ---------------------------------------------------------------------------
var _player_node: Node = null
var _encounter_zones: Array[Node] = []
var _npc_nodes: Dictionary = {}          # npc_id -> Node
var _save_point_node: Node = null

# ---------------------------------------------------------------------------
# Preloaded packed scenes (project-relative paths expected to exist)
# ---------------------------------------------------------------------------
const NPC_SCENE_PATH: String = "res://scenes/entities/npc.tscn"
const ENCOUNTER_ZONE_SCENE_PATH: String = "res://scenes/gameplay/encounter_zone.tscn"
const SAVE_POINT_SCENE_PATH: String = "res://scenes/ui/save_point.tscn"
const PLAYER_SCENE_PATH: String = "res://scenes/entities/player.tscn"


# ---------------------------------------------------------------------------
# _ready
# ---------------------------------------------------------------------------
func _ready() -> void:
	# 1. Add / position the player.
	_add_player()

	# 2. Start location music.
	_play_music()

	# 3. Perform autosave so progress is not lost on scene transitions.
	_run_autosave()

	# 4. Mark this location as visited in the global save state so fast-travel
	#    and other systems can reference it.
	_mark_visited()

	# 5. Check story triggers *after* everything else is ready.
	call_deferred("handle_story_triggers")

	emit_signal("location_ready")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

## Override in child classes to check story flags and fire cutscenes / events.
## Called once at the end of _ready() via call_deferred.
func handle_story_triggers() -> void:
	pass


## Transition to another location.
## location_id : the destination location identifier registered with SceneTransition.
## spawn_point : name of the SpawnPoint node at the destination (e.g. "from_warren").
func go_to_location(dest_location_id: String, spawn_point: String = "default") -> void:
	if not dest_location_id or dest_location_id.is_empty():
		push_error("BaseLocation.go_to_location: dest_location_id is empty.")
		return

	# Persist current state before leaving.
	_run_autosave()

	SceneTransition.change_scene(dest_location_id, spawn_point)


## Show the save-point UI (pause menu variant with save option highlighted).
func show_save_point() -> void:
	if _save_point_node and _save_point_node.has_method("show_save_ui"):
		_save_point_node.show_save_ui()
	else:
		# Fallback: ask SaveManager directly.
		if has_node("/root/SaveManager"):
			get_node("/root/SaveManager").open_save_menu()
		else:
			push_warning("BaseLocation.show_save_point: no SaveManager autoload found.")


## Spawn an NPC into the scene.
## npc_id   : key used to look up NPC data in the NPC database.
## position : world position for the NPC node.
## Returns the spawned NPC Node, or null on failure.
func add_npc(npc_id: String, position: Vector2) -> Node:
	if npc_id in _npc_nodes:
		push_warning("BaseLocation.add_npc: NPC '%s' already spawned." % npc_id)
		return _npc_nodes[npc_id]

	var npc_scene: PackedScene = load(NPC_SCENE_PATH)
	if npc_scene == null:
		push_error("BaseLocation.add_npc: Could not load NPC scene at '%s'." % NPC_SCENE_PATH)
		return null

	var npc: Node = npc_scene.instantiate()
	npc.name = npc_id

	# Let the NPC node configure itself from the database if it supports it.
	if npc.has_method("init_from_id"):
		npc.init_from_id(npc_id)

	add_child(npc)
	npc.global_position = position
	_npc_nodes[npc_id] = npc
	return npc


## Create an EncounterZone in the scene.
## rect       : Rect2 defining the zone's bounding box in local space.
## rate       : encounter rate, 0.0 – 1.0 (steps-based probability per tick).
## pool       : Array of enemy identifiers that can appear in this zone.
## background : battle background key; falls back to default_battle_background.
## Returns the spawned EncounterZone Node, or null on failure.
func spawn_encounter_zone(
		rect: Rect2,
		rate: float,
		pool: Array,
		background: String = "") -> Node:

	var ez_scene: PackedScene = load(ENCOUNTER_ZONE_SCENE_PATH)
	if ez_scene == null:
		push_error("BaseLocation.spawn_encounter_zone: Could not load EncounterZone scene.")
		return null

	var ez: Node = ez_scene.instantiate()
	add_child(ez)

	if ez.has_method("configure"):
		var bg: String = background if not background.is_empty() else default_battle_background
		ez.configure(rect, rate, pool, bg)
	else:
		push_warning("BaseLocation.spawn_encounter_zone: EncounterZone has no configure() method.")

	_encounter_zones.append(ez)
	return ez


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

func _add_player() -> void:
	# Only spawn a new player node if one doesn't already exist in the tree.
	# (SceneTransition may transfer an existing player node between scenes.)
	if has_node("Player"):
		_player_node = get_node("Player")
		_position_player_at_spawn()
		return

	if SceneTransition and SceneTransition.has_method("get_player_node"):
		_player_node = SceneTransition.get_player_node()
		if _player_node:
			add_child(_player_node)
			_position_player_at_spawn()
			return

	# Last resort: instantiate a fresh player.
	var player_scene: PackedScene = load(PLAYER_SCENE_PATH)
	if player_scene:
		_player_node = player_scene.instantiate()
		_player_node.name = "Player"
		add_child(_player_node)
		_position_player_at_spawn()
	else:
		push_error("BaseLocation._add_player: Could not load player scene.")


func _position_player_at_spawn() -> void:
	var spawn_id: String = SceneTransition.requested_spawn_point \
		if SceneTransition and "requested_spawn_point" in SceneTransition else "default"

	var spawn_node: Node = _find_spawn_point(spawn_id)
	if spawn_node == null:
		spawn_node = _find_spawn_point("default")

	if spawn_node and _player_node:
		_player_node.global_position = spawn_node.global_position
	elif _player_node:
		push_warning(
			"BaseLocation._position_player_at_spawn: No spawn point '%s' found in '%s'."
			% [spawn_id, location_id]
		)


func _find_spawn_point(spawn_id: String) -> Node:
	# Spawn points are expected to live under a "SpawnPoints" Node2D group node.
	if has_node("SpawnPoints/" + spawn_id):
		return get_node("SpawnPoints/" + spawn_id)
	# Also search by group tag as fallback.
	var tagged: Array = get_tree().get_nodes_in_group("spawn_" + spawn_id)
	if tagged.size() > 0:
		return tagged[0]
	return null


func _play_music() -> void:
	if music_track.is_empty():
		return
	if has_node("/root/AudioManager"):
		get_node("/root/AudioManager").play_music(music_track)
	else:
		push_warning("BaseLocation._play_music: AudioManager autoload not found.")


func _run_autosave() -> void:
	if has_node("/root/SaveManager"):
		get_node("/root/SaveManager").autosave()
	else:
		push_warning("BaseLocation._run_autosave: SaveManager autoload not found.")


func _mark_visited() -> void:
	if location_id.is_empty():
		return
	if has_node("/root/GameFlags"):
		get_node("/root/GameFlags").set_flag("visited_" + location_id, true)
