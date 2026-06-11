## desert_region.gd
## The Desert Region – a punishing mid-to-late-game area of
## "There Will Be Kobolds". High encounter rates, limited rest points,
## expensive vendors, and best-in-slot equipment hidden in randomised chests.
## Once the army blocks the return path the player cannot go back.
extends BaseLocation
class_name DesertRegion

# ---------------------------------------------------------------------------
# Location constants
# ---------------------------------------------------------------------------
const LOCATION_ID: String = "desert_region"
const MUSIC: String = "desert"
const BATTLE_BG: String = "desert_dunes"

# Enemy pool – intentionally harder than earlier zones.
const ENCOUNTER_POOL: Array = [
	"desert_wraith",
	"sand_scorpion",
	"desert_cultist",
	"undead_knight",
]
const ENCOUNTER_RATE: float = 0.35   # 35% chance per step tick (high pressure).

# The region has exactly two rest/save points.
const REST_POINT_COUNT: int = 2

# Encounter zones (local-space Rect2).
const ZONE_OPEN_SANDS: Rect2    = Rect2(-640, -128, 1280, 256)
const ZONE_CANYON_PASS: Rect2   = Rect2(-192, 128, 384, 192)
const ZONE_RUINS_INTERIOR: Rect2 = Rect2(320, -96, 256, 160)

# Vendor NPC identifiers and spawn positions.
const NPC_DESERT_VENDOR_A: String = "desert_vendor_oasis"
const NPC_DESERT_VENDOR_B: String = "desert_vendor_ruins"

const VENDOR_SPAWNS: Dictionary = {
	"desert_vendor_oasis": Vector2(-300, -64),
	"desert_vendor_ruins": Vector2( 390,  32),
}

# Chest positions are randomised each run.  These are the candidate positions
# from which CHEST_COUNT positions are drawn without replacement.
const CHEST_COUNT: int = 4
const CHEST_CANDIDATE_POSITIONS: Array = [
	Vector2(-520,  80),
	Vector2(-400, -96),
	Vector2( 120, 140),
	Vector2( 280, -80),
	Vector2( 480,  96),
	Vector2( 560, -48),
	Vector2(-180, 160),
	Vector2( 640, 112),
]

# Best-in-slot equipment pool distributed across the chests.
const BIS_EQUIPMENT_POOL: Array = [
	"desert_veil_armor",
	"scorpion_fang_blade",
	"wraith_channeling_staff",
	"oasis_shield",
	"sand_sovereign_ring",
	"dune_strider_boots",
]

# Destination when leaving forward (toward army camp).
const EXIT_FORWARD_DESTINATION: String = "army_camp"
const EXIT_FORWARD_SPAWN: String = "from_desert"

# Destination when leaving backward (toward previous region).
# Blocked by army_blocks_return flag.
const EXIT_BACK_DESTINATION: String = "imperial_city"
const EXIT_BACK_SPAWN: String = "from_desert_return"

# Sensory Deprivation spell is sold by vendors (flag guards first availability).
const SENSORY_DEPRIVATION_VENDOR_ID: String = "desert_vendor_oasis"

# ---------------------------------------------------------------------------
# @onready child nodes
# ---------------------------------------------------------------------------
@onready var exit_forward_trigger: Area2D = $Exits/ForwardTrigger
@onready var exit_back_trigger: Area2D    = $Exits/BackTrigger
@onready var army_blockade_overlay: Node  = $ArmyBlockadeOverlay
@onready var rest_point_markers: Node     = $RestPointMarkers   # parent of Marker2D children


# ---------------------------------------------------------------------------
# _ready override
# ---------------------------------------------------------------------------
func _ready() -> void:
	location_id = LOCATION_ID
	music_track  = MUSIC
	default_battle_background = BATTLE_BG

	_connect_exit_triggers()

	super._ready()

	_setup_encounter_zones()
	_setup_rest_points()
	_spawn_vendors()
	_spawn_randomised_chests()
	_apply_army_blockade_state()


# ---------------------------------------------------------------------------
# Story triggers (override)
# ---------------------------------------------------------------------------
func handle_story_triggers() -> void:
	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags == null:
		push_warning("DesertRegion.handle_story_triggers: GameFlags autoload missing.")
		return

	# Enforce one-way travel if the army has closed the path.
	if flags.get_flag("army_blocks_return"):
		_block_backward_exit()

	emit_signal("story_trigger_fired", "desert_region_triggers_checked")


# ---------------------------------------------------------------------------
# Private – encounter zones
# ---------------------------------------------------------------------------
func _setup_encounter_zones() -> void:
	spawn_encounter_zone(ZONE_OPEN_SANDS,     ENCOUNTER_RATE,        ENCOUNTER_POOL, BATTLE_BG)
	spawn_encounter_zone(ZONE_CANYON_PASS,    ENCOUNTER_RATE + 0.05, ENCOUNTER_POOL, BATTLE_BG)
	spawn_encounter_zone(ZONE_RUINS_INTERIOR, ENCOUNTER_RATE + 0.10, ENCOUNTER_POOL, BATTLE_BG)


