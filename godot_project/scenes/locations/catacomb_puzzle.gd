## catacomb_puzzle.gd
## The catacomb pressure-plate puzzle in CatacombDepths.
## Three pressure plates must all be simultaneously activated by push blocks
## to open the door to the deeper chamber (and catacomb_lich boss).
## Puzzle difficulty: FF6-level. Blocks are in fixed positions; player must
## route them to each plate without pushing them into walls.
extends Node2D
class_name CatacombPuzzle

# ---------------------------------------------------------------------------
# Node refs
# ---------------------------------------------------------------------------
@onready var puzzle_system = $PuzzleSystem
@onready var door_to_depths = $DoorToDepths
@onready var plate_a: Area2D = $PlateA
@onready var plate_b: Area2D = $PlateB
@onready var plate_c: Area2D = $PlateC
@onready var block_1: CharacterBody2D = $Block1
@onready var block_2: CharacterBody2D = $Block2
@onready var block_3: CharacterBody2D = $Block3
@onready var hint_label: Label = $UI/HintLabel
@onready var reset_button_area: Area2D = $ResetSkull


# ---------------------------------------------------------------------------
# Block start positions (for reset)
# ---------------------------------------------------------------------------
const BLOCK_START_POSITIONS: Array[Vector2] = [
	Vector2(64, 48),
	Vector2(80, 80),
	Vector2(48, 96)
]

const PLATE_POSITIONS: Array[Vector2] = [
	Vector2(128, 48),
	Vector2(128, 80),
	Vector2(128, 96)
]


# ---------------------------------------------------------------------------
# _ready
# ---------------------------------------------------------------------------
func _ready() -> void:
	add_to_group("catacomb_puzzle")

	# Check if already solved
	if FlagManager.is_flag("catacomb_puzzle_solved"):
		_apply_solved_state()
		return

	# Set up puzzle system
	if puzzle_system:
		puzzle_system.puzzle_id = "catacomb_depths_main"
		puzzle_system.puzzle_type = "block_push"
		puzzle_system.save_flag = "catacomb_puzzle_solved"
		puzzle_system.solved.connect(_on_puzzle_solved)

	# Position blocks at start positions
	_reset_blocks()

	# Show hint on first visit
	if not FlagManager.is_flag("catacomb_puzzle_seen"):
		FlagManager.set_flag("catacomb_puzzle_seen", true)
		_show_hint()

	# Reset skull (interact to reset puzzle)
	if reset_button_area:
		reset_button_area.body_entered.connect(_on_reset_skull_enter)


# ---------------------------------------------------------------------------
# Public
# ---------------------------------------------------------------------------
func reset_puzzle() -> void:
	_reset_blocks()
	if puzzle_system and puzzle_system.has_method("_reset_sequence"):
		puzzle_system._reset_sequence()
	AudioManager.play_sfx("puzzle_wrong")
	_show_hint()


# ---------------------------------------------------------------------------
# Private
# ---------------------------------------------------------------------------
func _reset_blocks() -> void:
	if block_1:
		block_1.global_position = BLOCK_START_POSITIONS[0]
	if block_2:
		block_2.global_position = BLOCK_START_POSITIONS[1]
	if block_3:
		block_3.global_position = BLOCK_START_POSITIONS[2]


func _show_hint() -> void:
	if not hint_label:
		return
	hint_label.text = "Three plates. Three stones.\nInteract with the skull to reset."
	hint_label.visible = true
	# Hide after 4 seconds
	var timer: SceneTreeTimer = get_tree().create_timer(4.0)
	timer.timeout.connect(hint_label.hide)


func _on_puzzle_solved(_puzzle_id: String) -> void:
	_apply_solved_state()
	NotificationManager.show_message("The stone door grinds open...", Color(0.8, 0.9, 1.0))


func _apply_solved_state() -> void:
	# Remove the door blocking the lich chamber
	if door_to_depths and door_to_depths.has_method("set_open"):
		door_to_depths.set_open(true)
	elif door_to_depths:
		door_to_depths.visible = false


func _on_reset_skull_enter(body: Node) -> void:
	if body.is_in_group("player") and InputManager.is_action_just_pressed("ui_accept"):
		reset_puzzle()
