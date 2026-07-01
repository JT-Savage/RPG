## imperial_city.gd
## The Imperial City – the main hub town of "There Will Be Kobolds".
## Home to all major shops, the inn, and several recruitable party members.
## Also serves as the fast-travel hub once the player has visited.
extends BaseLocation
class_name ImperialCity

# ---------------------------------------------------------------------------
# Location constants
# ---------------------------------------------------------------------------
const LOCATION_ID: String = "imperial_city"
const MUSIC: String = "town"

# No random encounters in the city.

# ---------------------------------------------------------------------------
# Shop scene paths
# ---------------------------------------------------------------------------
const SHOP_SCENE: String = "res://scenes/shop/shop_scene.tscn"
const SHOP_ID_MARKET: String = "imperial_city_market"
const SHOP_ID_BLACK_MARKET: String = "imperial_city_black_market"
const INN_COST: int = 50

# ---------------------------------------------------------------------------
# NPC identifiers and their world-space spawn positions
# ---------------------------------------------------------------------------
## Shopkeepers
const NPC_WEAPON_SHOPKEEPER: String  = "weapon_shopkeeper"
const NPC_MAGIC_SHOPKEEPER: String   = "magic_shopkeeper"
const NPC_ITEM_SHOPKEEPER: String    = "item_shopkeeper"
const NPC_INNKEEPER: String          = "innkeeper"

## Guards (decorative / minor dialogue)
const NPC_GUARD_GATE: String         = "city_guard_gate"
const NPC_GUARD_MARKET: String       = "city_guard_market"
const NPC_GUARD_PALACE: String       = "city_guard_palace"

## Recruitable party members
const NPC_MICHAEL: String            = "michael"
const NPC_FLOOD: String              = "flood"
const NPC_HANNAH: String             = "hannah"

## Story NPC
const NPC_FRITZZIT: String           = "fritzzit"
const NPC_CRANKPOT: String           = "crankpot"

# Spawn positions (world space; match scene layout).
const SPAWNS: Dictionary = {
	"weapon_shopkeeper":  Vector2(120,  -48),
	"magic_shopkeeper":   Vector2(320,  -48),
	"item_shopkeeper":    Vector2(520,  -48),
	"innkeeper":          Vector2(-160, -48),
	"city_guard_gate":    Vector2(-480, 32),
	"city_guard_market":  Vector2(64,   32),
	"city_guard_palace":  Vector2(480,  32),
	"michael":            Vector2(200,  64),
	"flood":              Vector2(-80,  64),
	"hannah":             Vector2(-200, 64),
	"fritzzit":           Vector2(380,  96),
	"crankpot":           Vector2(420,  96),
}

# Interactive shop-door node paths (set in scene editor).
@onready var weapon_shop_door: Area2D  = $Shops/WeaponShopDoor
@onready var magic_shop_door: Area2D   = $Shops/MagicShopDoor
@onready var item_shop_door: Area2D    = $Shops/ItemShopDoor
@onready var inn_door: Area2D          = $Inn/InnDoor

# Fast-travel board node.
@onready var fast_travel_board   = $FastTravelBoard


# ---------------------------------------------------------------------------
# _ready override
# ---------------------------------------------------------------------------
func _ready() -> void:
	location_id = LOCATION_ID
	music_track  = MUSIC
	default_battle_background = ""   # No battles in the city.

	_connect_shop_doors()

	super._ready()

	# Spawn static NPCs.
	_spawn_city_npcs()

	# Configure fast travel.
	_setup_fast_travel()


