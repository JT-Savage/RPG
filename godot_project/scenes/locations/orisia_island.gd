## orisia_island.gd
## Orisia's Island – the critical story decision point of the game.
## A serene, beautiful island where the ancient being Orisia resides.
## No enemies. Houses the recruitment deadline and class evolution unlocks.
extends BaseLocation
class_name OrisiaIsland

# ---------------------------------------------------------------------------
# Location constants
# ---------------------------------------------------------------------------
const LOCATION_ID: String = "orisia_island"
const MUSIC: String = "orisia_theme"
const BATTLE_BG: String = ""        # No battles on this island

const ENCOUNTER_POOL: Array = []
const ENCOUNTER_RATE: float = 0.0

const NPC_ORISIA_ID: String = "orisia"
const NPC_ORISIA_POSITION: Vector2 = Vector2(0, -80)

const EXIT_TO_FLOATING_ISLAND: String = "floating_island"
const SPAWN_FROM_ORISIA: String = "from_orisia"

# Party members who unlock class evolutions upon completing their sidequests.
const CLASS_EVOLUTION_FLAGS: Dictionary = {
	"michael_sidequest_done": "michael_class_evolved",
	"fei_sidequest_done": "fei_class_evolved",
	"hannah_sidequest_done": "hannah_class_evolved",
	"druidess_sidequest_done": "druidess_class_evolved",
	"dreamwalker_sidequest_done": "dreamwalker_class_evolved",
	"iris_sidequest_done": "iris_class_evolved",
	"vampire_sidequest_done": "vampire_class_evolved",
	"fritzzit_sidequest_done": "fritzzit_class_evolved",
	"crankpot_sidequest_done": "crankpot_class_evolved",
}

# ---------------------------------------------------------------------------
# Child node paths
# ---------------------------------------------------------------------------
@onready var exit_trigger: Area2D = $ExitTrigger
@onready var orisia_meeting_zone: Area2D = $OrisiaMeetingZone

# ---------------------------------------------------------------------------
# _ready override
# ---------------------------------------------------------------------------
func _ready() -> void:
	location_id = LOCATION_ID
	music_track = MUSIC
	default_battle_background = BATTLE_BG

	if exit_trigger:
		exit_trigger.body_entered.connect(_on_exit_trigger_body_entered)

	if orisia_meeting_zone:
		orisia_meeting_zone.body_entered.connect(_on_orisia_meeting_zone_body_entered)

	super._ready()

	_spawn_orisia()

# ---------------------------------------------------------------------------
# Story triggers (override)
# ---------------------------------------------------------------------------
func handle_story_triggers() -> void:
	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags == null:
		push_warning("OrisiaIsland.handle_story_triggers: GameFlags autoload missing.")
		return

	# Apply class evolutions for party members who completed sidequests.
	_check_class_evolutions(flags)

	if not flags.get_flag("orisia_island_first_visit_done"):
		flags.set_flag("orisia_island_first_visit_done", true)
		emit_signal("story_trigger_fired", "orisia_island_first_visit")

# ---------------------------------------------------------------------------
# Private – story helpers
# ---------------------------------------------------------------------------
func _spawn_orisia() -> void:
	var orisia: Node = add_npc(NPC_ORISIA_ID, NPC_ORISIA_POSITION)
	if orisia:
		# Orisia's NPC script handles the branching dialogue internally;
		# we pass context so it knows whether the meeting has already occurred.
		var flags: Node = get_node_or_null("/root/GameFlags")
		if orisia.has_method("set_meeting_state"):
			var already_met: bool = flags != null and flags.get_flag("orisia_meeting_done")
			orisia.set_meeting_state(already_met)

func _check_class_evolutions(flags: Node) -> void:
	var party_manager: Node = get_node_or_null("/root/PartyManager")
	for sidequest_flag: String in CLASS_EVOLUTION_FLAGS:
		var evolution_flag: String = CLASS_EVOLUTION_FLAGS[sidequest_flag]
		if flags.get_flag(sidequest_flag) and not flags.get_flag(evolution_flag):
			flags.set_flag(evolution_flag, true)
			if party_manager and party_manager.has_method("apply_class_evolution"):
				# Derive character id from evolution flag name (e.g. "michael_class_evolved" -> "michael").
				var character_id: String = evolution_flag.split("_class_evolved")[0]
				party_manager.apply_class_evolution(character_id)
			emit_signal("story_trigger_fired", "class_evolution_" + evolution_flag)

func _trigger_orisia_meeting(player: Node) -> void:
	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags and flags.get_flag("orisia_meeting_done"):
		return

	var orisia: Node = _npc_nodes.get(NPC_ORISIA_ID)
	if orisia and orisia.has_method("play_cutscene"):
		orisia.play_cutscene("orisia_meeting")
		# The cutscene script is responsible for setting orisia_meeting_done
		# and recruitment_deadline_accepted / rejected based on player choice.
		if orisia.has_signal("cutscene_finished"):
			if not orisia.cutscene_finished.is_connected(_on_orisia_meeting_finished):
				orisia.cutscene_finished.connect(_on_orisia_meeting_finished, CONNECT_ONE_SHOT)

func _on_orisia_meeting_finished(choice: String) -> void:
	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags:
		flags.set_flag("orisia_meeting_done", true)
		if choice == "yes":
			flags.set_flag("orisia_side_accepted", true)
			emit_signal("story_trigger_fired", "orisia_recruitment_accepted")
		else:
			flags.set_flag("orisia_side_rejected", true)
			emit_signal("story_trigger_fired", "orisia_recruitment_rejected")

# ---------------------------------------------------------------------------
# Signal callbacks
# ---------------------------------------------------------------------------
func _on_exit_trigger_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	go_to_location(EXIT_TO_FLOATING_ISLAND, SPAWN_FROM_ORISIA)

func _on_orisia_meeting_zone_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	_trigger_orisia_meeting(body)
