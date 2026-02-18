## door.gd
## Locked/unlocked door for dungeons.
## Can require a key item, a flag condition, or a puzzle to be solved first.
extends Node2D
class_name Door

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------
@export var door_id: String = ""
@export var required_key_item: String = ""     # Key item ID needed, or empty
@export var required_flag: String = ""         # Flag that must be true, or empty
@export var destination_scene: String = ""     # If set, entering opens a new scene
@export var destination_spawn: String = "default"
@export var consume_key: bool = false          # If true, key item is removed on use

# ---------------------------------------------------------------------------
# Signals
# ---------------------------------------------------------------------------
signal door_opened

# ---------------------------------------------------------------------------
# Node refs
# ---------------------------------------------------------------------------
@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var area: Area2D = $Area2D
@onready var collision: CollisionShape2D = $StaticBody2D/CollisionShape2D
@onready var prompt_label: Label = $PromptLabel

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
var _is_open: bool = false
var _player_nearby: bool = false


# ---------------------------------------------------------------------------
# _ready
# ---------------------------------------------------------------------------
func _ready() -> void:
	if area:
		area.body_entered.connect(_on_body_entered)
		area.body_exited.connect(_on_body_exited)

	# Check if previously opened
	if not door_id.is_empty() and FlagManager.is_flag("door_open_" + door_id):
		set_open(true)
	elif sprite:
		sprite.play("closed")

	if prompt_label:
		prompt_label.visible = false


# ---------------------------------------------------------------------------
# _process
# ---------------------------------------------------------------------------
func _process(_delta: float) -> void:
	if _player_nearby and not _is_open and InputManager.is_action_just_pressed("ui_accept"):
		_try_open()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
func open() -> void:
	_open_door()

func set_open(value: bool) -> void:
	_is_open = value
	if collision:
		collision.disabled = value
	if sprite:
		sprite.play("open" if value else "closed")


# ---------------------------------------------------------------------------
# Private
# ---------------------------------------------------------------------------
func _try_open() -> void:
	# Check requirements
	if not required_key_item.is_empty():
		if not GameManager.has_key_item(required_key_item):
			var KeyDB = load("res://data/key_items/key_item_database.gd")
			var data: Dictionary = KeyDB.get_key_item(required_key_item) if KeyDB else {}
			var name_text: String = data.get("name", required_key_item)
			NotificationManager.show_message("Requires: %s" % name_text, Color(1.0, 0.5, 0.3))
			AudioManager.play_sfx("error")
			return
		if consume_key:
			GameManager.key_items.erase(required_key_item)

	if not required_flag.is_empty() and not FlagManager.is_flag(required_flag):
		NotificationManager.show_message("The door won't budge.", Color(0.7, 0.7, 0.7))
		AudioManager.play_sfx("error")
		return

	_open_door()


func _open_door() -> void:
	if _is_open:
		return

	AudioManager.play_sfx("door_open")
	set_open(true)

	if not door_id.is_empty():
		FlagManager.set_flag("door_open_" + door_id, true)

	emit_signal("door_opened")

	if not destination_scene.is_empty():
		await get_tree().create_timer(0.3).timeout
		SceneTransition.change_scene(destination_scene, destination_spawn)


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------
func _on_body_entered(body: Node) -> void:
	if body.is_in_group("player"):
		_player_nearby = true
		if not _is_open and prompt_label:
			var key_text: String = ""
			if not required_key_item.is_empty():
				key_text = " (Locked)"
			prompt_label.text = "[Z] Enter%s" % key_text
			prompt_label.visible = true

		# If door is already open and has destination, auto-enter
		if _is_open and not destination_scene.is_empty():
			SceneTransition.change_scene(destination_scene, destination_spawn)


func _on_body_exited(body: Node) -> void:
	if body.is_in_group("player"):
		_player_nearby = false
		if prompt_label:
			prompt_label.visible = false