# ---------------------------------------------------------------------------
# Story triggers (override)
# ---------------------------------------------------------------------------
func handle_story_triggers() -> void:
	var flags = get_node_or_null("/root/GameFlags")
	if flags == null:
		push_warning("ImperialCity.handle_story_triggers: GameFlags autoload missing.")
		return

	# ------------------------------------------------------------------
	# Trigger: Michael recruitment scene.
	# Michael is available in the city unless already recruited or his
	# recruitment quest is past the deadline.
	# ------------------------------------------------------------------
	if not flags.get_flag("michael_recruited") and not flags.get_flag("recruitment_deadline_passed"):
		_enable_michael_recruitment()
	else:
		_remove_npc_if_present(NPC_MICHAEL)

	# ------------------------------------------------------------------
	# Trigger: Flood recruitment.
	# ------------------------------------------------------------------
	if not flags.get_flag("flood_recruited") and not flags.get_flag("recruitment_deadline_passed"):
		_enable_flood_recruitment()
	else:
		_remove_npc_if_present(NPC_FLOOD)

	# ------------------------------------------------------------------
	# Trigger: Hannah recruitment.
	# ------------------------------------------------------------------
	if not flags.get_flag("hannah_recruited") and not flags.get_flag("recruitment_deadline_passed"):
		_enable_hannah_recruitment()
	else:
		_remove_npc_if_present(NPC_HANNAH)

	# ------------------------------------------------------------------
	# Trigger: Kobolds released into city (changes ambient NPC behaviour
	# and adds a wave of panicking kobold NPCs in the street).
	# ------------------------------------------------------------------
	if flags.get_flag("kobolds_released"):
		_play_kobolds_released_state()

	# ------------------------------------------------------------------
	# Trigger: Fritzzit & Crankpot become available after a story beat.
	# ------------------------------------------------------------------
	if flags.get_flag("fritzzit_crankpot_available"):
		_spawn_fritzzit_crankpot()
	else:
		_remove_npc_if_present(NPC_FRITZZIT)
		_remove_npc_if_present(NPC_CRANKPOT)

	emit_signal("story_trigger_fired", "imperial_city_triggers_checked")


# ---------------------------------------------------------------------------
# Private – NPC spawning
# ---------------------------------------------------------------------------
func _spawn_city_npcs() -> void:
	# Always-present shopkeepers and guards.
	for npc_id in [
		NPC_WEAPON_SHOPKEEPER,
		NPC_MAGIC_SHOPKEEPER,
		NPC_ITEM_SHOPKEEPER,
		NPC_INNKEEPER,
		NPC_GUARD_GATE,
		NPC_GUARD_MARKET,
		NPC_GUARD_PALACE,
	]:
		if npc_id in SPAWNS:
			add_npc(npc_id, SPAWNS[npc_id])


func _enable_michael_recruitment() -> void:
	var michael = add_npc(NPC_MICHAEL, SPAWNS[NPC_MICHAEL])
	if michael and michael.has_method("set_dialogue"):
		michael.set_dialogue("michael_recruitment")
	emit_signal("story_trigger_fired", "michael_recruitment")


func _enable_flood_recruitment() -> void:
	var flood = add_npc(NPC_FLOOD, SPAWNS[NPC_FLOOD])
	if flood and flood.has_method("set_dialogue"):
		flood.set_dialogue("flood_recruitment")
	emit_signal("story_trigger_fired", "flood_recruitment")


func _enable_hannah_recruitment() -> void:
	var hannah = add_npc(NPC_HANNAH, SPAWNS[NPC_HANNAH])
	if hannah and hannah.has_method("set_dialogue"):
		hannah.set_dialogue("hannah_recruitment")
	emit_signal("story_trigger_fired", "hannah_recruitment")


func _spawn_fritzzit_crankpot() -> void:
	var fritzzit = add_npc(NPC_FRITZZIT, SPAWNS[NPC_FRITZZIT])
	var crankpot = add_npc(NPC_CRANKPOT, SPAWNS[NPC_CRANKPOT])

	if fritzzit and fritzzit.has_method("set_dialogue"):
		fritzzit.set_dialogue("fritzzit_introduction")
	if crankpot and crankpot.has_method("set_dialogue"):
		crankpot.set_dialogue("crankpot_banter")

	emit_signal("story_trigger_fired", "fritzzit_crankpot_available")


func _remove_npc_if_present(npc_id: String) -> void:
	if npc_id in _npc_nodes:
		_npc_nodes[npc_id].queue_free()
		_npc_nodes.erase(npc_id)


