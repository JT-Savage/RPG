## chest.gd
## Treasure chest node for all locations.
## Shows closed/open sprite, plays animation, grants item, sets flag.
extends Node2D
class_name Chest

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------
@export var chest_id: String = ""          # Unique ID for this chest (used as save flag)
@export var item_type: String = "item"     # "item", "key_item", "equipment", "gil"
@export var item_id: String = ""           # Item/equipment ID
@export var quantity: int = 1             # For regular items / gil amount
@export var one_time: bool = true         # If false, chest respawns (rare)

# ---------------------------------------------------------------------------
# Signals
# ---------------------------------------------------------------------------
signal interacted

# ---------------------------------------------------------------------------
# Node refs
# ---------------------------------------------------------------------------
@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var area: Area2D = $Area2D
@onready var prompt_label: Label = $PromptLabel

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
var _opened: bool = false
var _player_nearby: bool = false


# ---------------------------------------------------------------------------
# _ready
# ---------------------------------------------------------------------------
func _ready() -> void:
	if area:
		area.body_entered.connect(_on_body_entered)
		area.body_exited.connect(_on_body_exited)

	if prompt_label:
		prompt_label.visible = false

	# Check if already opened
	if one_time and not chest_id.is_empty():
		_opened = FlagManager.is_flag("chest_" + chest_id)

	if _opened:
		set_opened(true)
	elif sprite:
		sprite.play("closed")


# ---------------------------------------------------------------------------
# _process
# ---------------------------------------------------------------------------
func _process(_delta: float) -> void:
	if _player_nearby and not _opened and InputManager.is_action_just_pressed("ui_accept"):
		_open()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
func set_opened(opened: bool) -> void:
	_opened = opened
	if sprite:
		sprite.play("open" if opened else "closed")
	if prompt_label:
		prompt_label.visible = false


func set_enabled(enabled: bool) -> void:
	if area:
		area.monitoring = enabled
		area.monitorable = enabled


# ---------------------------------------------------------------------------
# Private
# ---------------------------------------------------------------------------
func _open() -> void:
	if _opened:
		return

	_opened = true

	# Play animation
	AudioManager.play_sfx("chest_open")
	if sprite:
		sprite.play("opening")
		await sprite.animation_finished
		sprite.play("open")

	# Grant reward
	match item_type:
		"item":
			if not item_id.is_empty():
				GameManager.add_item(item_id, quantity)
				NotificationManager.show_item(item_id, quantity)
		"key_item":
			if not item_id.is_empty():
				GameManager.add_key_item(item_id)
				NotificationManager.show_key_item(item_id)
		"equipment":
			if not item_id.is_empty():
				GameManager.add_equipment(item_id)
				NotificationManager.show_item(item_id, 1)
		"gil":
			GameManager.earn_gil(quantity)
			NotificationManager.show_gil(quantity)

	# Save opened state
	if one_time and not chest_id.is_empty():
		FlagManager.set_flag("chest_" + chest_id, true)

	if prompt_label:
		prompt_label.visible = false

	emit_signal("interacted")


# ---------------------------------------------------------------------------
# Collision callbacks
# ---------------------------------------------------------------------------
func _on_body_entered(body: Node) -> void:
	if body.is_in_group("player") and not _opened:
		_player_nearby = true
		if prompt_label:
			prompt_label.text = "[Z] Open"
			prompt_label.visible = true


func _on_body_exited(body: Node) -> void:
	if body.is_in_group("player"):
		_player_nearby = false
		if prompt_label:
			prompt_label.visible = false
