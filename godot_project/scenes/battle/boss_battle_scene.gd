## boss_battle_scene.gd
## Extended battle scene for boss fights.
## Disables flee option, plays boss music, shows boss HP bar prominently.
## Inherits logic from battle_scene.gd via composition (not extends, to keep scenes clean).
extends Node2D
class_name BossBattleScene

# ---------------------------------------------------------------------------
# Node refs
# ---------------------------------------------------------------------------
@onready var background_rect: TextureRect = $Background
@onready var party_ui: Control = $UI/PartyPanel
@onready var boss_panel: Control = $UI/BossPanel
@onready var boss_name_label: Label = $UI/BossPanel/BossName
@onready var boss_hp_bar: ProgressBar = $UI/BossPanel/HPBar
@onready var boss_hp_label: Label = $UI/BossPanel/HPLabel
@onready var turn_label: Label = $UI/TurnLabel
@onready var damage_layer: CanvasLayer = $DamageNumbers
@onready var animation_player: AnimationPlayer = $AnimationPlayer
@onready var command_menu_container: Control = $UI/CommandMenuContainer

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
var boss_id: String = ""
var boss_data: Dictionary = {}
var _command_menu: Node = null
var _battle_active: bool = false
var _party_ui_nodes: Array[Control] = []

const COMMAND_MENU_SCENE: String = "res://scenes/battle/command_menu.tscn"


# ---------------------------------------------------------------------------
# _ready
# ---------------------------------------------------------------------------
func _ready() -> void:
	_connect_battle_signals()
	_load_boss_data()
	_build_boss_ui()
	_build_party_ui()
	_spawn_command_menu()
	_start_battle()


func _connect_battle_signals() -> void:
	if not BattleManager:
		return
	BattleManager.turn_ready.connect(_on_turn_ready)
	BattleManager.damage_dealt.connect(_on_damage_dealt)
	BattleManager.character_died.connect(_on_character_died)
	BattleManager.enemy_died.connect(_on_enemy_died)
	BattleManager.battle_won.connect(_on_battle_won)
	BattleManager.battle_lost.connect(_on_battle_lost)
	BattleManager.status_applied.connect(_on_status_applied)


func _load_boss_data() -> void:
	boss_id = GameManager.get_meta("pending_boss_id") if GameManager.has_meta("pending_boss_id") else "void_architect"
	var EnemyDB = load("res://data/enemy_database.gd")
	if EnemyDB:
		boss_data = EnemyDB.get_enemy(boss_id)


func _build_boss_ui() -> void:
	if boss_panel:
		boss_name_label.text = boss_data.get("name", boss_id.replace("_", " ").capitalize())
		boss_hp_bar.max_value = boss_data.get("hp", 9999)
		boss_hp_bar.value = boss_data.get("hp", 9999)
		_update_boss_hp()

	# Load background
	var bg_key: String = boss_data.get("battle_bg", "final_dungeon")
	var bg_path: String = "res://assets/backgrounds/battle_%s.png" % bg_key
	if background_rect and ResourceLoader.exists(bg_path):
		background_rect.texture = load(bg_path)


func _update_boss_hp() -> void:
	if not BattleManager or not boss_panel:
		return
	var enemies: Array = BattleManager.get_enemy_states()
	if enemies.is_empty():
		return
	var boss_state: Dictionary = enemies[0]
	var hp: int = boss_state.get("current_hp", 0)
	var max_hp: int = boss_state.get("max_hp", 1)
	boss_hp_bar.value = hp
	boss_hp_label.text = "%d / %d" % [hp, max_hp]

	# Color based on HP %
	var pct: float = float(hp) / float(max_hp)
	if pct < 0.25:
		boss_hp_bar.modulate = Color(1.0, 0.2, 0.2)
	elif pct < 0.5:
		boss_hp_bar.modulate = Color(1.0, 0.7, 0.2)
	else:
		boss_hp_bar.modulate = Color(0.3, 1.0, 0.3)


func _build_party_ui() -> void:
	if not party_ui:
		return
	for child in party_ui.get_children():
		child.queue_free()
	_party_ui_nodes.clear()

	var party: Array = BattleManager.get_party_states() if BattleManager else []
	for member in party:
		var panel: Panel = Panel.new()
		panel.custom_minimum_size = Vector2(80, 40)
		party_ui.add_child(panel)

		var vbox: VBoxContainer = VBoxContainer.new()
		vbox.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		panel.add_child(vbox)

		var name_lbl: Label = Label.new()
		name_lbl.name = "Name"
		name_lbl.text = member.get("name", "?")
		name_lbl.add_theme_font_size_override("font_size", 7)
		vbox.add_child(name_lbl)

		var hp_lbl: Label = Label.new()
		hp_lbl.name = "HP"
		hp_lbl.text = "HP %d" % member.get("current_hp", 0)
		hp_lbl.add_theme_font_size_override("font_size", 7)
		vbox.add_child(hp_lbl)

		var atb_bar: ProgressBar = ProgressBar.new()
		atb_bar.name = "ATBBar"
		atb_bar.max_value = 100
		atb_bar.value = member.get("atb_gauge", 0)
		atb_bar.custom_minimum_size = Vector2(70, 5)
		vbox.add_child(atb_bar)

		panel.set_meta("char_id", member.get("char_id", ""))
		_party_ui_nodes.append(panel)


