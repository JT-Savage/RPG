extends Control
## TitleScreen - Main menu with New Game, Continue, Load, Settings, Credits

@onready var menu_container: VBoxContainer = $MenuContainer
@onready var title_label: Label = $TitleLabel
@onready var cursor: Sprite2D = $Cursor
@onready var version_label: Label = $VersionLabel

var _options: Array = []
var _cursor_index := 0
var _ng_plus_available := false

func _ready() -> void:
	AudioManager.play_music("title", 0.5)
	AdManager.show_banner()

	_ng_plus_available = SaveSystem.has_ng_plus_data()
	_build_menu()

	version_label.text = "v1.0.0"

func _build_menu() -> void:
	_options = ["New Game"]

	if SaveSystem.has_autosave() or SaveSystem.has_quicksave():
		_options.append("Continue")

	_options.append("Load Game")
	_options.append("Settings")
	_options.append("Credits")

	if OS.get_name() not in ["Android", "iOS"]:
		_options.append("Quit")

	for child in menu_container.get_children():
		child.queue_free()

	for option in _options:
		var lbl := Label.new()
		lbl.text = option
		lbl.add_theme_font_size_override("font_size", 10)
		lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		menu_container.add_child(lbl)

	_cursor_index = 0
	_update_cursor()

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("move_up"):
		_cursor_index = (_cursor_index - 1 + _options.size()) % _options.size()
		_update_cursor()
		AudioManager.play_sfx("menu_select")

	elif event.is_action_pressed("move_down"):
		_cursor_index = (_cursor_index + 1) % _options.size()
		_update_cursor()
		AudioManager.play_sfx("menu_select")

	elif event.is_action_pressed("action_confirm"):
		_confirm_option()
		AudioManager.play_sfx("menu_confirm")

func _confirm_option() -> void:
	var selected: String = _options[_cursor_index]
	match selected:
		"New Game":
			_start_new_game()
		"Continue":
			_quick_continue()
		"Load Game":
			SceneTransition.change_scene("res://scenes/title/save_select_screen.tscn")
		"Settings":
			SceneTransition.change_scene("res://scenes/ui/settings_menu.tscn")
		"Credits":
			SceneTransition.change_scene("res://scenes/ui/credits_screen.tscn")
		"Quit":
			get_tree().quit()

func _start_new_game() -> void:
	if _ng_plus_available:
		# Offer New Game+
		_show_ng_plus_prompt()
	else:
		_begin_new_game({})

func _show_ng_plus_prompt() -> void:
	# Simple two-option prompt
	var dialog := AcceptDialog.new()
	dialog.title = "New Game+"
	dialog.dialog_text = "A completed save was found.\nStart New Game+ with bonus content?"
	dialog.ok_button_text = "New Game+"
	dialog.add_cancel_button("Normal New Game")
	add_child(dialog)
	dialog.popup_centered()

	dialog.confirmed.connect(func():
		var ng_data := SaveSystem.load_ng_plus_data()
		_begin_new_game(ng_data)
	)
	dialog.canceled.connect(func():
		_begin_new_game({})
	)

func _begin_new_game(ng_plus_data: Dictionary) -> void:
	GameManager.new_game(ng_plus_data)
	SceneTransition.change_scene("res://scenes/locations/tutorial_warren.tscn", "start")

func _quick_continue() -> void:
	var success := false
	if SaveSystem.has_quicksave():
		success = SaveSystem.load_quicksave()
	elif SaveSystem.has_autosave():
		success = SaveSystem.load_autosave()

	if success:
		var location: String = GameManager.current_location
		SceneTransition.change_scene("res://scenes/locations/%s.tscn" % location)
	else:
		_build_menu()  # Refresh if load failed

func _update_cursor() -> void:
	var children := menu_container.get_children()
	if children.is_empty():
		return
	var idx := clamp(_cursor_index, 0, children.size() - 1)
	var target: Control = children[idx]
	cursor.global_position = Vector2(
		target.global_position.x - 12,
		target.global_position.y + target.size.y / 2
	)
