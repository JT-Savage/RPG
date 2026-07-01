## catacomb_depths.gd
## Catacomb Depths – the lower level of the catacombs, home to the Catacomb Lich.
## Features a pressure-plate puzzle and Hannah's recruitment event.
extends BaseLocation
class_name CatacombDepths

# ---------------------------------------------------------------------------
# Location constants
# ---------------------------------------------------------------------------
const LOCATION_ID: String = "catacomb_depths"
const MUSIC: String = "dungeon_dark"
const BATTLE_BG: String = "catacomb"

const ENCOUNTER_POOL: Array = ["lich_minion", "bone_knight", "wraith"]
const ENCOUNTER_RATE: float = 0.32

const ZONE_LOWER_HALL: Rect2 = Rect2(-640, -112, 1280, 224)
const ZONE_LICH_ANTECHAMBER: Rect2 = Rect2(480, -96, 320, 192)

const NPC_HANNAH_ID: String = "hannah"
const NPC_HANNAH_POSITION: Vector2 = Vector2(-80, 48)

const BOSS_TRIGGER_POSITION: Vector2 = Vector2(740, 0)
const BOSS_TRIGGER_RECT: Rect2 = Rect2(680, -64, 128, 128)

const EXIT_TO_ENTRANCE: String = "catacomb_entrance"
const SPAWN_FROM_DEPTHS: String = "from_depths"
const EXIT_TO_SWAMP: String = "swamp_border"
const SPAWN_FROM_CATACOMB: String = "from_catacomb"

# ---------------------------------------------------------------------------
# Child node paths
# ---------------------------------------------------------------------------
@onready var exit_to_entrance_trigger: Area2D = $ExitToEntranceTrigger
@onready var exit_to_swamp_trigger: Area2D = $ExitToSwampTrigger
@onready var pressure_plate_puzzle = $PressurePlatePuzzle
@onready var boss_trigger: Area2D = $BossTrigger

# ---------------------------------------------------------------------------
# _ready override
# ---------------------------------------------------------------------------
func _ready() -> void:
	location_id = LOCATION_ID
	music_track = MUSIC
	default_battle_background = BATTLE_BG

	if exit_to_entrance_trigger:
		exit_to_entrance_trigger.body_entered.connect(_on_exit_to_entrance_body_entered)

	if exit_to_swamp_trigger:
		exit_to_swamp_trigger.body_entered.connect(_on_exit_to_swamp_body_entered)

	if boss_trigger:
		boss_trigger.body_entered.connect(_on_boss_trigger_body_entered)

	if pressure_plate_puzzle and pressure_plate_puzzle.has_signal("puzzle_solved"):
		pressure_plate_puzzle.puzzle_solved.connect(_on_pressure_plate_puzzle_solved)

	super._ready()

	_setup_encounter_zones()

# ---------------------------------------------------------------------------
# Story triggers (override)
# ---------------------------------------------------------------------------
func handle_story_triggers() -> void:
	var flags = get_node_or_null("/root/GameFlags")
	if flags == null:
		push_warning("CatacombDepths.handle_story_triggers: GameFlags autoload missing.")
		return

	# Hannah recruitment – she is found trapped in the depths.
	if not flags.get_flag("hannah_recruited"):
		_spawn_hannah_for_recruitment()

	# Restore pressure plate state if puzzle was already solved.
	if flags.get_flag("pressure_plate_puzzle_solved"):
		_apply_puzzle_solved_state()

	# Lock swamp exit until the lich is defeated.
	if exit_to_swamp_trigger:
		exit_to_swamp_trigger.monitoring = flags.get_flag("catacomb_lich_defeated")

	if not flags.get_flag("catacomb_depths_first_visit_done"):
		flags.set_flag("catacomb_depths_first_visit_done", true)
		emit_signal("story_trigger_fired", "catacomb_depths_first_visit")

# ---------------------------------------------------------------------------
# Private – encounter zones
# ---------------------------------------------------------------------------
func _setup_encounter_zones() -> void:
	spawn_encounter_zone(ZONE_LOWER_HALL, ENCOUNTER_RATE, ENCOUNTER_POOL, BATTLE_BG)
	spawn_encounter_zone(ZONE_LICH_ANTECHAMBER, ENCOUNTER_RATE + 0.10, ENCOUNTER_POOL, BATTLE_BG)

# ---------------------------------------------------------------------------
# Private – story helpers
# ---------------------------------------------------------------------------
func _spawn_hannah_for_recruitment() -> void:
	var hannah: Node = add_npc(NPC_HANNAH_ID, NPC_HANNAH_POSITION)
	if hannah and hannah.has_method("play_cutscene"):
		hannah.set_meta("cutscene_id", "hannah_recruitment")
		hannah.set_meta("trigger_proximity", 88.0)
		hannah.set_meta("on_recruit_flag", "hannah_recruited")

func _apply_puzzle_solved_state() -> void:
	if pressure_plate_puzzle and pressure_plate_puzzle.has_method("set_solved"):
		pressure_plate_puzzle.set_solved(true)

# ---------------------------------------------------------------------------
# Signal callbacks
# ---------------------------------------------------------------------------
func _on_exit_to_entrance_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	go_to_location(EXIT_TO_ENTRANCE, SPAWN_FROM_DEPTHS)

func _on_exit_to_swamp_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	var flags = get_node_or_null("/root/GameFlags")
	if flags and not flags.get_flag("catacomb_lich_defeated"):
		# Silently block; the puzzle/boss gate should communicate this visually.
		return
	go_to_location(EXIT_TO_SWAMP, SPAWN_FROM_CATACOMB)

func _on_boss_trigger_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	var flags = get_node_or_null("/root/GameFlags")
	if flags and flags.get_flag("catacomb_lich_defeated"):
		return
	# Initiate boss battle.
	var battle_manager = get_node_or_null("/root/BattleManager")
	if battle_manager and battle_manager.has_method("start_boss_battle"):
		battle_manager.start_boss_battle("catacomb_lich", BATTLE_BG)
		if battle_manager.has_signal("battle_won"):
			if not battle_manager.battle_won.is_connected(_on_catacomb_lich_defeated):
				battle_manager.battle_won.connect(_on_catacomb_lich_defeated, CONNECT_ONE_SHOT)

func _on_catacomb_lich_defeated() -> void:
	var flags = get_node_or_null("/root/GameFlags")
	if flags:
		flags.set_flag("catacomb_lich_defeated", true)
	if exit_to_swamp_trigger:
		exit_to_swamp_trigger.monitoring = true
	emit_signal("story_trigger_fired", "catacomb_lich_defeated")

func _on_pressure_plate_puzzle_solved() -> void:
	var flags = get_node_or_null("/root/GameFlags")
	if flags:
		flags.set_flag("pressure_plate_puzzle_solved", true)
	emit_signal("story_trigger_fired", "pressure_plate_puzzle_solved")
