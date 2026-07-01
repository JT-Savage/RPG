## tutorial_warren.gd
## The Tutorial Warren – the opening dungeon of "There Will Be Kobolds".
## Kobold warrens infested with an early-stage infection. Serves as the
## player's introduction to combat, story triggers, and the save system.
extends BaseLocation
class_name TutorialWarren

# ---------------------------------------------------------------------------
# Location constants
# ---------------------------------------------------------------------------
const LOCATION_ID: String = "tutorial_warren"
const MUSIC: String = "dungeon"
const BATTLE_BG: String = "warren_stone_tunnel"

# Enemy pool for encounter zones
const ENCOUNTER_POOL: Array = ["infected_kobold", "zombie_kobold"]
const ENCOUNTER_RATE: float = 0.25          # 25% chance per encounter step tick

# Encounter zone rectangles (local-space Rect2: x, y, width, height)
const ZONE_MAIN_TUNNEL: Rect2 = Rect2(-480, -96, 960, 192)
const ZONE_SIDE_CHAMBER: Rect2 = Rect2(200, 96, 320, 160)

# Chest containing the baby-dragon item (world position)
const BABY_DRAGON_CHEST_POSITION: Vector2 = Vector2(340, 60)

# Kella cutscene NPC spawn
const KELLA_NPC_ID: String = "kella"
const KELLA_SPAWN_POSITION: Vector2 = Vector2(-120, 48)

# Exit trigger rect – player overlaps this to travel to surface_forest
const EXIT_DESTINATION: String = "surface_forest"
const EXIT_SPAWN_POINT: String = "from_warren"

# Save point world position
const SAVE_POINT_SPAWN: Vector2 = Vector2(-360, 0)

# ---------------------------------------------------------------------------
# Child node paths (set in scene editor, declared here for reference)
# ---------------------------------------------------------------------------
@onready var exit_trigger: Area2D = $ExitTrigger
@onready var baby_dragon_chest = $BabyDragonChest
@onready var save_point_marker: Marker2D = $SavePointMarker
@onready var tutorial_prompt_label: Label = $UI/TutorialPromptLabel


# ---------------------------------------------------------------------------
# _ready override
# ---------------------------------------------------------------------------
func _ready() -> void:
	location_id = LOCATION_ID
	music_track = MUSIC
	default_battle_background = BATTLE_BG

	# Connect exit trigger before calling super (super spawns player first).
	if exit_trigger:
		exit_trigger.body_entered.connect(_on_exit_trigger_body_entered)

	# Connect chest interaction.
	if baby_dragon_chest and baby_dragon_chest.has_signal("interacted"):
		baby_dragon_chest.interacted.connect(_on_baby_dragon_chest_interacted)

	# Base class handles player spawn, music, autosave, and story trigger check.
	super._ready()

	# Spawn encounter zones after base setup.
	_setup_encounter_zones()

	# Place the save point.
	_setup_save_point()

	# Show tutorial movement hints on first visit.
	_show_tutorial_hints()


# ---------------------------------------------------------------------------
# Story triggers (override)
# ---------------------------------------------------------------------------
func handle_story_triggers() -> void:
	var flags = get_node_or_null("/root/GameFlags")
	if flags == null:
		push_warning("TutorialWarren.handle_story_triggers: GameFlags autoload missing.")
		return

	# ------------------------------------------------------------------
	# Trigger 1: Warren infection flag – adjusts enemy visuals / dialogue.
	# ------------------------------------------------------------------
	if flags.get_flag("warren_infected"):
		_activate_full_infection_state()
	else:
		# Set the infection flag on first entry so it persists across saves.
		flags.set_flag("warren_infected", true)
		emit_signal("story_trigger_fired", "warren_infected_initial")

	# ------------------------------------------------------------------
	# Trigger 2: Baby dragon chest – only if item not already collected.
	# ------------------------------------------------------------------
	if not flags.get_flag("baby_dragon_chest_opened"):
		_enable_baby_dragon_chest()
	else:
		# Chest already looted: replace with empty / open sprite.
		if baby_dragon_chest and baby_dragon_chest.has_method("set_opened"):
			baby_dragon_chest.set_opened(true)

	# ------------------------------------------------------------------
	# Trigger 3: Kella cutscene – fires once, before the warren exit.
	# ------------------------------------------------------------------
	if not flags.get_flag("kella_cutscene_played"):
		_spawn_kella_for_cutscene()


