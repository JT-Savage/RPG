## mountain_pass.gd
## Mountain Pass – a treacherous snow-covered path leading to the Floating Island.
## Yipp the kobold may randomly spawn here as one of their possible appearances.
extends BaseLocation
class_name MountainPass

# ---------------------------------------------------------------------------
# Location constants
# ---------------------------------------------------------------------------
const LOCATION_ID: String = "mountain_pass"
const MUSIC: String = "mountain"
const BATTLE_BG: String = "mountain"

const ENCOUNTER_POOL: Array = ["mountain_troll", "ice_witch"]
const ENCOUNTER_RATE: float = 0.27

const ZONE_LOWER_PASS: Rect2 = Rect2(-700, -128, 900, 256)
const ZONE_UPPER_CLIFFS: Rect2 = Rect2(300, -160, 500, 320)

# Yipp random spawn chance on entering this location (evaluated once per visit).
const YIPP_SPAWN_CHANCE: float = 0.33
const NPC_YIPP_ID: String = "yipp"
const NPC_YIPP_POSITION: Vector2 = Vector2(180, -60)

const EXIT_TO_SWAMP: String = "swamp_village"
const SPAWN_FROM_MOUNTAIN: String = "from_mountain"
const EXIT_TO_FLOATING_ISLAND: String = "floating_island_entrance"
const SPAWN_FROM_MOUNTAIN_TOP: String = "from_mountain"

# ---------------------------------------------------------------------------
# Child node paths
# ---------------------------------------------------------------------------
@onready var exit_to_swamp_trigger: Area2D = $ExitToSwampTrigger
@onready var exit_to_island_trigger: Area2D = $ExitToIslandTrigger
@onready var snow_weather_effect: Node = $SnowWeatherEffect

# ---------------------------------------------------------------------------
# _ready override
# ---------------------------------------------------------------------------
func _ready() -> void:
	location_id = LOCATION_ID
	music_track = MUSIC
	default_battle_background = BATTLE_BG

	if exit_to_swamp_trigger:
		exit_to_swamp_trigger.body_entered.connect(_on_exit_to_swamp_body_entered)

	if exit_to_island_trigger:
		exit_to_island_trigger.body_entered.connect(_on_exit_to_island_body_entered)

	super._ready()

	_setup_encounter_zones()
	_enable_snow_effect()
	_maybe_spawn_yipp()

# ---------------------------------------------------------------------------
# Story triggers (override)
# ---------------------------------------------------------------------------
func handle_story_triggers() -> void:
	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags == null:
		push_warning("MountainPass.handle_story_triggers: GameFlags autoload missing.")
		return

	if not flags.get_flag("mountain_pass_first_visit_done"):
		flags.set_flag("mountain_pass_first_visit_done", true)
		emit_signal("story_trigger_fired", "mountain_pass_first_visit")

# ---------------------------------------------------------------------------
# Private – encounter zones
# ---------------------------------------------------------------------------
func _setup_encounter_zones() -> void:
	spawn_encounter_zone(ZONE_LOWER_PASS, ENCOUNTER_RATE, ENCOUNTER_POOL, BATTLE_BG)
	spawn_encounter_zone(ZONE_UPPER_CLIFFS, ENCOUNTER_RATE + 0.08, ENCOUNTER_POOL, BATTLE_BG)

# ---------------------------------------------------------------------------
# Private – weather effect
# ---------------------------------------------------------------------------
func _enable_snow_effect() -> void:
	if snow_weather_effect and snow_weather_effect.has_method("start"):
		snow_weather_effect.start()
	elif snow_weather_effect:
		snow_weather_effect.visible = true

# ---------------------------------------------------------------------------
# Private – Yipp random encounter
# ---------------------------------------------------------------------------
func _maybe_spawn_yipp() -> void:
	var flags: Node = get_node_or_null("/root/GameFlags")
	# Don't spawn if already recruited or if Yipp already appeared here this cycle.
	if flags and (flags.get_flag("yipp_recruited") or flags.get_flag("yipp_seen_mountain")):
		return

	if randf() <= YIPP_SPAWN_CHANCE:
		var yipp: Node = add_npc(NPC_YIPP_ID, NPC_YIPP_POSITION)
		if yipp and yipp.has_method("play_cutscene"):
			yipp.set_meta("cutscene_id", "yipp_random_encounter")
			yipp.set_meta("on_recruit_flag", "yipp_recruited")
		if flags:
			flags.set_flag("yipp_seen_mountain", true)
			emit_signal("story_trigger_fired", "yipp_mountain_spawn")

# ---------------------------------------------------------------------------
# Signal callbacks
# ---------------------------------------------------------------------------
func _on_exit_to_swamp_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	go_to_location(EXIT_TO_SWAMP, SPAWN_FROM_MOUNTAIN)

func _on_exit_to_island_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	go_to_location(EXIT_TO_FLOATING_ISLAND, SPAWN_FROM_MOUNTAIN_TOP)
