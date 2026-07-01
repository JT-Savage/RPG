extends Node2D
## BattleScene - Main battle UI, connects to BattleManager signals

@onready var background_sprite: Sprite2D = $Background
@onready var party_ui: Control = $UI/PartyPanel
@onready var enemy_ui: Control = $UI/EnemyPanel
@onready var command_menu = $UI/CommandMenu
@onready var message_label: Label = $UI/MessageLabel
@onready var damage_container: Control = $UI/DamageNumbers
@onready var portraits_panel: Control = $UI/Portraits

var _active_actor_id: String = ""
var _battle_data: Dictionary = {}
var _enemy_slots: Array = []
var _party_slots: Array = []
var _waiting_for_input := false
var _banter_popup = null

func _ready() -> void:
	# Get pending battle data
	if GameManager.has_meta("pending_battle"):
		_battle_data = GameManager.get_meta("pending_battle")
		GameManager.remove_meta("pending_battle")

	# Connect BattleManager signals
	BattleManager.turn_ready.connect(_on_turn_ready)
	BattleManager.damage_dealt.connect(_on_damage_dealt)
	BattleManager.character_ko.connect(_on_character_ko)
	BattleManager.enemy_ko.connect(_on_enemy_ko)
	BattleManager.battle_ended.connect(_on_battle_ended)
	BattleManager.status_applied.connect(_on_status_applied)
	BattleManager.status_removed.connect(_on_status_removed)

	# Hide command menu initially and connect its signal
	command_menu.visible = false
	command_menu.action_selected.connect(_on_command_selected)

	# Set background
	var bg_name: String = _battle_data.get("background", "dungeon")
	var bg_path := "res://assets/backgrounds/battle_%s.png" % bg_name
	if ResourceLoader.exists(bg_path):
		background_sprite.texture = load(bg_path)

	# Start the battle
	var formation: Array = _battle_data.get("formation", [])
	var bg: String = _battle_data.get("background", "dungeon")
	BattleManager.start_battle(formation, bg)

	# Reset banter system for a fresh battle
	BanterSystem.reset_for_battle()

	# Instantiate banter popup overlay
	var popup_scene := load("res://scenes/ui/banter_popup.tscn")
	if popup_scene:
		_banter_popup = popup_scene.instantiate()
		add_child(_banter_popup)

	# Build UI slots
	_build_party_ui()
	_build_enemy_ui()

	# Play battle music
	var music: String = _battle_data.get("music", "battle")
	AudioManager.play_music(music)

# ===== UI BUILDING =====

func _build_party_ui() -> void:
	_party_slots.clear()
	for child in party_ui.get_children():
		child.queue_free()

	var party := GameManager.get_active_characters()
	for i in party.size():
		var char_id: String = party[i]
		var slot := _create_party_slot(char_id, i)
		party_ui.add_child(slot)
		_party_slots.append(slot)

func _create_party_slot(char_id: String, slot_index: int) -> Control:
	var container := VBoxContainer.new()
	container.name = "Slot_%s" % char_id

	var data := PartyManager.CHARACTER_DATA.get(char_id, {})
	var char_state := PartyManager.get_character(char_id)

	# Name label
	var name_lbl := Label.new()
	name_lbl.text = data.get("name", char_id.capitalize())
	name_lbl.add_theme_font_size_override("font_size", 8)
	container.add_child(name_lbl)

	# HP bar
	var hp_bar := _create_stat_bar("HP", char_state.get("hp",1), char_state.get("max_hp",1), Color(0.8,0.1,0.1))
	hp_bar.name = "HPBar"
	container.add_child(hp_bar)

	# MP bar
	var mp_bar := _create_stat_bar("MP", char_state.get("mp",0), char_state.get("max_mp",0), Color(0.1,0.2,0.9))
	mp_bar.name = "MPBar"
	container.add_child(mp_bar)

	# ATB gauge
	var atb_bar := _create_stat_bar("ATB", 0, 100, Color(0.9,0.8,0.1))
	atb_bar.name = "ATBBar"
	container.add_child(atb_bar)

	# Status icons row
	var status_row := HBoxContainer.new()
	status_row.name = "StatusIcons"
	container.add_child(status_row)

	return container

