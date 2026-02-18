extends Control

const SCROLL_SPEED: float = 30.0
const TITLE_SCENE: String = "res://scenes/title/title_screen.tscn"

@onready var credits_container: VBoxContainer = $CreditsContainer
@onready var animation_player: AnimationPlayer = $AnimationPlayer
@onready var skip_button: Button = $SkipButton

var scrolling: bool = false
var start_y: float = 0.0
var end_y: float = 0.0


func _ready() -> void:
	skip_button.pressed.connect(_on_skip_pressed)
	_start_scroll()


func _start_scroll() -> void:
	await get_tree().process_frame
	start_y = get_viewport_rect().size.y
	end_y = -credits_container.size.y - 32.0
	credits_container.position.y = start_y
	scrolling = true


func _process(delta: float) -> void:
	if not scrolling:
		return
	credits_container.position.y -= SCROLL_SPEED * delta
	if credits_container.position.y <= end_y:
		scrolling = false
		_finish_credits()


func _finish_credits() -> void:
	await get_tree().create_timer(1.5).timeout
	_go_to_title()


func _on_skip_pressed() -> void:
	scrolling = false
	_go_to_title()


func _go_to_title() -> void:
	if SceneManager:
		SceneManager.change_scene(TITLE_SCENE)
	else:
		get_tree().change_scene_to_file(TITLE_SCENE)
