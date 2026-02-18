## puzzle_system.gd
## Reusable puzzle framework for dungeon puzzles in "There Will Be Kobolds".
## Supports: pressure plates, push blocks, switch sequences, light beam deflection.
## Each puzzle is self-contained and emits solved() when complete.
extends Node
class_name PuzzleSystem

# ---------------------------------------------------------------------------
# Signals
# ---------------------------------------------------------------------------
signal solved(puzzle_id: String)
signal reset_puzzle(puzzle_id: String)

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------
@export var puzzle_id: String = ""
@export var puzzle_type: String = "pressure_plate"   # pressure_plate | block_push | switch_sequence | light_beam
@export var save_flag: String = ""                   # If set, puzzle stays solved across sessions

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
var _is_solved: bool = false
var _plate_states: Dictionary = {}         # plate_id -> bool
var _switch_sequence: Array[String] = []   # Required press order
var _switch_pressed: Array[String] = []    # Current press history
var _blocks: Array[Node] = []


# ---------------------------------------------------------------------------
# _ready
# ---------------------------------------------------------------------------
func _ready() -> void:
	if not save_flag.is_empty() and FlagManager.is_flag(save_flag):
		_is_solved = true
		_on_already_solved()
		return

	match puzzle_type:
		"pressure_plate":
			_setup_pressure_plates()
		"block_push":
			_setup_block_push()
		"switch_sequence":
			_setup_switch_sequence()
		"light_beam":
			_setup_light_beam()


# ---------------------------------------------------------------------------
# Pressure Plate Puzzle
# (All plates must be simultaneously activated to solve)
# ---------------------------------------------------------------------------
func _setup_pressure_plates() -> void:
	for child in get_children():
		if child.is_in_group("pressure_plate"):
			_plate_states[child.name] = false
			if child.has_signal("activated"):
				child.activated.connect(_on_plate_activated.bind(child.name))
			if child.has_signal("deactivated"):
				child.deactivated.connect(_on_plate_deactivated.bind(child.name))


func _on_plate_activated(plate_id: String) -> void:
	_plate_states[plate_id] = true
	_check_all_plates()


func _on_plate_deactivated(plate_id: String) -> void:
	_plate_states[plate_id] = false


func _check_all_plates() -> void:
	if _is_solved:
		return
	for plate_id in _plate_states:
		if not _plate_states[plate_id]:
			return
	_solve()


# ---------------------------------------------------------------------------
# Block Push Puzzle
# (Push blocks onto target markers to solve)
# ---------------------------------------------------------------------------
func _setup_block_push() -> void:
	_blocks = []
	for child in get_children():
		if child.is_in_group("push_block"):
			_blocks.append(child)
			if child.has_signal("position_changed"):
				child.position_changed.connect(_on_block_moved)


func _on_block_moved() -> void:
	if _is_solved:
		return
	_check_all_blocks_on_targets()


func _check_all_blocks_on_targets() -> void:
	var targets: Array = get_tree().get_nodes_in_group("block_target_" + puzzle_id)
	if targets.is_empty():
		return

	for target in targets:
		var covered: bool = false
		for block in _blocks:
			if block.global_position.distance_to(target.global_position) < 8.0:
				covered = true
				break
		if not covered:
			return
	_solve()


# ---------------------------------------------------------------------------
# Switch Sequence Puzzle
# (Switches must be pressed in correct order)
# ---------------------------------------------------------------------------
func _setup_switch_sequence() -> void:
	for child in get_children():
		if child.is_in_group("sequence_switch"):
			if child.has_signal("pressed"):
				child.pressed.connect(_on_switch_pressed.bind(child.name))

	# Sequence stored as metadata on this node (set in editor)
	if has_meta("required_sequence"):
		_switch_sequence = get_meta("required_sequence")


func _on_switch_pressed(switch_id: String) -> void:
	if _is_solved:
		return

	_switch_pressed.append(switch_id)
	var idx: int = _switch_pressed.size() - 1

	if idx >= _switch_sequence.size():
		_reset_sequence()
		return

	if _switch_pressed[idx] != _switch_sequence[idx]:
		AudioManager.play_sfx("puzzle_wrong")
		_reset_sequence()
		return

	AudioManager.play_sfx("puzzle_click")

	if _switch_pressed.size() == _switch_sequence.size():
		_solve()


func _reset_sequence() -> void:
	_switch_pressed.clear()
	emit_signal("reset_puzzle", puzzle_id)
	# Reset all switches visually
	for child in get_children():
		if child.is_in_group("sequence_switch") and child.has_method("reset"):
			child.reset()


# ---------------------------------------------------------------------------
# Light Beam Puzzle
# (Rotate mirrors to direct beam into receiver)
# ---------------------------------------------------------------------------
func _setup_light_beam() -> void:
	# Light beam puzzles use raycast-based beam tracing
	# Receivers emit signal when beam hits them
	for child in get_children():
		if child.is_in_group("beam_receiver"):
			if child.has_signal("beam_received"):
				child.beam_received.connect(_on_beam_received)


func _on_beam_received() -> void:
	# Count how many receivers have been hit
	var total: int = 0
	var hit: int = 0
	for child in get_children():
		if child.is_in_group("beam_receiver"):
			total += 1
			if child.has_method("is_active") and child.is_active():
				hit += 1
	if total > 0 and hit >= total:
		_solve()


# ---------------------------------------------------------------------------
# Solve
# ---------------------------------------------------------------------------
func _solve() -> void:
	if _is_solved:
		return
	_is_solved = true

	AudioManager.play_sfx("puzzle_solved")

	if not save_flag.is_empty():
		FlagManager.set_flag(save_flag, true)

	emit_signal("solved", puzzle_id)
	_on_solved()


func _on_solved() -> void:
	# Open doors, move obstacles, etc. – handled by child nodes in the group "puzzle_door_puzzle_id"
	for door in get_tree().get_nodes_in_group("puzzle_door_" + puzzle_id):
		if door.has_method("open"):
			door.open()
		elif door.has_node("AnimationPlayer"):
			door.get_node("AnimationPlayer").play("open")


func _on_already_solved() -> void:
	# Immediately put puzzle in solved state without animation
	for door in get_tree().get_nodes_in_group("puzzle_door_" + puzzle_id):
		if door.has_method("set_open"):
			door.set_open(true)
		else:
			door.visible = false