func _spawn_command_menu() -> void:
	var scene: PackedScene = load(COMMAND_MENU_SCENE)
	if scene:
		_command_menu = scene.instantiate()
		command_menu_container.add_child(_command_menu)
		_command_menu.visible = false
		if _command_menu.has_signal("action_chosen"):
			_command_menu.action_chosen.connect(BattleManager.execute_player_action)


func _start_battle() -> void:
	var formation: Dictionary = GameManager.get_meta("pending_formation") if GameManager.has_meta("pending_formation") else {}
	AudioManager.play_music(boss_data.get("music", "battle_boss"))
	BattleManager.start_battle(formation, boss_id)
	_battle_active = true


# ---------------------------------------------------------------------------
# _process
# ---------------------------------------------------------------------------
func _process(_delta: float) -> void:
	if not _battle_active:
		return
	_update_all_ui()


func _update_all_ui() -> void:
	_update_boss_hp()
	_update_party_panels()


func _update_party_panels() -> void:
	if not BattleManager:
		return
	var states: Array = BattleManager.get_party_states()
	for panel in _party_ui_nodes:
		var char_id: String = panel.get_meta("char_id", "")
		for state in states:
			if state.get("char_id", "") == char_id:
				var hp_lbl: Label = panel.get_node_or_null("VBoxContainer/HP")
				if hp_lbl:
					hp_lbl.text = "HP %d" % state.get("current_hp", 0)
				var atb: ProgressBar = panel.get_node_or_null("VBoxContainer/ATBBar")
				if atb:
					atb.value = state.get("atb_gauge", 0)
				break


# ---------------------------------------------------------------------------
# Signal handlers
# ---------------------------------------------------------------------------
func _on_turn_ready(actor_id: String, _is_enemy: bool) -> void:
	if _is_enemy:
		if _command_menu:
			_command_menu.visible = false
		turn_label.text = ""
		return

	turn_label.text = "%s's turn" % actor_id.capitalize()
	if _command_menu:
		_command_menu.visible = true
		if _command_menu.has_method("setup_for_character"):
			_command_menu.setup_for_character(actor_id)


func _on_damage_dealt(target_id: String, amount: int, _damage_type: String) -> void:
	_show_damage_number(amount, Color.RED)
	_update_boss_hp()


func _show_damage_number(amount: int, color: Color) -> void:
	var lbl: Label = Label.new()
	lbl.text = str(amount)
	lbl.modulate = color
	lbl.add_theme_font_size_override("font_size", 10)
	lbl.position = Vector2(randf_range(80, 180), randf_range(40, 80))
	damage_layer.add_child(lbl)

	var tween: Tween = create_tween()
	tween.tween_property(lbl, "position:y", lbl.position.y - 30.0, 0.8)
	tween.parallel().tween_property(lbl, "modulate:a", 0.0, 0.8)
	tween.tween_callback(lbl.queue_free)


func _on_character_died(char_id: String) -> void:
	AudioManager.play_sfx("player_death")
	# Check for Iris berserk (if Fei died)
	if char_id == "fei" and "iris" in GameManager.active_party:
		if DialogueManager.has_method("start_dialogue"):
			DialogueManager.start_dialogue("iris_berserk")


func _on_enemy_died(_enemy_id: String) -> void:
	# Boss death — could trigger phase 2 if needed
	pass


func _on_status_applied(target_id: String, status: String) -> void:
	_show_damage_number(0, Color.YELLOW)  # Status indicator


func _on_battle_won(exp: int, gil: int) -> void:
	_battle_active = false
	if _command_menu:
		_command_menu.visible = false
	AudioManager.play_sfx("victory_fanfare")
	await get_tree().create_timer(1.5).timeout

	# Check if this was the final boss
	if boss_id == "void_architect":
		var EndingCtrl = load("res://scenes/ui/ending_controller.gd")
		if EndingCtrl:
			var ctrl = EndingCtrl.new()
			add_child(ctrl)
			var ending = StoryEventSystem.determine_ending()
			ctrl.play_ending(ending)
	elif boss_id == "the_architect":
		# Secret boss
		var EndingCtrl = load("res://scenes/ui/ending_controller.gd")
		if EndingCtrl:
			var ctrl = EndingCtrl.new()
			add_child(ctrl)
			ctrl.play_ending("bad")
	else:
		# Normal boss – return to location
		var victory_scene: PackedScene = load("res://scenes/ui/victory_screen.tscn")
		if victory_scene:
			var victory: Node = victory_scene.instantiate()
			victory.set_meta("exp_gained", exp)
			victory.set_meta("gil_gained", gil)
			add_child(victory)
		else:
			SceneTransition.back()


func _on_battle_lost() -> void:
	_battle_active = false
	await get_tree().create_timer(1.0).timeout
	SceneTransition.change_scene("res://scenes/ui/game_over.tscn")