func _play_kobolds_released_state() -> void:
	# Swap city music to a chaotic variant.
	if has_node("/root/AudioManager"):
		get_node("/root/AudioManager").play_music("town_chaos")

	# Spawn panicking kobold NPCs as a visual event (non-combatants).
	var kobold_panic_positions: Array[Vector2] = [
		Vector2(-100, 0), Vector2(50, -20), Vector2(200, 10),
		Vector2(-300, 5), Vector2(310, -10),
	]
	for i in kobold_panic_positions.size():
		var kob = add_npc("panicking_kobold_%d" % i, kobold_panic_positions[i])
		if kob and kob.has_method("set_behaviour"):
			kob.set_behaviour("flee_random")

	emit_signal("story_trigger_fired", "kobolds_released_state")


# ---------------------------------------------------------------------------
# Private – shop doors
# ---------------------------------------------------------------------------
func _connect_shop_doors() -> void:
	_connect_door(weapon_shop_door, "_on_weapon_shop_door_entered")
	_connect_door(magic_shop_door,  "_on_magic_shop_door_entered")
	_connect_door(item_shop_door,   "_on_item_shop_door_entered")
	_connect_door(inn_door,         "_on_inn_door_entered")


func _connect_door(door: Area2D, callback: String) -> void:
	if door and door.has_signal("body_entered"):
		door.body_entered.connect(Callable(self, callback))


func _open_shop(shop_id: String, shop_label: String) -> void:
	var shop_scene: PackedScene = load(SHOP_SCENE)
	if shop_scene == null:
		push_error("ImperialCity._open_shop: Could not load '%s'." % SHOP_SCENE)
		return

	var shop = shop_scene.instantiate()
	shop.name = shop_label
	if shop.has_method("setup"):
		shop.setup(shop_id)
	get_tree().root.add_child(shop)

	# Pause the location while shop is open.
	get_tree().paused = true
	if shop.has_signal("shop_closed"):
		shop.shop_closed.connect(func(): get_tree().paused = false)


# ---------------------------------------------------------------------------
# Shop door signal callbacks
# ---------------------------------------------------------------------------
func _on_weapon_shop_door_entered(body: Node) -> void:
	if body.is_in_group("player"):
		_open_shop(SHOP_ID_MARKET, "WeaponShop")


func _on_magic_shop_door_entered(body: Node) -> void:
	if body.is_in_group("player"):
		_open_shop(SHOP_ID_BLACK_MARKET, "MagicShop")


func _on_item_shop_door_entered(body: Node) -> void:
	if body.is_in_group("player"):
		_open_shop(SHOP_ID_MARKET, "ItemShop")


func _on_inn_door_entered(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	_rest_at_inn()


func _rest_at_inn() -> void:
	if GameManager.gil < INN_COST:
		NotificationManager.show_message("Not enough gil to rest (%d needed)" % INN_COST, Color.RED)
		return
	GameManager.gil -= INN_COST
	PartyManager.restore_all_hp_mp()
	AudioManager.play_sfx("save_point")
	NotificationManager.show_message("The party rested. HP/MP restored!", Color.GREEN)
	SaveSystem.autosave()


# ---------------------------------------------------------------------------
# Private – fast travel
# ---------------------------------------------------------------------------
func _setup_fast_travel() -> void:
	if fast_travel_board == null:
		return

	var flags = get_node_or_null("/root/GameFlags")
	# Fast travel unlocks after visiting the city at least once.
	# The base class already sets visited_imperial_city=true during _ready.
	var unlock: bool = (flags != null and flags.get_flag("visited_imperial_city"))

	fast_travel_board.visible = unlock

	if unlock and fast_travel_board.has_signal("destination_selected"):
		fast_travel_board.destination_selected.connect(_on_fast_travel_destination_selected)


func _on_fast_travel_destination_selected(dest_id: String) -> void:
	go_to_location(dest_id, "fast_travel_arrival")
