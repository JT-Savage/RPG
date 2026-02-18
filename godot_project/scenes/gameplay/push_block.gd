## push_block.gd
## A movable block for block-push puzzles.
## Player pushes it by walking into it; it slides one tile (16px).
## Emits position_changed signal for PuzzleSystem to check targets.
extends CharacterBody2D
class_name PushBlock

# ---------------------------------------------------------------------------
# Signals
# ---------------------------------------------------------------------------
signal position_changed

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
const TILE_SIZE: int = 16
const SLIDE_SPEED: float = 120.0

# ---------------------------------------------------------------------------
# Node refs
# ---------------------------------------------------------------------------
@onready var sprite: Sprite2D = $Sprite2D

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
var _sliding: bool = false
var _slide_target: Vector2


# ---------------------------------------------------------------------------
# _ready
# ---------------------------------------------------------------------------
func _ready() -> void:
	add_to_group("push_block")
	# Snap to grid on start
	position = position.snapped(Vector2(TILE_SIZE, TILE_SIZE))


# ---------------------------------------------------------------------------
# _physics_process
# ---------------------------------------------------------------------------
func _physics_process(delta: float) -> void:
	if not _sliding:
		return

	var dir: Vector2 = (_slide_target - global_position).normalized()
	var dist: float = global_position.distance_to(_slide_target)

	if dist <= SLIDE_SPEED * delta:
		global_position = _slide_target
		_sliding = false
		velocity = Vector2.ZERO
		emit_signal("position_changed")
	else:
		velocity = dir * SLIDE_SPEED

	move_and_slide()


# ---------------------------------------------------------------------------
# Public – called by player when they walk into the block
# ---------------------------------------------------------------------------
func try_push(push_direction: Vector2) -> bool:
	if _sliding:
		return false

	# Normalize to one of 4 directions
	var dir: Vector2 = _snap_direction(push_direction)
	var target: Vector2 = global_position + dir * TILE_SIZE

	# Check for obstacles at target
	var space := get_world_2d().direct_space_state
	var query := PhysicsRayQueryParameters2D.create(
		global_position,
		target + dir * 2.0,
		collision_mask
	)
	query.exclude = [self]
	var result := space.intersect_ray(query)

	if result:
		# Blocked – cannot push
		AudioManager.play_sfx("error")
		return false

	_slide_target = target
	_sliding = true
	AudioManager.play_sfx("puzzle_click")
	return true


func _snap_direction(d: Vector2) -> Vector2:
	if abs(d.x) >= abs(d.y):
		return Vector2(sign(d.x), 0)
	return Vector2(0, sign(d.y))
