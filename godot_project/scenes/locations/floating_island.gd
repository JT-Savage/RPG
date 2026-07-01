## floating_island.gd
## Floating Island – a sky island sanctuary where the Dreamwalker resides.
## Introduces psychic damage via tutorial trigger. Backup chest for Yipp items.
extends BaseLocation
class_name FloatingIsland

# ---------------------------------------------------------------------------
# Location constants
# ---------------------------------------------------------------------------
const LOCATION_ID: String = "floating_island"
const MUSIC: String = "ethereal"
const BATTLE_BG: String = "sky"

const ENCOUNTER_POOL: Array = ["sky_serpent", "wind_elemental"]
const ENCOUNTER_RATE: float = 0.22

const ZONE_OUTER_ISLAND: Rect2 = Rect2(-600, -128, 1200, 256)
const ZONE_CLOUD_EDGE: Rect2 = Rect2(-700, 80, 300, 200)

const NPC_DREAMWALKER_ID: String = "dreamwalker"
const NPC_DREAMWALKER_POSITION: Vector2 = Vector2(0, -40)

# Yipp backup item chest positions.
const CHEST_HOLY_SYMBOL_POSITION: Vector2 = Vector2(300, 60)
const CHEST_WINE_GLASS_POSITION: Vector2 = Vector2(360, 60)

const EXIT_TO_MOUNTAIN: String = "mountain_pass"
const SPAWN_FROM_ISLAND: String = "from_island"

# ---------------------------------------------------------------------------
# Child node paths
# ---------------------------------------------------------------------------
@onready var exit_trigger: Area2D = $ExitTrigger
@onready var chest_holy_symbol = $ChestHolySymbol
@onready var chest_wine_glass = $ChestWineGlass
@onready var psychic_tutorial_trigger: Area2D = $PsychicTutorialTrigger

# ---------------------------------------------------------------------------
# _ready override
# ---------------------------------------------------------------------------
func _ready() -> void:
	location_id = LOCATION_ID
	music_track = MUSIC
	default_battle_background = BATTLE_BG

	if exit_trigger:
		exit_trigger.body_entered.connect(_on_exit_trigger_body_entered)

	if chest_holy_symbol and chest_holy_symbol.has_signal("interacted"):
		chest_holy_symbol.interacted.connect(_on_chest_holy_symbol_interacted)

	if chest_wine_glass and chest_wine_glass.has_signal("interacted"):
		chest_wine_glass.interacted.connect(_on_chest_wine_glass_interacted)

	if psychic_tutorial_trigger:
		psychic_tutorial_trigger.body_entered.connect(_on_psychic_tutorial_trigger_body_entered)

	super._ready()

	_setup_encounter_zones()
	_spawn_dreamwalker()
	_configure_yipp_chests()

# ---------------------------------------------------------------------------
# Story triggers (override)
# ---------------------------------------------------------------------------
func handle_story_triggers() -> void:
	var flags = get_node_or_null("/root/GameFlags")
	if flags == null:
		push_warning("FloatingIsland.handle_story_triggers: GameFlags autoload missing.")
		return

	# Restore chest open states.
	if flags.get_flag("yipp_holy_symbol_obtained"):
		if chest_holy_symbol and chest_holy_symbol.has_method("set_opened"):
			chest_holy_symbol.set_opened(true)

	if flags.get_flag("yipp_wine_glass_obtained"):
		if chest_wine_glass and chest_wine_glass.has_method("set_opened"):
			chest_wine_glass.set_opened(true)

	if not flags.get_flag("floating_island_first_visit_done"):
		flags.set_flag("floating_island_first_visit_done", true)
		emit_signal("story_trigger_fired", "floating_island_first_visit")

