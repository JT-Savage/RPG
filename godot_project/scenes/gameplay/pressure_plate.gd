## pressure_plate.gd
## A pressure plate that activates when a heavy object (push block or player)
## stands on it, and deactivates when the object leaves.
## Add to group "pressure_plate" for PuzzleSystem to discover it.
extends Area2D
class_name PressurePlate

# ---------------------------------------------------------------------------
# Signals
# ---------------------------------------------------------------------------
signal activated
signal deactivated

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------
@export var require_block: bool = true   # If true, only push blocks activate it (not player)
@export var stay_active: bool = false    # If true, plate locks active once triggered

# ---------------------------------------------------------------------------
# Node refs
# ---------------------------------------------------------------------------
@onready var sprite: Sprite2D = $Sprite2D

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
var _active: bool = false
var _bodies_on: int = 0

const COLOR_INACTIVE: Color = Color(0.5, 0.5, 0.5)
const COLOR_ACTIVE: Color   = Color(0.3, 0.8, 0.3)


# ---------------------------------------------------------------------------
# _ready
# ---------------------------------------------------------------------------
func _ready() -> void:
	add_to_group("pressure_plate")
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)
	_update_visual()


# ---------------------------------------------------------------------------
# Public
# ---------------------------------------------------------------------------
func is_active() -> bool:
	return _active


# ---------------------------------------------------------------------------
# Private
# ---------------------------------------------------------------------------
func _on_body_entered(body: Node) -> void:
	if stay_active and _active:
		return

	if require_block and not body.is_in_group("push_block"):
		return

	if not require_block and not (body.is_in_group("push_block") or body.is_in_group("player")):
		return

	_bodies_on += 1
	if _bodies_on == 1:
		_set_active(true)


func _on_body_exited(body: Node) -> void:
	if stay_active and _active:
		return

	if require_block and not body.is_in_group("push_block"):
		return

	if not require_block and not (body.is_in_group("push_block") or body.is_in_group("player")):
		return

	_bodies_on = max(0, _bodies_on - 1)
	if _bodies_on == 0:
		_set_active(false)


func _set_active(value: bool) -> void:
	if _active == value:
		return
	_active = value
	_update_visual()
	AudioManager.play_sfx("puzzle_click")
	if _active:
		emit_signal("activated")
	else:
		emit_signal("deactivated")


func _update_visual() -> void:
	if sprite:
		sprite.modulate = COLOR_ACTIVE if _active else COLOR_INACTIVE
