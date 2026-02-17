extends Control
## GameOverScreen

func _ready() -> void:
	AudioManager.play_music("game_over", 0.5)
	$Label.text = "GAME OVER"
	$Label.add_theme_font_size_override("font_size", 18)

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("action_confirm"):
		_load_last_save()
	elif event.is_action_pressed("action_cancel"):
		SceneTransition.change_scene("res://scenes/title/title_screen.tscn")

func _load_last_save() -> void:
	var success := false
	if SaveSystem.has_quicksave():
		success = SaveSystem.load_quicksave()
	elif SaveSystem.has_autosave():
		success = SaveSystem.load_autosave()

	if success:
		SceneTransition.change_scene(
			"res://scenes/locations/%s.tscn" % GameManager.current_location)
	else:
		SceneTransition.change_scene("res://scenes/title/title_screen.tscn")
