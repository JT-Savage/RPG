extends CharacterBody2D
## Player - 4-directional movement, encounters, interaction

const SPEED := 80.0
const TILE_SIZE := 16

@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var camera: Camera2D = $Camera2D
@onready var interaction_area: Area2D = $InteractionArea

var _direction := Vector2.ZERO
var _facing := "down"
var _step_distance := 0.0
var _current_encounter_zone = null
var _can_interact := true
var _spawn_point := ""
var _pause_menu: Node = null

func _ready() -> void:
	add_to_group("player")
	camera.position_smoothing_enabled = true
	camera.position_smoothing_speed = 5.0

	_load_sprite_frames()

	# Connect to encounter zones spawned after the player enters the tree
	get_tree().node_added.connect(_on_node_added)
	# And any zones that already exist
	for zone in get_tree().get_nodes_in_group("encounter_zone"):
		_connect_zone(zone)

func _load_sprite_frames() -> void:
	var leader := "kella"
	if not GameManager.active_party.is_empty():
		leader = GameManager.active_party[0]
	animated_sprite.sprite_frames = SpriteCache.get_character_frames(leader)
	animated_sprite.animation = "walk_down"
	animated_sprite.stop()

func _process(_delta: float) -> void:
	# Quicksave shortcut
	if Input.is_action_just_pressed("action_quicksave") and not BattleManager.in_battle:
		SaveSystem.quicksave()

	# Menu shortcut
	if Input.is_action_just_pressed("action_menu") and not BattleManager.in_battle:
		_open_pause_menu()

func _physics_process(delta: float) -> void:
	if BattleManager.in_battle or DialogueManager.is_active or _pause_menu_open():
		velocity = Vector2.ZERO
		_play_idle()
		return

	_direction = InputManager.get_direction()

	if _direction != Vector2.ZERO:
		velocity = _direction * SPEED
		_update_facing()
		animated_sprite.play("walk_" + _facing)

		# Count a "step" per tile of distance travelled (not per frame)
		_step_distance += SPEED * delta
		if _step_distance >= TILE_SIZE:
			_step_distance -= TILE_SIZE
			_check_encounter()
	else:
		velocity = Vector2.ZERO
		_play_idle()

	move_and_slide()

func _play_idle() -> void:
	animated_sprite.stop()
	animated_sprite.frame = 0

func _update_facing() -> void:
	if abs(_direction.x) >= abs(_direction.y):
		_facing = "right" if _direction.x > 0 else "left"
	else:
		_facing = "down" if _direction.y > 0 else "up"

func _check_encounter() -> void:
	if _current_encounter_zone == null:
		return
	if not _current_encounter_zone.has_method("check_encounter"):
		return
	var battle_data: Dictionary = _current_encounter_zone.check_encounter(self)
	if not battle_data.is_empty():
		_start_encounter(battle_data)

func _start_encounter(battle_data: Dictionary) -> void:
	# Battle data must be stored BEFORE the scene change so the
	# battle scene can pick it up in its _ready()
	GameManager.set_meta("pending_battle", battle_data)
	SceneTransition.change_scene("res://scenes/battle/battle_scene.tscn", "", 0.4)

func set_spawn_point(spawn_id: String) -> void:
	_spawn_point = spawn_id
	var spawn_node := get_tree().get_first_node_in_group("spawn_" + spawn_id)
	if spawn_node:
		global_position = spawn_node.global_position

func _pause_menu_open() -> bool:
	return _pause_menu != null and is_instance_valid(_pause_menu)

func _open_pause_menu() -> void:
	if _pause_menu_open():
		return
	var pause_scene: PackedScene = load("res://scenes/ui/pause_menu.tscn")
	if pause_scene == null:
		push_error("Player: could not load pause_menu.tscn")
		return
	_pause_menu = pause_scene.instantiate()
	# Overlay on top of the current scene; pause menu frees itself on close
	get_tree().root.add_child(_pause_menu)
	AudioManager.play_sfx("menu_confirm")

# ===== INTERACTION =====

func _unhandled_input(event: InputEvent) -> void:
	if BattleManager.in_battle or DialogueManager.is_active or _pause_menu_open():
		return
	if event.is_action_pressed("action_confirm") and _can_interact:
		_try_interact()

func _try_interact() -> void:
	var overlapping := interaction_area.get_overlapping_areas()
	for area in overlapping:
		var parent := area.get_parent()
		if parent and parent.has_method("interact"):
			parent.interact()
			return
	# Also check bodies (NPCs are physics bodies)
	for body in interaction_area.get_overlapping_bodies():
		if body != self and body.has_method("interact"):
			body.interact()
			return

# ===== ENCOUNTER ZONE TRACKING =====

func _on_encounter_zone_entered(zone: Area2D) -> void:
	_current_encounter_zone = zone
	_step_distance = 0.0

func _on_encounter_zone_exited(zone: Area2D) -> void:
	if _current_encounter_zone == zone:
		_current_encounter_zone = null

func _on_node_added(node: Node) -> void:
	if node.is_in_group("encounter_zone"):
		_connect_zone(node)

func _connect_zone(zone: Node) -> void:
	if not zone is Area2D:
		return
	if zone.has_meta("player_zone_connected"):
		return
	zone.set_meta("player_zone_connected", true)
	zone.body_entered.connect(_on_zone_body_entered.bind(zone))
	zone.body_exited.connect(_on_zone_body_exited.bind(zone))

func _on_zone_body_entered(body: Node, zone: Area2D) -> void:
	if body == self:
		_on_encounter_zone_entered(zone)

func _on_zone_body_exited(body: Node, zone: Area2D) -> void:
	if body == self:
		_on_encounter_zone_exited(zone)
