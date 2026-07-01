## army_camp.gd
## The Army Camp – the final staging area before entering Orisia.
## Last chance for party recruitment and the point of no return cutscene.
## Orisia herself appears here to brief the party and assign sidequests.
extends BaseLocation
class_name ArmyCamp

# ---------------------------------------------------------------------------
# Location constants
# ---------------------------------------------------------------------------
const LOCATION_ID: String = "army_camp"
const MUSIC: String = "town"

# No random encounters inside the camp perimeter.

# ---------------------------------------------------------------------------
# NPC identifiers and spawn positions
# ---------------------------------------------------------------------------
## Primary story NPC.
const NPC_ORISIA: String   = "orisia"

## Backup spawns for characters not yet recruited.
## These NPCs appear *only* if the player missed them earlier.
const NPC_COOKIE: String   = "cookie"
const NPC_IRIS: String     = "iris"
const NPC_FRITZZIT: String = "fritzzit"
const NPC_CRANKPOT: String = "crankpot"

const NPC_SPAWNS: Dictionary = {
	"orisia":   Vector2(0,    -80),
	"cookie":   Vector2(-200,  32),
	"iris":     Vector2(-280,  32),
	"fritzzit": Vector2( 200,  48),
	"crankpot": Vector2( 260,  48),
}

# Exit toward Orisia – the point-of-no-return gate.
const EXIT_TO_ORISIA_DESTINATION: String = "orisia_region"
const EXIT_TO_ORISIA_SPAWN: String = "camp_entrance"

# Return path to the desert (allowed until recruitment_deadline_passed).
const EXIT_TO_DESERT_DESTINATION: String = "desert_region"
const EXIT_TO_DESERT_SPAWN: String = "from_army_camp"

# ---------------------------------------------------------------------------
# @onready child nodes
# ---------------------------------------------------------------------------
@onready var orisia_gate_trigger: Area2D = $Gates/OrisiaTrigger
@onready var desert_exit_trigger: Area2D = $Gates/DesertExitTrigger
@onready var point_of_no_return_prompt = $UI/PointOfNoReturnPrompt


# ---------------------------------------------------------------------------
# _ready override
# ---------------------------------------------------------------------------
func _ready() -> void:
	location_id = LOCATION_ID
	music_track  = MUSIC
	default_battle_background = ""   # No encounters.

	_connect_exit_triggers()

	super._ready()

	_spawn_camp_npcs()


# ---------------------------------------------------------------------------
# Story triggers (override)
# ---------------------------------------------------------------------------
func handle_story_triggers() -> void:
	var flags = get_node_or_null("/root/GameFlags")
	if flags == null:
		push_warning("ArmyCamp.handle_story_triggers: GameFlags autoload missing.")
		return

	# ------------------------------------------------------------------
	# Trigger: Orisia's first meeting – sets orisia_met flag.
	# ------------------------------------------------------------------
	if not flags.get_flag("orisia_met"):
		_trigger_orisia_first_meeting()
	else:
		# Orisia is present but greets the party more briefly.
		_enable_orisia_repeat_greeting()

	# ------------------------------------------------------------------
	# Backup recruitments – Cookie, Iris, Fritzzit+Crankpot.
	# These only appear if the deadline hasn't passed AND the character
	# was not picked up in their primary location.
	# ------------------------------------------------------------------
	if not flags.get_flag("recruitment_deadline_passed"):
		_handle_backup_recruitments(flags)

	emit_signal("story_trigger_fired", "army_camp_triggers_checked")


# ---------------------------------------------------------------------------
# Private – NPC spawning
# ---------------------------------------------------------------------------
func _spawn_camp_npcs() -> void:
	# Orisia is always placed; her dialogue state varies.
	add_npc(NPC_ORISIA, NPC_SPAWNS[NPC_ORISIA])


