## catacomb_entrance.gd
## Catacomb Entrance – the first dungeon reached after Imperial City.
## Spooky, decayed corridors haunted by undead. Contains a save point.
extends BaseLocation
class_name CatacombEntrance

# ---------------------------------------------------------------------------
# Location constants
# ---------------------------------------------------------------------------
const LOCATION_ID: String = "catacomb_entrance"
const MUSIC: String = "dungeon_dark"
const BATTLE_BG: String = "catacomb"

const ENCOUNTER_POOL: Array = ["skeleton", "zombie", "ghost"]
const ENCOUNTER_RATE: float = 0.28

const ZONE_ENTRY_HALL: Rect2 = Rect2(-512, -96, 1024, 192)
const ZONE_SIDE_CRYPT: Rect2 = Rect2(280, 96, 360, 180)

const SAVE_POINT_SPAWN: Vector2 = Vector2(-440, 0)

const EXIT_TO_DEPTHS: String = "catacomb_depths"
const SPAWN_FROM_ENTRANCE: String = "from_entrance"
const EXIT_TO_IMPERIAL_CITY: String = "imperial_city"
const SPAWN_FROM_CATACOMB: String = "from_catacomb"

# ---------------------------------------------------------------------------
# Child node paths
# ---------------------------------------------------------------------------
@onready var exit_to_depths_trigger: Area2D = $ExitToDepthsTrigger
@onready var exit_to_city_trigger: Area2D = $ExitToCityTrigger
@onready var save_point_marker: Marker2D = $SavePointMarker

# ---------------------------------------------------------------------------
# _ready override
# ---------------------------------------------------------------------------
func _ready() -> void:
	location_id = LOCATION_ID
	music_track = MUSIC
	default_battle_background = BATTLE_BG

	if exit_to_depths_trigger:
		exit_to_depths_trigger.body_entered.connect(_on_exit_to_depths_body_entered)

	if exit_to_city_trigger:
		exit_to_city_trigger.body_entered.connect(_on_exit_to_city_body_entered)

	super._ready()

	_setup_encounter_zones()
	_setup_save_point()

# ---------------------------------------------------------------------------
# Story triggers (override)
# ---------------------------------------------------------------------------
func handle_story_triggers() -> void:
	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags == null:
		push_warning("CatacombEntrance.handle_story_triggers: GameFlags autoload missing.")
		return

	if not flags.get_flag("catacomb_entrance_first_visit_done"):
		flags.set_flag("catacomb_entrance_first_visit_done", true)
		emit_signal("story_trigger_fired", "catacomb_entrance_first_visit")

# ---------------------------------------------------------------------------
# Private – encounter zones
# ---------------------------------------------------------------------------
func _setup_encounter_zones() -> void:
	spawn_encounter_zone(ZONE_ENTRY_HALL, ENCOUNTER_RATE, ENCOUNTER_POOL, BATTLE_BG)
	spawn_encounter_zone(ZONE_SIDE_CRYPT, ENCOUNTER_RATE + 0.08, ENCOUNTER_POOL, BATTLE_BG)

# ---------------------------------------------------------------------------
# Private – save point
# ---------------------------------------------------------------------------
func _setup_save_point() -> void:
	var sp_scene: PackedScene = load(SAVE_POINT_SCENE_PATH)
	if sp_scene == null:
		push_error("CatacombEntrance._setup_save_point: Could not load save point scene.")
		return

	_save_point_node = sp_scene.instantiate()
	_save_point_node.name = "SavePoint"
	add_child(_save_point_node)

	if save_point_marker:
		_save_point_node.global_position = save_point_marker.global_position
	else:
		_save_point_node.global_position = SAVE_POINT_SPAWN

	if _save_point_node.has_signal("save_requested"):
		_save_point_node.save_requested.connect(show_save_point)

# ---------------------------------------------------------------------------
# Signal callbacks
# ---------------------------------------------------------------------------
func _on_exit_to_depths_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	go_to_location(EXIT_TO_DEPTHS, SPAWN_FROM_ENTRANCE)

func _on_exit_to_city_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	go_to_location(EXIT_TO_IMPERIAL_CITY, SPAWN_FROM_CATACOMB)