func _create_stat_bar(label_text: String, current: int, maximum: int, color: Color) -> HBoxContainer:
	var row := HBoxContainer.new()

	var lbl := Label.new()
	lbl.text = label_text
	lbl.add_theme_font_size_override("font_size", 7)
	lbl.custom_minimum_size = Vector2(18, 0)
	row.add_child(lbl)

	var bar := ProgressBar.new()
	bar.min_value = 0
	bar.max_value = max(1, maximum)
	bar.value = current
	bar.custom_minimum_size = Vector2(50, 6)
	bar.show_percentage = false
	var stylebox := StyleBoxFlat.new()
	stylebox.bg_color = color
	bar.add_theme_stylebox_override("fill", stylebox)
	row.add_child(bar)

	var val_lbl := Label.new()
	val_lbl.text = "%d/%d" % [current, maximum]
	val_lbl.add_theme_font_size_override("font_size", 7)
	row.add_child(val_lbl)

	return row

func _build_enemy_ui() -> void:
	_enemy_slots.clear()
	for child in enemy_ui.get_children():
		child.queue_free()

	for i in BattleManager.current_enemies.size():
		var enemy: Dictionary = BattleManager.current_enemies[i]
		var slot := _create_enemy_slot(enemy, i)
		enemy_ui.add_child(slot)
		_enemy_slots.append(slot)

func _create_enemy_slot(enemy: Dictionary, index: int) -> Control:
	var container := VBoxContainer.new()
	container.name = "Enemy_%d" % index

	var sprite := Sprite2D.new()
	var tex_path := "res://assets/sprites/enemies/%s.png" % enemy.get("sprite", "kobold")
	if ResourceLoader.exists(tex_path):
		sprite.texture = load(tex_path)
	else:
		# Placeholder colored rectangle
		var placeholder := ColorRect.new()
		placeholder.color = Color(0.6, 0.2, 0.2)
		placeholder.custom_minimum_size = Vector2(32, 32)
		container.add_child(placeholder)

	if sprite.texture:
		container.add_child(sprite)

	var hp_bar := _create_stat_bar("", enemy.get("max_hp",1), enemy.get("max_hp",1), Color(0.8,0.1,0.1))
	hp_bar.name = "HPBar"
	container.add_child(hp_bar)

	return container

# ===== SIGNAL HANDLERS =====

func _on_turn_ready(actor: Dictionary) -> void:
	_active_actor_id = str(actor.get("id", ""))

	if actor.get("type") == "character":
		var char_id: String = actor["id"]
		var char_state := PartyManager.get_character(char_id)

		# Check for berserk/confusion - auto-act
		if char_state.get("berserk_mode", false):
			_auto_berserk_action(char_id)
			return

		# Open command menu
		_waiting_for_input = true
		command_menu.visible = true
		command_menu.setup_for_character(char_id)

	# Enemy turns handled automatically by BattleManager._process()

func _auto_berserk_action(char_id: String) -> void:
	# Iris berserk: attack killer, or random enemy
	var target_idx := BattleManager._get_random_living_enemy()
	var char_state := PartyManager.get_character(char_id)

	if char_state.get("panda_form_active", false):
		# 3 attacks
		for _i in 3:
			BattleManager.execute_player_action(char_id, {
				"type": "attack",
				"target": {"type": "enemy", "id": target_idx}
			})
			await get_tree().create_timer(0.3).timeout
	else:
		BattleManager.execute_player_action(char_id, {
			"type": "attack",
			"target": {"type": "enemy", "id": target_idx}
		})

func _on_command_selected(char_id: String, action: Dictionary) -> void:
	_waiting_for_input = false
	command_menu.visible = false
	BattleManager.execute_player_action(char_id, action)
	_update_all_ui()
	# Try to fire banter between turns (non-blocking; BanterPopup handles display)
	BanterSystem.try_trigger_banter(GameManager.get_active_characters())

func _on_damage_dealt(target: Dictionary, damage: int, descriptor: String, element: String) -> void:
	_show_damage_number(target, damage, descriptor)
	_update_all_ui()

