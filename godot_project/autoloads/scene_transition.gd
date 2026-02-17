extends CanvasLayer
## SceneTransition - Fade in/out, scene changes with spawn points

var fade_rect: ColorRect
var is_transitioning := false
var pending_scene := ""
var pending_spawn := ""

signal transition_completed

func _ready() -> void:
	layer = 100  # Always on top
	fade_rect = ColorRect.new()
	fade_rect.color = Color.BLACK
	fade_rect.anchors_preset = Control.PRESET_FULL_RECT
	fade_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	fade_rect.modulate.a = 0.0
	add_child(fade_rect)

func change_scene(scene_path: String, spawn_point: String = "", fade_duration: float = 0.5) -> void:
	if is_transitioning:
		return
	is_transitioning = true
	pending_scene = scene_path
	pending_spawn = spawn_point

	await _fade_out(fade_duration)

	# Load and switch scene
	var err := get_tree().change_scene_to_file(scene_path)
	if err != OK:
		push_error("SceneTransition: Failed to load scene '%s'" % scene_path)
		is_transitioning = false
		return

	await get_tree().process_frame
	await get_tree().process_frame

	# Signal spawn point to the new scene's player
	if pending_spawn != "":
		var player := get_tree().get_first_node_in_group("player")
		if player and player.has_method("set_spawn_point"):
			player.set_spawn_point(pending_spawn)

	await _fade_in(fade_duration)
	is_transitioning = false
	transition_completed.emit()

func fade_out(duration: float = 0.5) -> void:
	await _fade_out(duration)

func fade_in(duration: float = 0.5) -> void:
	await _fade_in(duration)

func _fade_out(duration: float) -> void:
	var tween := create_tween()
	tween.tween_property(fade_rect, "modulate:a", 1.0, duration)
	await tween.finished

func _fade_in(duration: float) -> void:
	var tween := create_tween()
	tween.tween_property(fade_rect, "modulate:a", 0.0, duration)
	await tween.finished

func flash(color: Color = Color.WHITE, duration: float = 0.3) -> void:
	fade_rect.color = color
	fade_rect.modulate.a = 1.0
	var tween := create_tween()
	tween.tween_property(fade_rect, "modulate:a", 0.0, duration)
	await tween.finished
	fade_rect.color = Color.BLACK