## Conditionally spawn backup NPCs if the player has not yet recruited them.
func _handle_backup_recruitments(flags: Node) -> void:
	# Cookie
	if not flags.get_flag("cookie_recruited"):
		var cookie = add_npc(NPC_COOKIE, NPC_SPAWNS[NPC_COOKIE])
		if cookie and cookie.has_method("set_dialogue"):
			cookie.set_dialogue("cookie_backup_recruitment")
		emit_signal("story_trigger_fired", "cookie_backup_spawn")

	# Iris
	if not flags.get_flag("iris_recruited"):
		var iris = add_npc(NPC_IRIS, NPC_SPAWNS[NPC_IRIS])
		if iris and iris.has_method("set_dialogue"):
			iris.set_dialogue("iris_backup_recruitment")
		emit_signal("story_trigger_fired", "iris_backup_spawn")

	# Fritzzit & Crankpot (they always come as a pair)
	if not flags.get_flag("fritzzit_recruited"):
		var fritzzit = add_npc(NPC_FRITZZIT, NPC_SPAWNS[NPC_FRITZZIT])
		var crankpot = add_npc(NPC_CRANKPOT, NPC_SPAWNS[NPC_CRANKPOT])
		if fritzzit and fritzzit.has_method("set_dialogue"):
			fritzzit.set_dialogue("fritzzit_backup_recruitment")
		if crankpot and crankpot.has_method("set_dialogue"):
			crankpot.set_dialogue("crankpot_backup_recruitment")
		emit_signal("story_trigger_fired", "fritzzit_backup_spawn")


# ---------------------------------------------------------------------------
# Private – Orisia meeting
# ---------------------------------------------------------------------------
func _trigger_orisia_first_meeting() -> void:
	var orisia = _npc_nodes.get(NPC_ORISIA)
	if orisia == null:
		push_warning("ArmyCamp._trigger_orisia_first_meeting: Orisia NPC not found.")
		return

	if orisia.has_method("set_dialogue"):
		orisia.set_dialogue("orisia_meeting")

	# Auto-play the meeting cutscene on scene entry.
	if orisia.has_method("play_cutscene"):
		orisia.play_cutscene("orisia_meeting")

	var flags = get_node_or_null("/root/GameFlags")
	if flags:
		flags.set_flag("orisia_met", true)

	emit_signal("story_trigger_fired", "orisia_first_meeting")


func _enable_orisia_repeat_greeting() -> void:
	var orisia = _npc_nodes.get(NPC_ORISIA)
	if orisia and orisia.has_method("set_dialogue"):
		orisia.set_dialogue("orisia_repeat_greeting")


# ---------------------------------------------------------------------------
# Private – exit triggers
# ---------------------------------------------------------------------------
func _connect_exit_triggers() -> void:
	if orisia_gate_trigger and orisia_gate_trigger.has_signal("body_entered"):
		orisia_gate_trigger.body_entered.connect(_on_orisia_gate_entered)

	if desert_exit_trigger and desert_exit_trigger.has_signal("body_entered"):
		desert_exit_trigger.body_entered.connect(_on_desert_exit_entered)


func _on_orisia_gate_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return

	var flags = get_node_or_null("/root/GameFlags")

	# The gate only opens after Orisia's briefing is complete and the player
	# confirms the point-of-no-return prompt from orisia_meeting dialogue.
	if flags and not flags.get_flag("recruitment_deadline_passed"):
		_show_point_of_no_return_prompt()
		return

	go_to_location(EXIT_TO_ORISIA_DESTINATION, EXIT_TO_ORISIA_SPAWN)


func _show_point_of_no_return_prompt() -> void:
	# The prompt is managed by the orisia_meeting dialogue (DialogueManager will
	# present it), but if the player walks to the gate manually, we force it.
	if point_of_no_return_prompt and point_of_no_return_prompt.has_method("show"):
		point_of_no_return_prompt.show()
	else:
		# Fallback: start the dialogue directly.
		var dm = get_node_or_null("/root/DialogueManager")
		if dm and dm.has_method("start_dialogue"):
			dm.start_dialogue("orisia_meeting", "point_of_no_return_label")


func _on_desert_exit_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return

	var flags = get_node_or_null("/root/GameFlags")
	if flags and flags.get_flag("recruitment_deadline_passed"):
		var notify = get_node_or_null("/root/NotificationManager")
		if notify and notify.has_method("show_message"):
			notify.show_message(
				"You have already committed to the march on Orisia. "
				+ "The path behind you is sealed."
			)
		return

	go_to_location(EXIT_TO_DESERT_DESTINATION, EXIT_TO_DESERT_SPAWN)