# ---------------------------------------------------------------------------
# Private – encounter zones
# ---------------------------------------------------------------------------
func _setup_encounter_zones() -> void:
	# Main tunnel zone.
	spawn_encounter_zone(ZONE_MAIN_TUNNEL, ENCOUNTER_RATE, ENCOUNTER_POOL, BATTLE_BG)
	# Side chamber has a slightly higher encounter rate (more enemies packed in).
	spawn_encounter_zone(ZONE_SIDE_CHAMBER, ENCOUNTER_RATE + 0.10, ENCOUNTER_POOL, BATTLE_BG)


# ---------------------------------------------------------------------------
# Private – save point
# ---------------------------------------------------------------------------
func _setup_save_point() -> void:
	var sp_scene: PackedScene = load(SAVE_POINT_SCENE_PATH)
	if sp_scene == null:
		push_error("TutorialWarren._setup_save_point: Could not load save point scene.")
		return

	_save_point_node = sp_scene.instantiate()
	_save_point_node.name = "SavePoint"
	add_child(_save_point_node)

	# Position via marker if available, otherwise use constant.
	if save_point_marker:
		_save_point_node.global_position = save_point_marker.global_position
	else:
		_save_point_node.global_position = SAVE_POINT_SPAWN

	if _save_point_node.has_signal("save_requested"):
		_save_point_node.save_requested.connect(show_save_point)


# ---------------------------------------------------------------------------
# Private – story trigger helpers
# ---------------------------------------------------------------------------
func _activate_full_infection_state() -> void:
	# Visual / audio changes to reflect the warren being fully infected.
	# Child nodes tagged "infection_overlay" become visible.
	for node in get_tree().get_nodes_in_group("infection_overlay"):
		node.visible = true
	emit_signal("story_trigger_fired", "warren_full_infection")


func _enable_baby_dragon_chest() -> void:
	if baby_dragon_chest and baby_dragon_chest.has_method("set_enabled"):
		baby_dragon_chest.set_enabled(true)


func _spawn_kella_for_cutscene() -> void:
	var kella = add_npc(KELLA_NPC_ID, KELLA_SPAWN_POSITION)
	if kella and kella.has_method("play_cutscene"):
		# Cutscene plays when the player reaches the warren exit area.
		# Kella's NPC script will handle the trigger proximity check.
		kella.set_meta("cutscene_id", "kella_warren_farewell")
		kella.set_meta("trigger_proximity", 80.0)


# ---------------------------------------------------------------------------
# Private – tutorial hints
# ---------------------------------------------------------------------------
func _show_tutorial_hints() -> void:
	var flags = get_node_or_null("/root/GameFlags")
	if flags and flags.get_flag("tutorial_complete"):
		# Skip hints on repeat playthroughs / after tutorial is done.
		if tutorial_prompt_label:
			tutorial_prompt_label.hide()
		return

	if tutorial_prompt_label:
		tutorial_prompt_label.text = (
			"Use arrow keys or WASD to move.\n"
			+ "Interact with [Z] or [Enter].\n"
			+ "Open the menu with [X] or [Escape]."
		)
		tutorial_prompt_label.show()


# ---------------------------------------------------------------------------
# Signal callbacks
# ---------------------------------------------------------------------------
func _on_exit_trigger_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return

	var flags = get_node_or_null("/root/GameFlags")

	# Kella cutscene must play before the player can leave.
	if flags and not flags.get_flag("kella_cutscene_played"):
		# Kella blocks the exit – her NPC script handles the blocking behaviour.
		var kella = _npc_nodes.get(KELLA_NPC_ID)
		if kella and kella.has_method("force_cutscene"):
			kella.force_cutscene()
		return

	go_to_location(EXIT_DESTINATION, EXIT_SPAWN_POINT)


func _on_baby_dragon_chest_interacted() -> void:
	var flags = get_node_or_null("/root/GameFlags")
	if flags and flags.get_flag("baby_dragon_chest_opened"):
		return

	# Give the player the baby dragon item.
	var inventory = get_node_or_null("/root/Inventory")
	if inventory and inventory.has_method("add_item"):
		inventory.add_item("baby_dragon_egg")

	if flags:
		flags.set_flag("baby_dragon_chest_opened", true)

	emit_signal("story_trigger_fired", "baby_dragon_chest_opened")

	# Show a small notification.
	var notify = get_node_or_null("/root/NotificationManager")
	if notify and notify.has_method("show_key_item"):
		notify.show_key_item("baby_dragon_egg")
