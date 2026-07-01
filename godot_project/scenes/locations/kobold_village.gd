## kobold_village.gd
## Kobold Village – a refugee settlement of displaced kobolds.
## Safe zone: no random encounters. Michael recruitment cutscene fires here.
extends BaseLocation
class_name KoboldVillage

# ---------------------------------------------------------------------------
# Location constants
# ---------------------------------------------------------------------------
const LOCATION_ID: String = "kobold_village"
const MUSIC: String = "village"
const BATTLE_BG: String = ""        # No battles in this location

const ENCOUNTER_POOL: Array = []
const ENCOUNTER_RATE: float = 0.0

const NPC_ELDER_ID: String = "kobold_elder"
const NPC_ELDER_POSITION: Vector2 = Vector2(0, -60)
const NPC_CHILDREN_ID: String = "kobold_children"
const NPC_CHILDREN_POSITION: Vector2 = Vector2(120, 80)

const NPC_MICHAEL_ID: String = "michael"
const NPC_MICHAEL_POSITION: Vector2 = Vector2(-180, 40)

const EXIT_TO_SURFACE_FOREST: String = "surface_forest"
const SPAWN_FROM_VILLAGE: String = "from_village"

# ---------------------------------------------------------------------------
# Child node paths
# ---------------------------------------------------------------------------
@onready var exit_trigger: Area2D = $ExitTrigger

# ---------------------------------------------------------------------------
# _ready override
# ---------------------------------------------------------------------------
func _ready() -> void:
	location_id = LOCATION_ID
	music_track = MUSIC
	default_battle_background = BATTLE_BG

	if exit_trigger:
		exit_trigger.body_entered.connect(_on_exit_trigger_body_entered)

	super._ready()

	_spawn_village_npcs()

# ---------------------------------------------------------------------------
# Story triggers (override)
# ---------------------------------------------------------------------------
func handle_story_triggers() -> void:
	var flags = get_node_or_null("/root/GameFlags")
	if flags == null:
		push_warning("KoboldVillage.handle_story_triggers: GameFlags autoload missing.")
		return

	# Michael recruitment cutscene fires if he has not yet joined the party.
	if not flags.get_flag("michael_recruited"):
		_spawn_michael_for_recruitment()

	if not flags.get_flag("kobold_village_first_visit_done"):
		flags.set_flag("kobold_village_first_visit_done", true)
		emit_signal("story_trigger_fired", "kobold_village_first_visit")

# ---------------------------------------------------------------------------
# Private – NPC spawning
# ---------------------------------------------------------------------------
func _spawn_village_npcs() -> void:
	add_npc(NPC_ELDER_ID, NPC_ELDER_POSITION)
	add_npc(NPC_CHILDREN_ID, NPC_CHILDREN_POSITION)

func _spawn_michael_for_recruitment() -> void:
	var michael: Node = add_npc(NPC_MICHAEL_ID, NPC_MICHAEL_POSITION)
	if michael and michael.has_method("play_cutscene"):
		michael.set_meta("cutscene_id", "michael_recruitment")
		michael.set_meta("trigger_proximity", 96.0)
		michael.set_meta("on_recruit_flag", "michael_recruited")

# ---------------------------------------------------------------------------
# Signal callbacks
# ---------------------------------------------------------------------------
func _on_exit_trigger_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	go_to_location(EXIT_TO_SURFACE_FOREST, SPAWN_FROM_VILLAGE)