func _show_damage_number(target: Dictionary, damage: int, descriptor: String) -> void:
	var lbl := Label.new()
	damage_container.add_child(lbl)

	if damage < 0:
		lbl.text = "+" + str(abs(damage))
		lbl.modulate = Color.GREEN
	elif damage == 0:
		lbl.text = "MISS"
		lbl.modulate = Color.GRAY
	else:
		lbl.text = str(damage)
		match descriptor:
			"physical": lbl.modulate = Color.WHITE
			"magical": lbl.modulate = Color(0.5, 0.8, 1.0)
			"psychic": lbl.modulate = Color(0.8, 0.4, 1.0)
			"heal": lbl.modulate = Color.GREEN
			_: lbl.modulate = Color.WHITE

	lbl.add_theme_font_size_override("font_size", 9)

	# Float upward and fade
	var tween := create_tween()
	tween.parallel().tween_property(lbl, "position:y", lbl.position.y - 20, 0.8)
	tween.parallel().tween_property(lbl, "modulate:a", 0.0, 0.8)
	tween.tween_callback(lbl.queue_free)

func _on_character_ko(char_id: String) -> void:
	_update_all_ui()
	_show_message("%s is KO'd!" % char_id.capitalize())

func _on_enemy_ko(enemy_index: int) -> void:
	if enemy_index < _enemy_slots.size():
		_enemy_slots[enemy_index].modulate = Color(0.3, 0.3, 0.3, 0.5)
	_update_all_ui()

func _on_status_applied(target: Dictionary, status: String) -> void:
	_update_all_ui()

func _on_status_removed(target: Dictionary, status: String) -> void:
	_update_all_ui()

func _on_battle_ended(result: String) -> void:
	command_menu.visible = false
	if _banter_popup != null:
		_banter_popup.dismiss()
	match result:
		"victory":
			await get_tree().create_timer(1.5).timeout
			SceneTransition.change_scene("res://scenes/ui/victory_screen.tscn")
		"defeat":
			await get_tree().create_timer(1.0).timeout
			SceneTransition.change_scene("res://scenes/ui/game_over.tscn")
		"fled":
			SceneTransition.change_scene(
				"res://scenes/locations/%s.tscn" % GameManager.current_location)

# ===== UI UPDATES =====

func _update_all_ui() -> void:
	_update_party_ui()
	_update_enemy_ui()
	_update_atb_bars()

func _update_party_ui() -> void:
	var party := GameManager.get_active_characters()
	for i in min(party.size(), _party_slots.size()):
		var char_id: String = party[i]
		var char_state := PartyManager.get_character(char_id)
		var slot := _party_slots[i]

		var hp_row: HBoxContainer = slot.get_node_or_null("HPBar")
		if hp_row:
			var bar: ProgressBar = hp_row.get_child(1)
			var lbl: Label = hp_row.get_child(2)
			bar.max_value = max(1, char_state.get("max_hp", 1))
			bar.value = char_state.get("hp", 0)
			lbl.text = "%d/%d" % [char_state.get("hp", 0), char_state.get("max_hp", 1)]

		var mp_row: HBoxContainer = slot.get_node_or_null("MPBar")
		if mp_row:
			var bar: ProgressBar = mp_row.get_child(1)
			var lbl: Label = mp_row.get_child(2)
			bar.max_value = max(1, char_state.get("max_mp", 1))
			bar.value = char_state.get("mp", 0)
			lbl.text = "%d/%d" % [char_state.get("mp", 0), char_state.get("max_mp", 1)]

func _update_enemy_ui() -> void:
	for i in min(BattleManager.current_enemies.size(), _enemy_slots.size()):
		var enemy: Dictionary = BattleManager.current_enemies[i]
		var slot := _enemy_slots[i]
		var hp_row: HBoxContainer = slot.get_node_or_null("HPBar")
		if hp_row:
			var bar: ProgressBar = hp_row.get_child(1)
			bar.max_value = max(1, enemy.get("max_hp", 1))
			bar.value = enemy.get("current_hp", 0)

func _update_atb_bars() -> void:
	var party := GameManager.get_active_characters()
	for i in min(party.size(), _party_slots.size()):
		var char_id: String = party[i]
		var slot := _party_slots[i]
		var atb_row: HBoxContainer = slot.get_node_or_null("ATBBar")
		if atb_row:
			var bar: ProgressBar = atb_row.get_child(1)
			bar.value = BattleManager.atb_gauges.get(char_id, 0.0)

func _process(_delta: float) -> void:
	_update_atb_bars()

func _show_message(text: String, duration: float = 2.0) -> void:
	message_label.text = text
	message_label.visible = true
	await get_tree().create_timer(duration).timeout
	message_label.visible = false
