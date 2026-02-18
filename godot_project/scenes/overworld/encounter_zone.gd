extends Area2D
## EncounterZone - Manages random encounters in a map area

@export var encounter_rate: float = 0.12   # Chance per step (0.0–1.0)
@export var min_steps: int = 8             # Minimum steps before encounter possible
@export var background: String = "dungeon"
@export var battle_background: String = "dungeon"

# Enemy formations: each is an array of enemy dicts
@export var enemy_pool: Array = []

var _steps_since_last := 0

## Configure this zone from a Rect2, rate, pool, and background string.
## Called at runtime when zones are built procedurally from map data.
func configure(rect: Rect2, rate: float, pool: Array, bg: String) -> void:
	var shape_node: CollisionShape2D = $CollisionShape2D if has_node("CollisionShape2D") else null
	if shape_node == null:
		shape_node = CollisionShape2D.new()
		add_child(shape_node)
	var rect_shape := RectangleShape2D.new()
	rect_shape.size = rect.size
	shape_node.shape = rect_shape
	shape_node.position = rect.get_center()

	encounter_rate = rate
	enemy_pool = pool
	battle_background = bg
	background = bg
	min_steps = max(1, int(rect.get_area() / 256.0))


## Called each time the player takes a step inside this zone.
## player_node: the player Node (unused directly but available for future hooks).
## Returns a formation Dictionary (with "formation", "background", "music" keys)
## or an empty Dictionary if no encounter triggers.
func check_encounter(player_node: Node) -> Dictionary:
	_steps_since_last += 1
	if _steps_since_last < min_steps:
		return {}

	var effective_rate := _get_modified_rate()
	if randf() > effective_rate:
		return {}

	_steps_since_last = 0
	return _pick_formation()

func _get_modified_rate() -> float:
	var rate := encounter_rate

	# Story-based modifications
	if FlagManager.is_flag("kobolds_released") and not FlagManager.is_flag("desert_entered"):
		# 70% of encounters are infected kobolds
		rate *= 1.25   # More encounters in general

	if FlagManager.is_flag("desert_entered"):
		# Desert: harder enemies, slightly fewer encounters (they're tougher)
		rate *= 0.9

	return clamp(rate, 0.0, 1.0)

func _pick_formation() -> Dictionary:
	if enemy_pool.is_empty():
		return {}

	# Story-modified formation selection
	var available_pool := enemy_pool.duplicate()

	if FlagManager.is_flag("kobolds_released") and not FlagManager.is_flag("desert_entered"):
		# Weight toward infected kobold formations
		var kobold_formations := enemy_pool.filter(func(f): return f.get("type","") == "kobold")
		if not kobold_formations.is_empty():
			# 70% chance to pick a kobold formation
			if randf() < 0.70:
				available_pool = kobold_formations

	if FlagManager.is_flag("desert_entered"):
		# Desert: only desert formations
		var desert_formations := enemy_pool.filter(func(f): return f.get("region","") == "desert")
		if not desert_formations.is_empty():
			available_pool = desert_formations

	var chosen_pool: Dictionary = available_pool[randi() % available_pool.size()]

	# Apply music track for battle
	var music_track := "battle"
	if FlagManager.is_flag("kobolds_released") and not FlagManager.is_flag("desert_entered"):
		music_track = "battle_kobold_heavy"

	return {
		"formation": chosen_pool.get("enemies", []),
		"background": battle_background,
		"music": music_track,
	}
