## surface_forest.gd
## Surface Forest – the first overworld area reached after escaping the warren.
## Kobold allies roam the forest paths leading toward Imperial City.
extends BaseLocation
class_name SurfaceForest

# ---------------------------------------------------------------------------
# Location constants
# ---------------------------------------------------------------------------
const LOCATION_ID: String = "surface_forest"
const MUSIC: String = "overworld"
const BATTLE_BG: String = "forest"

const ENCOUNTER_POOL: Array = ["wolf", "infected_kobold"]
const ENCOUNTER_RATE: float = 0.20

const ZONE_FOREST_PATH: Rect2 = Rect2(-640, -128, 1280, 256)
const ZONE_DEEP_BRUSH: Rect2 = Rect2(300, 128, 400, 200)

const NPC_KOBOLD_ALLY_ID: String = "kobold_ally"
const NPC_KOBOLD_ALLY_POSITION: Vector2 = Vector2(-200, 60)

const EXIT_TO_IMPERIAL_CITY: String = "imperial_city"
const SPAWN_FROM_FOREST_CITY: String = "from_forest"
const EXIT_TO_KOBOLD_VILLAGE: String = "kobold_village"
const SPAWN_FROM_FOREST_VILLAGE: String = "from_forest"

# ---------------------------------------------------------------------------
# Child node paths
# ---------------------------------------------------------------------------
@onready var exit_to_city_trigger: Area2D = $ExitToCityTrigger
@onready var exit_to_village_trigger: Area2D = $ExitToVillageTrigger

# ---------------------------------------------------------------------------
# _ready override
# ---------------------------------------------------------------------------
func _ready() -> void:
	location_id = LOCATION_ID
	music_track = MUSIC
	default_battle_background = BATTLE_BG

	if exit_to_city_trigger:
		exit_to_city_trigger.body_entered.connect(_on_exit_to_city_body_entered)

	if exit_to_village_trigger:
		exit_to_village_trigger.body_entered.connect(_on_exit_to_village_body_entered)

	super._ready()

	_setup_encounter_zones()
	_spawn_ally_npcs()

# ---------------------------------------------------------------------------
# Story triggers (override)
# ---------------------------------------------------------------------------
func handle_story_triggers() -> void:
	var flags = get_node_or_null("/root/GameFlags")
	if flags == null:
		push_warning("SurfaceForest.handle_story_triggers: GameFlags autoload missing.")
		return

	if not flags.get_flag("surface_forest_first_visit_done"):
		flags.set_flag("surface_forest_first_visit_done", true)
		emit_signal("story_trigger_fired", "surface_forest_first_visit")

# ---------------------------------------------------------------------------
# Private – encounter zones
# ---------------------------------------------------------------------------
func _setup_encounter_zones() -> void:
	spawn_encounter_zone(ZONE_FOREST_PATH, ENCOUNTER_RATE, ENCOUNTER_POOL, BATTLE_BG)
	spawn_encounter_zone(ZONE_DEEP_BRUSH, ENCOUNTER_RATE + 0.10, ENCOUNTER_POOL, BATTLE_BG)

# ---------------------------------------------------------------------------
# Private – NPCs
# ---------------------------------------------------------------------------
func _spawn_ally_npcs() -> void:
	var flags = get_node_or_null("/root/GameFlags")
	if flags and flags.get_flag("kobold_ally_npc_removed"):
		return
	add_npc(NPC_KOBOLD_ALLY_ID, NPC_KOBOLD_ALLY_POSITION)

# ---------------------------------------------------------------------------
# Signal callbacks
# ---------------------------------------------------------------------------
func _on_exit_to_city_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	go_to_location(EXIT_TO_IMPERIAL_CITY, SPAWN_FROM_FOREST_CITY)

func _on_exit_to_village_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	go_to_location(EXIT_TO_KOBOLD_VILLAGE, SPAWN_FROM_FOREST_VILLAGE)
