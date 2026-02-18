## final_dungeon.gd
## The Void Spire – the final dungeon of "There Will Be Kobolds".
## Multi-floor structure navigated via teleporter triggers. Story-flag-checked
## ending sequences fire after the final boss is defeated on the top floor.
extends BaseLocation
class_name FinalDungeon

# ---------------------------------------------------------------------------
# Location constants
# ---------------------------------------------------------------------------
const LOCATION_ID: String = "final_dungeon"
const MUSIC: String = "final_dungeon"
const BATTLE_BG: String = "void_spire"

const ENCOUNTER_POOL: Array = ["void_knight", "shadow_dragon", "corrupted_saint"]
const ENCOUNTER_RATE: float = 0.35

# Encounter zones per floor.
const ZONE_FLOOR_1: Rect2 = Rect2(-640, -128, 1280, 256)
const ZONE_FLOOR_2: Rect2 = Rect2(-640, -1408, 1280, 256)
const ZONE_FLOOR_3: Rect2 = Rect2(-640, -2688, 1280, 256)

# Teleporter world positions (each leads one floor up).
const TELEPORTER_1_POSITION: Vector2 = Vector2(560, 0)
const TELEPORTER_2_POSITION: Vector2 = Vector2(560, -1280)
const TELEPORTER_3_POSITION: Vector2 = Vector2(560, -2560)

# Boss trigger on the top floor.
const BOSS_TRIGGER_RECT: Rect2 = Rect2(-160, -2750, 320, 128)

# Destination spawn points for teleporters (same scene, different spawn nodes).
const SPAWN_FLOOR_2: String = "floor_2_entry"
const SPAWN_FLOOR_3: String = "floor_3_entry"
const SPAWN_TOP_FLOOR: String = "top_floor_entry"

# ---------------------------------------------------------------------------
# Child node paths
# ---------------------------------------------------------------------------
@onready var teleporter_to_floor_2: Area2D = $TeleporterToFloor2
@onready var teleporter_to_floor_3: Area2D = $TeleporterToFloor3
@onready var teleporter_to_top: Area2D = $TeleporterToTop
@onready var boss_trigger: Area2D = $BossTrigger

# ---------------------------------------------------------------------------
# _ready override
# ---------------------------------------------------------------------------
func _ready() -> void:
	location_id = LOCATION_ID
	music_track = MUSIC
	default_battle_background = BATTLE_BG

	if teleporter_to_floor_2:
		teleporter_to_floor_2.body_entered.connect(_on_teleporter_floor_2_body_entered)

	if teleporter_to_floor_3:
		teleporter_to_floor_3.body_entered.connect(_on_teleporter_floor_3_body_entered)

	if teleporter_to_top:
		teleporter_to_top.body_entered.connect(_on_teleporter_top_body_entered)

	if boss_trigger:
		boss_trigger.body_entered.connect(_on_boss_trigger_body_entered)

	super._ready()

	_setup_encounter_zones()

# ---------------------------------------------------------------------------
# Story triggers (override)
# ---------------------------------------------------------------------------
func handle_story_triggers() -> void:
	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags == null:
		push_warning("FinalDungeon.handle_story_triggers: GameFlags autoload missing.")
		return

	# Lock top-floor teleporter until floors 1 and 2 are cleared.
	if teleporter_to_top:
		teleporter_to_top.monitoring = (
			flags.get_flag("void_spire_floor_2_cleared") and
			flags.get_flag("void_spire_floor_3_cleared")
		)

	# Disable boss trigger if final boss already defeated.
	if boss_trigger:
		boss_trigger.monitoring = not flags.get_flag("final_boss_defeated")

	if not flags.get_flag("final_dungeon_entered"):
		flags.set_flag("final_dungeon_entered", true)
		emit_signal("story_trigger_fired", "final_dungeon_entered")

# ---------------------------------------------------------------------------
# Private – encounter zones (all three floors)
# ---------------------------------------------------------------------------
func _setup_encounter_zones() -> void:
	spawn_encounter_zone(ZONE_FLOOR_1, ENCOUNTER_RATE, ENCOUNTER_POOL, BATTLE_BG)
	spawn_encounter_zone(ZONE_FLOOR_2, ENCOUNTER_RATE, ENCOUNTER_POOL, BATTLE_BG)
	spawn_encounter_zone(ZONE_FLOOR_3, ENCOUNTER_RATE + 0.08, ENCOUNTER_POOL, BATTLE_BG)

# ---------------------------------------------------------------------------
# Private – ending resolution
# ---------------------------------------------------------------------------
func _resolve_ending() -> void:
	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags == null:
		return

	var ending_id: String = _determine_ending(flags)
	flags.set_flag("ending_reached_" + ending_id, true)
	emit_signal("story_trigger_fired", "ending_" + ending_id)

	var ending_manager: Node = get_node_or_null("/root/EndingManager")
	if ending_manager and ending_manager.has_method("play_ending"):
		ending_manager.play_ending(ending_id)
	else:
		push_warning("FinalDungeon._resolve_ending: EndingManager autoload not found.")

func _determine_ending(flags: Node) -> String:
	# Four endings based on story flag combinations.
	var joined_orisia: bool = flags.get_flag("orisia_side_accepted")
	var all_recruited: bool = flags.get_flag("all_characters_recruited")
	var fei_alive: bool = not flags.get_flag("fei_is_dead")

	if joined_orisia and all_recruited and fei_alive:
		return "true_peace"
	elif joined_orisia:
		return "orisia_victory"
	elif all_recruited:
		return "resistance_triumph"
	else:
		return "bitter_sacrifice"

func _on_final_boss_defeated() -> void:
	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags:
		flags.set_flag("final_boss_defeated", true)
	emit_signal("story_trigger_fired", "final_boss_defeated")
	_resolve_ending()

# ---------------------------------------------------------------------------
# Signal callbacks – teleporters (same-scene repositioning)
# ---------------------------------------------------------------------------
func _on_teleporter_floor_2_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags:
		flags.set_flag("void_spire_floor_2_cleared", true)
	# Teleport within the same scene to floor 2 spawn.
	_teleport_player_to_spawn(SPAWN_FLOOR_2)

func _on_teleporter_floor_3_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags:
		flags.set_flag("void_spire_floor_3_cleared", true)
	_teleport_player_to_spawn(SPAWN_FLOOR_3)

func _on_teleporter_top_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	_teleport_player_to_spawn(SPAWN_TOP_FLOOR)

func _teleport_player_to_spawn(spawn_id: String) -> void:
	var spawn_node: Node = _find_spawn_point(spawn_id)
	if spawn_node and _player_node:
		_player_node.global_position = spawn_node.global_position
	else:
		push_warning(
			"FinalDungeon._teleport_player_to_spawn: Spawn point '%s' not found." % spawn_id
		)

func _on_boss_trigger_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags and flags.get_flag("final_boss_defeated"):
		return
	var battle_manager: Node = get_node_or_null("/root/BattleManager")
	if battle_manager and battle_manager.has_method("start_boss_battle"):
		battle_manager.start_boss_battle("final_boss", BATTLE_BG)
		if battle_manager.has_signal("battle_won"):
			if not battle_manager.battle_won.is_connected(_on_final_boss_defeated):
				battle_manager.battle_won.connect(_on_final_boss_defeated, CONNECT_ONE_SHOT)