# ---------------------------------------------------------------------------
# Private – rest / save points (exactly two)
# ---------------------------------------------------------------------------
func _setup_rest_points() -> void:
	var sp_scene: PackedScene = load(SAVE_POINT_SCENE_PATH)
	if sp_scene == null:
		push_error("DesertRegion._setup_rest_points: Could not load save point scene.")
		return

	# Use Marker2D children of rest_point_markers as positions.
	var markers: Array = []
	if rest_point_markers:
		for child in rest_point_markers.get_children():
			if child is Marker2D:
				markers.append(child)

	# Fallback hard-coded positions if scene markers are missing.
	var fallback_positions: Array[Vector2] = [
		Vector2(-480, -64),
		Vector2(400,   80),
	]

	for i in REST_POINT_COUNT:
		var rp: Node = sp_scene.instantiate()
		rp.name = "RestPoint_%d" % i
		add_child(rp)

		if i < markers.size():
			rp.global_position = markers[i].global_position
		elif i < fallback_positions.size():
			rp.global_position = fallback_positions[i]

		if rp.has_signal("save_requested"):
			rp.save_requested.connect(show_save_point)

		# First rest point also acts as _save_point_node for the base class.
		if i == 0:
			_save_point_node = rp


# ---------------------------------------------------------------------------
# Private – vendors
# ---------------------------------------------------------------------------
func _spawn_vendors() -> void:
	for vendor_id in VENDOR_SPAWNS:
		var vendor: Node = add_npc(vendor_id, VENDOR_SPAWNS[vendor_id])
		if vendor == null:
			continue

		if vendor.has_method("set_shop_type"):
			vendor.set_shop_type("desert_vendor")

		# Mark the oasis vendor as the source of Sensory Deprivation.
		if vendor_id == SENSORY_DEPRIVATION_VENDOR_ID:
			if vendor.has_method("add_special_item"):
				vendor.add_special_item("sensory_deprivation_spell")


# ---------------------------------------------------------------------------
# Private – randomised chests
# ---------------------------------------------------------------------------
func _spawn_randomised_chests() -> void:
	var flags: Node = get_node_or_null("/root/GameFlags")

	# Determine positions. Use a stored seed per run so positions are stable
	# within a single playthrough but differ between NG runs.
	var rng: RandomNumberGenerator = RandomNumberGenerator.new()
	var run_seed: int = 0
	if flags and flags.has_method("get_run_seed"):
		run_seed = flags.get_run_seed()
	rng.seed = run_seed

	var candidates: Array = CHEST_CANDIDATE_POSITIONS.duplicate()
	candidates.shuffle()   # GDScript Array.shuffle uses the global RNG seed.
	# For determinism, pick manually using our seeded RNG.
	var chosen_positions: Array = []
	var pool_copy: Array = CHEST_CANDIDATE_POSITIONS.duplicate()
	for _i in CHEST_COUNT:
		var idx: int = rng.randi() % pool_copy.size()
		chosen_positions.append(pool_copy[idx])
		pool_copy.remove_at(idx)

	# Distribute equipment evenly across chests.
	var eq_pool: Array = BIS_EQUIPMENT_POOL.duplicate()
	var chest_scene_path: String = "res://scenes/gameplay/chest.tscn"
	var chest_scene: PackedScene = load(chest_scene_path)

	for i in CHEST_COUNT:
		if chest_scene == null:
			# No scene available; just log and skip.
			push_warning("DesertRegion: Could not load treasure_chest scene.")
			break

		var chest: Node = chest_scene.instantiate()
		chest.name = "DesertChest_%d" % i
		add_child(chest)
		chest.global_position = chosen_positions[i]

		# Assign loot – cycle through pool so all slots are covered.
		var loot_id: String = eq_pool[i % eq_pool.size()]
		if chest.has_method("set_loot"):
			chest.set_loot([loot_id])

		# Mark already-opened chests as looted (loaded from save).
		var chest_flag: String = "desert_chest_%d_opened_%d" % [i, run_seed]
		if flags and flags.get_flag(chest_flag):
			if chest.has_method("set_opened"):
				chest.set_opened(true)
		elif chest.has_signal("chest_opened"):
			chest.chest_opened.connect(_on_chest_opened.bind(chest_flag))


func _on_chest_opened(chest_flag: String) -> void:
	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags:
		flags.set_flag(chest_flag, true)


# ---------------------------------------------------------------------------
# Private – exit triggers
# ---------------------------------------------------------------------------
func _connect_exit_triggers() -> void:
	if exit_forward_trigger and exit_forward_trigger.has_signal("body_entered"):
		exit_forward_trigger.body_entered.connect(_on_exit_forward_entered)

	if exit_back_trigger and exit_back_trigger.has_signal("body_entered"):
		exit_back_trigger.body_entered.connect(_on_exit_back_entered)


func _apply_army_blockade_state() -> void:
	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags and flags.get_flag("army_blocks_return"):
		_block_backward_exit()


func _block_backward_exit() -> void:
	# Show a physical blockade sprite / collision.
	if army_blockade_overlay:
		army_blockade_overlay.visible = true

	# Disable the exit trigger so the player can't walk through.
	if exit_back_trigger:
		exit_back_trigger.monitoring = false
		exit_back_trigger.monitorable = false


# ---------------------------------------------------------------------------
# Signal callbacks
# ---------------------------------------------------------------------------
func _on_exit_forward_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	go_to_location(EXIT_FORWARD_DESTINATION, EXIT_FORWARD_SPAWN)


func _on_exit_back_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return

	var flags: Node = get_node_or_null("/root/GameFlags")
	if flags and flags.get_flag("army_blocks_return"):
		# Show a message; do not transition.
		var notify: Node = get_node_or_null("/root/NotificationManager")
		if notify and notify.has_method("show_message"):
			notify.show_message(
				"The army's blockade seals the path. There is no going back."
			)
		return

	go_to_location(EXIT_BACK_DESTINATION, EXIT_BACK_SPAWN)
