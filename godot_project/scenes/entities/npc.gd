## npc.gd
## Generic NPC node for "There Will Be Kobolds".
## All interactive characters in locations use this scene.
## NPCs can show dialogue, trigger recruitment, block paths, or do nothing.
extends CharacterBody2D
class_name NPC

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------
@export var npc_id: String = ""
@export var dialogue_id: String = ""
@export var face_direction: Vector2 = Vector2.DOWN
@export var wander: bool = false
@export var wander_radius: float = 48.0
@export var cutscene_id: String = ""
@export var trigger_proximity: float = 0.0   # 0 = interaction only, >0 = proximity trigger

# ---------------------------------------------------------------------------
# Node refs
# ---------------------------------------------------------------------------
@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var interaction_area: Area2D = $InteractionArea
@onready var collision: CollisionShape2D = $CollisionShape2D

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
var _base_position: Vector2
var _wander_target: Vector2
var _wander_timer: float = 0.0
var _player_in_range: bool = false
var _cutscene_triggered: bool = false

const WANDER_SPEED: float = 25.0
const WANDER_WAIT_MIN: float = 1.5
const WANDER_WAIT_MAX: float = 4.0


# ---------------------------------------------------------------------------
# _ready
# ---------------------------------------------------------------------------
func _ready() -> void:
	_base_position = global_position
	_wander_target = global_position
	_wander_timer = randf_range(WANDER_WAIT_MIN, WANDER_WAIT_MAX)

	if sprite:
		_set_direction(face_direction)

	if interaction_area:
		interaction_area.body_entered.connect(_on_body_entered)
		interaction_area.body_exited.connect(_on_body_exited)

	# Configure from NPC database if available
	if not npc_id.is_empty():
		_init_from_database()


func init_from_id(id: String) -> void:
	npc_id = id
	_init_from_database()


func _init_from_database() -> void:
	# NPC data would come from a data file; basic fallback here
	var npc_data: Dictionary = _get_npc_data(npc_id)
	if npc_data.is_empty():
		return
	if "dialogue" in npc_data and dialogue_id.is_empty():
		dialogue_id = npc_data["dialogue"]
	if "sprite" in npc_data and sprite:
		var frames_path: String = "res://assets/sprites/characters/%s.png" % npc_data["sprite"]
		if ResourceLoader.exists(frames_path):
			var tex: Texture2D = load(frames_path)
			sprite.texture = tex


func _get_npc_data(id: String) -> Dictionary:
	# Inline minimal NPC registry; expand as needed
	var registry: Dictionary = {
		"kobold_merchant": { "sprite": "kobold_npc", "dialogue": "kobold_merchant_shop" },
		"kobold_elder": { "sprite": "kobold_elder", "dialogue": "kobold_elder_talk" },
		"kobold_children": { "sprite": "kobold_child", "dialogue": "kobold_children_play" },
		"kella": { "sprite": "kella", "dialogue": "" },
		"druidess_elder": { "sprite": "elder_npc", "dialogue": "druidess_elder_talk" },
		"escaped_slave": { "sprite": "villager_npc", "dialogue": "escaped_slave_talk" }
	}
	return registry.get(id, {})


# ---------------------------------------------------------------------------
# _physics_process
# ---------------------------------------------------------------------------
func _physics_process(delta: float) -> void:
	if wander:
		_process_wander(delta)

	if trigger_proximity > 0.0 and not _cutscene_triggered:
		_check_proximity_trigger()

	move_and_slide()


func _process_wander(delta: float) -> void:
	_wander_timer -= delta
	if _wander_timer <= 0.0:
		# Pick a new wander target within radius of base position
		var angle: float = randf() * TAU
		var dist: float = randf() * wander_radius
		_wander_target = _base_position + Vector2(cos(angle), sin(angle)) * dist
		_wander_timer = randf_range(WANDER_WAIT_MIN, WANDER_WAIT_MAX)

	var dir: Vector2 = (_wander_target - global_position)
	if dir.length() > 4.0:
		velocity = dir.normalized() * WANDER_SPEED
		_set_direction(dir.normalized())
	else:
		velocity = Vector2.ZERO


func _check_proximity_trigger() -> void:
	var player_nodes: Array = get_tree().get_nodes_in_group("player")
	if player_nodes.is_empty():
		return
	var player: Node = player_nodes[0]
	if global_position.distance_to(player.global_position) <= trigger_proximity:
		_trigger_cutscene()


func _trigger_cutscene() -> void:
	if _cutscene_triggered:
		return
	_cutscene_triggered = true
	if cutscene_id.is_empty():
		return
	if DialogueManager and DialogueManager.has_method("start_dialogue"):
		DialogueManager.start_dialogue(cutscene_id)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
func set_opened(opened: bool) -> void:
	# For chest NPCs
	if sprite:
		sprite.play("open" if opened else "closed")


func set_enabled(enabled: bool) -> void:
	collision.disabled = not enabled
	if interaction_area:
		interaction_area.monitoring = enabled


func force_cutscene() -> void:
	_trigger_cutscene()


# ---------------------------------------------------------------------------
# Interaction
# ---------------------------------------------------------------------------
func interact() -> void:
	if not dialogue_id.is_empty():
		if DialogueManager and DialogueManager.has_method("start_dialogue"):
			DialogueManager.start_dialogue(dialogue_id)
	elif not cutscene_id.is_empty():
		_trigger_cutscene()


func _on_body_entered(body: Node) -> void:
	if body.is_in_group("player"):
		_player_in_range = true


func _on_body_exited(body: Node) -> void:
	if body.is_in_group("player"):
		_player_in_range = false


func _set_direction(dir: Vector2) -> void:
	if not sprite:
		return
	if abs(dir.y) >= abs(dir.x):
		sprite.play("walk_down" if dir.y > 0 else "walk_up")
	else:
		sprite.play("walk_right" if dir.x > 0 else "walk_left")
		sprite.flip_h = dir.x < 0
