## save_point.gd
## Crystal save point. Player walks into interaction area to open save menu.
## Emits save_requested signal; parent location handles the save UI.
extends Node2D
class_name SavePoint

# ---------------------------------------------------------------------------
# Signals
# ---------------------------------------------------------------------------
signal save_requested

# ---------------------------------------------------------------------------
# Node refs
# ---------------------------------------------------------------------------
@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var area: Area2D = $Area2D
@onready var prompt_label: Label = $PromptLabel
@onready var glow_light: PointLight2D = $PointLight2D

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
var _player_nearby: bool = false
const GLOW_COLORS: Array[Color] = [
	Color(0.4, 0.6, 1.0, 0.8),
	Color(0.6, 0.8, 1.0, 1.0),
]
var _glow_phase: float = 0.0


# ---------------------------------------------------------------------------
# _ready
# ---------------------------------------------------------------------------
func _ready() -> void:
	if area:
		area.body_entered.connect(_on_body_entered)
		area.body_exited.connect(_on_body_exited)
	if prompt_label:
		prompt_label.visible = false
	if sprite:
		sprite.play("idle")


# ---------------------------------------------------------------------------
# _process
# ---------------------------------------------------------------------------
func _process(delta: float) -> void:
	# Animate glow
	_glow_phase += delta * 1.5
	if glow_light:
		var t: float = (sin(_glow_phase) + 1.0) * 0.5
		glow_light.color = GLOW_COLORS[0].lerp(GLOW_COLORS[1], t)
		glow_light.energy = 0.8 + t * 0.4

	if _player_nearby and InputManager.is_action_just_pressed("ui_accept"):
		_activate()


# ---------------------------------------------------------------------------
# Interaction
# ---------------------------------------------------------------------------
func _activate() -> void:
	AudioManager.play_sfx("save_point")
	if sprite:
		sprite.play("activated")

	# Full heal
	PartyManager.restore_all_hp_mp()

	emit_signal("save_requested")
	show_save_ui()


func show_save_ui() -> void:
	SaveSystem.open_save_menu()


# ---------------------------------------------------------------------------
# Signal handlers
# ---------------------------------------------------------------------------
func _on_body_entered(body: Node) -> void:
	if body.is_in_group("player"):
		_player_nearby = true
		if prompt_label:
			prompt_label.text = "[Z] Save"
			prompt_label.visible = true
		if sprite:
			sprite.play("active")


func _on_body_exited(body: Node) -> void:
	if body.is_in_group("player"):
		_player_nearby = false
		if prompt_label:
			prompt_label.visible = false
		if sprite:
			sprite.play("idle")
