## slaver_island.gd
## Slaver Island – a post-credits bonus area accessible only after the best ending.
## A grim rescue mission that sets the "true_ending_complete" flag on completion.
extends BaseLocation
class_name SlaverIsland

# ---------------------------------------------------------------------------
# Location constants
# ---------------------------------------------------------------------------
const LOCATION_ID: String = "slaver_island"
const MUSIC: String = "grim"
const BATTLE_BG: String = "slaver_compound"

const ENCOUNTER_POOL: Array = ["slaver_guard", "mercenary", "undead_slave"]
const ENCOUNTER_RATE: float = 0.30

const ZONE_DOCKS: Rect2 = Rect2(-600, -112, 600, 224)
const ZONE_COMPOUND: Rect2 = Rect2(100, -128, 700, 256)
const ZONE_INNER_HOLD: Rect2 = Rect2(700, -96, 400, 192)

const NPC_ESCAPED_SLAVE_A_ID: String = "escaped_slave_a"
const NPC_ESCAPED_SLAVE_A_POSITION: Vector2 = Vector2(-300, 60)
const NPC_ESCAPED_SLAVE_B_ID: String = "escaped_slave_b"
const NPC_ESCAPED_SLAVE_B_POSITION: Vector2 = Vector2(-220, 80)
const NPC_ESCAPED_SLAVE_C_ID: String = "escaped_slave_c"
const NPC_ESCAPED_SLAVE_C_POSITION: Vector2 = Vector2(-260, 100)

# Number of slaves to rescue before the mission completes.
const SLAVES_TO_RESCUE: int = 3

# ---------------------------------------------------------------------------
# Child node paths
# ---------------------------------------------------------------------------
@onready var slave_rescue_trigger_a: Area2D = $SlaveRescueTriggerA
@onready var slave_rescue_trigger_b: Area2D = $SlaveRescueTriggerB
@onready var slave_rescue_trigger_c: Area2D = $SlaveRescueTriggerC
@onready var mission_complete_trigger: Area2D = $MissionCompleteTrigger

# ---------------------------------------------------------------------------
# _ready override
# ---------------------------------------------------------------------------
func _ready() -> void:
	location_id = LOCATION_ID
	music_track = MUSIC
	default_battle_background = BATTLE_BG

	if slave_rescue_trigger_a:
		slave_rescue_trigger_a.body_entered.connect(_on_rescue_trigger_body_entered.bind("slave_a"))

	if slave_rescue_trigger_b:
		slave_rescue_trigger_b.body_entered.connect(_on_rescue_trigger_body_entered.bind("slave_b"))

	if slave_rescue_trigger_c:
		slave_rescue_trigger_c.body_entered.connect(_on_rescue_trigger_body_entered.bind("slave_c"))

	if mission_complete_trigger:
		mission_complete_trigger.body_entered.connect(_on_mission_complete_trigger_body_entered)

	super._ready()

	_setup_encounter_zones()
	_spawn_escaped_slave_npcs()

# ---------------------------------------------------------------------------
# Story triggers (override)
# ---------------------------------------------------------------------------
func handle_story_triggers() -> void:
	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags == null:
		push_warning("SlaverIsland.handle_story_triggers: GameFlags autoload missing.")
		return

	# Guard – this area must only be reachable with the best ending flag.
	# SceneTransition should also enforce this, but we double-check here.
	if not flags.get_flag("best_ending"):
		push_warning("SlaverIsland.handle_story_triggers: Accessed without best_ending flag.")
		go_to_location("floating_island", "default")
		return

	# Restore already-rescued slave states.
	_restore_rescue_states(flags)

	# If mission already complete, disable encounter zones.
	if flags.get_flag("true_ending_complete"):
		for ez: Node in _encounter_zones:
			if ez.has_method("set_active"):
				ez.set_active(false)
		emit_signal("story_trigger_fired", "slaver_island_already_cleared")

	if not flags.get_flag("slaver_island_first_visit_done"):
		flags.set_flag("slaver_island_first_visit_done", true)
		emit_signal("story_trigger_fired", "slaver_island_first_visit")