# ---------------------------------------------------------------------------
# Private – encounter zones
# ---------------------------------------------------------------------------
func _setup_encounter_zones() -> void:
	spawn_encounter_zone(ZONE_OUTER_ISLAND, ENCOUNTER_RATE, ENCOUNTER_POOL, BATTLE_BG)
	spawn_encounter_zone(ZONE_CLOUD_EDGE, ENCOUNTER_RATE + 0.08, ENCOUNTER_POOL, BATTLE_BG)

# ---------------------------------------------------------------------------
# Private – Dreamwalker NPC
# ---------------------------------------------------------------------------
func _spawn_dreamwalker() -> void:
	var dw: Node = add_npc(NPC_DREAMWALKER_ID, NPC_DREAMWALKER_POSITION)
	if dw and dw.has_method("play_cutscene"):
		var flags = get_node_or_null("/root/GameFlags")
		if flags and not flags.get_flag("dreamwalker_introduced"):
			dw.set_meta("cutscene_id", "dreamwalker_introduction")
			dw.set_meta("trigger_proximity", 96.0)

# ---------------------------------------------------------------------------
# Private – Yipp backup item chests
# ---------------------------------------------------------------------------
func _configure_yipp_chests() -> void:
	var flags = get_node_or_null("/root/GameFlags")

	# Show holy symbol chest only if the item was not obtained elsewhere.
	if chest_holy_symbol:
		var already_have: bool = flags != null and flags.get_flag("yipp_holy_symbol_obtained")
		if chest_holy_symbol.has_method("set_enabled"):
			chest_holy_symbol.set_enabled(not already_have)
		chest_holy_symbol.visible = not already_have

	# Show wine glass chest only if the item was not obtained elsewhere.
	if chest_wine_glass:
		var already_have: bool = flags != null and flags.get_flag("yipp_wine_glass_obtained")
		if chest_wine_glass.has_method("set_enabled"):
			chest_wine_glass.set_enabled(not already_have)
		chest_wine_glass.visible = not already_have

# ---------------------------------------------------------------------------
# Signal callbacks
# ---------------------------------------------------------------------------
func _on_exit_trigger_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	go_to_location(EXIT_TO_MOUNTAIN, SPAWN_FROM_ISLAND)

func _on_chest_holy_symbol_interacted() -> void:
	var flags = get_node_or_null("/root/GameFlags")
	if flags and flags.get_flag("yipp_holy_symbol_obtained"):
		return
	var inventory = get_node_or_null("/root/Inventory")
	if inventory and inventory.has_method("add_item"):
		inventory.add_item("yipp_holy_symbol")
	if flags:
		flags.set_flag("yipp_holy_symbol_obtained", true)
	emit_signal("story_trigger_fired", "yipp_holy_symbol_chest_opened")
	if chest_holy_symbol and chest_holy_symbol.has_method("set_opened"):
		chest_holy_symbol.set_opened(true)

func _on_chest_wine_glass_interacted() -> void:
	var flags = get_node_or_null("/root/GameFlags")
	if flags and flags.get_flag("yipp_wine_glass_obtained"):
		return
	var inventory = get_node_or_null("/root/Inventory")
	if inventory and inventory.has_method("add_item"):
		inventory.add_item("yipp_wine_glass")
	if flags:
		flags.set_flag("yipp_wine_glass_obtained", true)
	emit_signal("story_trigger_fired", "yipp_wine_glass_chest_opened")
	if chest_wine_glass and chest_wine_glass.has_method("set_opened"):
		chest_wine_glass.set_opened(true)

func _on_psychic_tutorial_trigger_body_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	var flags = get_node_or_null("/root/GameFlags")
	if flags and flags.get_flag("psychic_tutorial_shown"):
		return
	var ui_manager = get_node_or_null("/root/UIManager")
	if ui_manager and ui_manager.has_method("show_tutorial_popup"):
		ui_manager.show_tutorial_popup("psychic_damage_tutorial")
	if flags:
		flags.set_flag("psychic_tutorial_shown", true)
	emit_signal("story_trigger_fired", "psychic_damage_tutorial_shown")
