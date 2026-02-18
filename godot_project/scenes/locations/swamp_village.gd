## swamp_village.gd
## Swamp Village – a murky settlement where the Druidess makes her home.
## Enemies appear only outside the village boundary; the village core is safe.
extends BaseLocation
class_name SwampVillage

# ---------------------------------------------------------------------------
# Location constants
# ---------------------------------------------------------------------------
const LOCATION_ID: String = "swamp_village"
const MUSIC: String = "swamp"
const BATTLE_BG: String = "swamp"

const ENCOUNTER_POOL: Array = ["swamp_beast", "poison_frog"]
const ENCOUNTER_RATE: float = 0.25

# Encounter zone is placed in the outer swamp, away from the village centre.
const ZONE_OUTER_SWAMP: Rect2 = Rect2(-800, -160, 600, 320)
const ZONE_FAR_MARSH: Rect2 = Rect2(500, -128, 400, 256)

const NPC_DRUIDESS_ELDER_ID: String = "druidess_elder"
const NPC_DRUIDESS_ELDER_POSITION: Vector2 = Vector2(60, -80)

const NPC_DRUIDESS_ID: String = "druidess"
const NPC_DRUIDESS_POSITION: Vector2 = Vector2(-40, 30)

const EXIT_TO_CATACOMB: String = "catacomb_depths"
const SPAWN_FROM_SWAMP: String = "from_swamp"
const EXIT_TO_MOUNTAIN: String = "mountain_pass"
const SPAWN_FROM_SWAMP_MOUNTAIN: String = "from_swamp"

# ---------------------------------------------------------------------------
# Child node paths
# ---------------------------------------------------------------------------
@onready var exit_to_catacomb_trigger: Area2D = $ExitToCatacombTrigger
@onready var exit_to_mountain_trigger: Area2D = $ExitToMountainTrigger

# ---------------------------------------------------------------------------
# _ready override
# ---------------------------------------------------------------------------
func _ready() -> void:
	location_id = LOCATION_ID
	music_track = MUSIC
	default_battle_background = BATTLE_BG

	if exit_to_catacomb_trigger:
		exit_to_catacomb_trigger.body_entered.connect(_on_exit_to_catacomb_body_entered)

	if exit_to_mountain_trigger:
		exit_to_mountain_trigger.body_entered.connect(_on_exit_to_mountain_body_entered)

	super._ready()

	_setup_encounter_zones()
	_spawn_village_npcs()

# ---------------------------------------------------------------------------
# Story triggers (override)
# ---------------------------------------------------------------------------
func handle_story_triggers() -> void:
	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags == null:
		push_warning("SwampVillage.handle_story_triggers: GameFlags autoload missing.")
		return

	# Druidess recruitment event.
	if not flags.get_flag("druidess_recruited"):
		_trigger_druidess_recruitment()

	if not flags.get_flag("swamp_village_first_visit_done"):
		flags.set_flag("swamp_village_first_visit_done", true)
		emit_signal("story_trigger_fired", "swamp_village_first_visit")

# ---------------------------------------------------------------------------
# Private – encounter zones (outer swamp only)
# ---------------------------------------------------------------------------
func _setup_encounter_zones() -> void:
	spawn_encounter_zone(ZONE_OUTER_SWAMP, ENCOUNTER_RATE, ENCOUNTER_POOL, BATTLE_BG)
	spawn_encounter_zone(ZONE_FAR_MARSH, ENCOUNTER_RATE + 0.08, ENCOUNTER_POOL, BATTLE_BG)

# ---------------------------------------------------------------------------
# Private – NPCs
# ---------------------------------------------------------------------------
func _spawn_village_npcs() -> void:
	add_npc(NPC_DRUIDESS_ELDER_ID, NPC_DRUIDESS_ELDER_POSITION)

func _trigger_druidess_recruitment() -> void:
	var druidess: Node = add_npc(NPC_DRUIDESS_ID, NPC_DRUIDESS_POSITION)
	if druidess and druidess.has_method("play_cutscene"):
		druidess.set_meta("cutscene_id", "druidess_recruitment")
		druidess.set_meta("trigger_proximity", 100.0)
		druidess.set_meta("on_recruit_flag", "druidess_recruited")

# ---------------------------------------------------------------------------
# Signal callbacks
# ---------------------------------------------------------------------------
func _on_exit_to_catacomb_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	go_to_location(EXIT_TO_CATACOMB, SPAWN_FROM_SWAMP)

func _on_exit_to_mountain_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	go_to_location(EXIT_TO_MOUNTAIN, SPAWN_FROM_SWAMP_MOUNTAIN)