# ---------------------------------------------------------------------------
# Private – encounter zones
# ---------------------------------------------------------------------------
func _setup_encounter_zones() -> void:
	spawn_encounter_zone(ZONE_DOCKS, ENCOUNTER_RATE, ENCOUNTER_POOL, BATTLE_BG)
	spawn_encounter_zone(ZONE_COMPOUND, ENCOUNTER_RATE + 0.08, ENCOUNTER_POOL, BATTLE_BG)
	spawn_encounter_zone(ZONE_INNER_HOLD, ENCOUNTER_RATE + 0.15, ENCOUNTER_POOL, BATTLE_BG)

# ---------------------------------------------------------------------------
# Private – NPC spawning
# ---------------------------------------------------------------------------
func _spawn_escaped_slave_npcs() -> void:
	var flags: Node = get_node_or_null("/root/GameFlags")

	if not (flags and flags.get_flag("slave_a_rescued")):
		add_npc(NPC_ESCAPED_SLAVE_A_ID, NPC_ESCAPED_SLAVE_A_POSITION)

	if not (flags and flags.get_flag("slave_b_rescued")):
		add_npc(NPC_ESCAPED_SLAVE_B_ID, NPC_ESCAPED_SLAVE_B_POSITION)

	if not (flags and flags.get_flag("slave_c_rescued")):
		add_npc(NPC_ESCAPED_SLAVE_C_ID, NPC_ESCAPED_SLAVE_C_POSITION)

func _restore_rescue_states(flags: Node) -> void:
	# Hide rescue triggers that have already been activated.
	if flags.get_flag("slave_a_rescued") and slave_rescue_trigger_a:
		slave_rescue_trigger_a.monitoring = false
	if flags.get_flag("slave_b_rescued") and slave_rescue_trigger_b:
		slave_rescue_trigger_b.monitoring = false
	if flags.get_flag("slave_c_rescued") and slave_rescue_trigger_c:
		slave_rescue_trigger_c.monitoring = false

func _count_rescued_slaves(flags: Node) -> int:
	var count: int = 0
	if flags.get_flag("slave_a_rescued"):
		count += 1
	if flags.get_flag("slave_b_rescued"):
		count += 1
	if flags.get_flag("slave_c_rescued"):
		count += 1
	return count

func _check_mission_complete(flags: Node) -> void:
	if _count_rescued_slaves(flags) >= SLAVES_TO_RESCUE:
		if not flags.get_flag("true_ending_complete"):
			flags.set_flag("true_ending_complete", true)
			emit_signal("story_trigger_fired", "true_ending_complete")
			# Unlock mission-complete trigger.
			if mission_complete_trigger:
				mission_complete_trigger.monitoring = true

# ---------------------------------------------------------------------------
# Signal callbacks
# ---------------------------------------------------------------------------
func _on_rescue_trigger_body_entered(body: Node, slave_id: String) -> void:
	if not body.is_in_group("player"):
		return
	var flags: Node = get_node_or_null("/root/GameFlags")
	var flag_key: String = slave_id + "_rescued"
	if flags and flags.get_flag(flag_key):
		return

	if flags:
		flags.set_flag(flag_key, true)
	emit_signal("story_trigger_fired", "rescued_" + slave_id)

	# Remove the corresponding slave NPC now that they are free.
	var npc_id_map: Dictionary = {
		"slave_a": NPC_ESCAPED_SLAVE_A_ID,
		"slave_b": NPC_ESCAPED_SLAVE_B_ID,
		"slave_c": NPC_ESCAPED_SLAVE_C_ID,
	}
	var npc_id: String = npc_id_map.get(slave_id, "")
	if npc_id and npc_id in _npc_nodes:
		var npc: Node = _npc_nodes[npc_id]
		if npc and npc.has_method("play_rescued_animation"):
			npc.play_rescued_animation()

	if flags:
		_check_mission_complete(flags)

func _on_mission_complete_trigger_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags and not flags.get_flag("true_ending_complete"):
		return
	# Fire the true ending credits / epilogue sequence.
	var ending_manager: Node = get_node_or_null("/root/EndingManager")
	if ending_manager and ending_manager.has_method("play_ending"):
		ending_manager.play_ending("true_ending_epilogue")
	emit_signal("story_trigger_fired", "true_ending_epilogue_started")
