extends Node
## InputManager - Abstracts keyboard, gamepad, and touch input

signal action_pressed(action: String)
signal action_released(action: String)
signal direction_changed(direction: Vector2)

var is_mobile: bool = false
var touch_controls_visible: bool = false
var current_direction: Vector2 = Vector2.ZERO

# Virtual control state (from TouchScreenButtons)
var _virtual_up := false
var _virtual_down := false
var _virtual_left := false
var _virtual_right := false
var _virtual_confirm := false
var _virtual_cancel := false
var _virtual_menu := false
var _virtual_quicksave := false

func _ready() -> void:
	is_mobile = GameManager.is_mobile
	touch_controls_visible = is_mobile
	_setup_input_map()

func _setup_input_map() -> void:
	# Ensure all actions exist in InputMap
	var actions := ["move_up","move_down","move_left","move_right",
					"action_confirm","action_cancel","action_menu","action_quicksave"]
	for action in actions:
		if not InputMap.has_action(action):
			InputMap.add_action(action)

func _process(_delta: float) -> void:
	_update_direction()

func _update_direction() -> void:
	var dir := Vector2.ZERO

	# Keyboard/Gamepad
	if Input.is_action_pressed("move_up") or _virtual_up:
		dir.y -= 1
	if Input.is_action_pressed("move_down") or _virtual_down:
		dir.y += 1
	if Input.is_action_pressed("move_left") or _virtual_left:
		dir.x -= 1
	if Input.is_action_pressed("move_right") or _virtual_right:
		dir.x += 1

	if dir != current_direction:
		current_direction = dir.normalized() if dir != Vector2.ZERO else Vector2.ZERO
		direction_changed.emit(current_direction)

func is_action_pressed(action: String) -> bool:
	match action:
		"action_confirm": return Input.is_action_pressed("action_confirm") or _virtual_confirm
		"action_cancel": return Input.is_action_pressed("action_cancel") or _virtual_cancel
		"action_menu": return Input.is_action_pressed("action_menu") or _virtual_menu
		"action_quicksave": return Input.is_action_pressed("action_quicksave") or _virtual_quicksave
		"move_up": return Input.is_action_pressed("move_up") or _virtual_up
		"move_down": return Input.is_action_pressed("move_down") or _virtual_down
		"move_left": return Input.is_action_pressed("move_left") or _virtual_left
		"move_right": return Input.is_action_pressed("move_right") or _virtual_right
	return Input.is_action_pressed(action)

func is_action_just_pressed(action: String) -> bool:
	return Input.is_action_just_pressed(action)

func get_direction() -> Vector2:
	return current_direction

# Called by virtual control buttons
func set_virtual_input(action: String, pressed: bool) -> void:
	match action:
		"up": _virtual_up = pressed
		"down": _virtual_down = pressed
		"left": _virtual_left = pressed
		"right": _virtual_right = pressed
		"confirm": _virtual_confirm = pressed
		"cancel": _virtual_cancel = pressed
		"menu": _virtual_menu = pressed
		"quicksave": _virtual_quicksave = pressed

func show_touch_controls() -> void:
	touch_controls_visible = true
	var controls := get_tree().get_first_node_in_group("virtual_controls")
	if controls:
		controls.visible = true

func hide_touch_controls() -> void:
	touch_controls_visible = false
	var controls := get_tree().get_first_node_in_group("virtual_controls")
	if controls:
		controls.visible = false
