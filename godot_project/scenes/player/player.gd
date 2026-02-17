extends CharacterBody2D
## Player - 4-directional movement, encounters, interaction

const SPEED := 80.0
const TILE_SIZE := 16

@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var camera: Camera2D = $Camera2D
@onready var interaction_area: Area2D = $InteractionArea
@onready var encounter_timer: Timer = $EncounterTimer

var _direction := Vector2.ZERO
var _facing := "down"
var _is_moving := false
var _step_count := 0
var _current_encounter_zone: Area2D = null
var _can_interact := true
var _spawn_point := ""

# Pixel-perfect: snap position to integer
func _process(_delta: float) -> void:
	global_position = global_position.round()

	# Quicksave shortcut
	if Input.is_action_just_pressed("action_quicksave") and not BattleManager.in_battle:
		SaveSystem.quicksave()

	# Menu shortcut
	if Input.is_action_just_pressed("action_menu") and not BattleManager.in_battle:
		_open_pause_menu()

func _physics_process(delta: float) -> void:
	if BattleManager.in_battle or DialogueManager.is_active:
		velocity = Vector2.ZERO
		animated_sprite.play(_facing + "_idle")
		return

	_direction = InputManager.get_direction()

	if _direction != Vector2.ZERO:
		velocity = _direction * SPEED
		_update_facing()
		_is_moving = true
		animated_sprite.play(_facing + "_walk")

		# Step counter for encounters
		if not encounter_timer.is_stopped():
			pass
		_step_count += 1
		_check_encounter()
	else:
		velocity = Vector2.ZERO
		_is_moving = false
		animated_sprite.play(_facing + "_idle")

	move_and_slide()

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
	var battle_data = _current_encounter_zone.check_encounter(_step_count)
	if battle_data != null:
		_step_count = 0
		_start_encounter(battle_data)

func _start_encounter(battle_data: Dictionary) -> void:
	SceneTransition.change_scene("res://scenes/battle/battle_scene.tscn", "", 0.4)
	# Battle data stored for battle scene to pick up
	GameManager.set_meta("pending_battle", battle_data)

func set_spawn_point(spawn_id: String) -> void:
	_spawn_point = spawn_id
	var spawn_node := get_tree().get_first_node_in_group("spawn_" + spawn_id)
	if spawn_node:
		global_position = spawn_node.global_position

func _open_pause_menu() -> void:
	get_tree().change_scene_to_file("res://scenes/ui/pause_menu.tscn")

# ===== INTERACTION =====

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("action_confirm") and _can_interact:
		_try_interact()

func _try_interact() -> void:
	var overlapping := interaction_area.get_overlapping_areas()
	for area in overlapping:
		var parent := area.get_parent()
		if parent.has_method("interact"):
			parent.interact(self)
			return

# ===== ENCOUNTER ZONE TRACKING =====

func _on_encounter_zone_entered(zone: Area2D) -> void:
	_current_encounter_zone = zone
	_step_count = 0

func _on_encounter_zone_exited(zone: Area2D) -> void:
	if _current_encounter_zone == zone:
		_current_encounter_zone = null

func _ready() -> void:
	add_to_group("player")
	camera.position_smoothing_enabled = true
	camera.position_smoothing_speed = 5.0

	# Connect to encounter zones at scene level
	get_tree().connect("node_added", _on_node_added)

func _on_node_added(node: Node) -> void:
	if node.is_in_group("encounter_zone"):
		node.body_entered.connect(func(_b): _on_encounter_zone_entered(node))
		node.body_exited.connect(func(_b): _on_encounter_zone_exited(node))
