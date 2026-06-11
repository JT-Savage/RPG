extends Control
## SettingsMenu - music/SFX volume and back navigation.

@onready var music_slider: HSlider = $Panel/VBox/MusicRow/MusicSlider
@onready var sfx_slider: HSlider = $Panel/VBox/SFXRow/SFXSlider
@onready var back_button: Button = $Panel/VBox/BackButton

const SETTINGS_PATH := "user://settings.cfg"

func _ready() -> void:
	_load_settings()
	music_slider.value_changed.connect(_on_music_changed)
	sfx_slider.value_changed.connect(_on_sfx_changed)
	back_button.pressed.connect(_on_back)
	back_button.grab_focus()

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("action_cancel") or event.is_action_pressed("ui_cancel"):
		_on_back()

func _on_music_changed(value: float) -> void:
	AudioManager.set_music_volume(value)
	_save_settings()

func _on_sfx_changed(value: float) -> void:
	AudioManager.set_sfx_volume(value)
	AudioManager.play_sfx("menu_select")
	_save_settings()

func _on_back() -> void:
	AudioManager.play_sfx("menu_cancel")
	SceneTransition.change_scene("res://scenes/title/title_screen.tscn")

func _load_settings() -> void:
	var cfg := ConfigFile.new()
	if cfg.load(SETTINGS_PATH) == OK:
		music_slider.value = cfg.get_value("audio", "music", 0.8)
		sfx_slider.value = cfg.get_value("audio", "sfx", 0.8)
	else:
		music_slider.value = 0.8
		sfx_slider.value = 0.8
	AudioManager.set_music_volume(music_slider.value)
	AudioManager.set_sfx_volume(sfx_slider.value)

func _save_settings() -> void:
	var cfg := ConfigFile.new()
	cfg.set_value("audio", "music", music_slider.value)
	cfg.set_value("audio", "sfx", sfx_slider.value)
	cfg.save(SETTINGS_PATH)
