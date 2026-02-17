extends Control
## CommandMenu - Battle command selection UI

signal action_selected(char_id: String, action: Dictionary)

var _char_id := ""
var _current_menu := "main"  # main / magic / item / target
var _cursor_index := 0
var _main_options := ["Attack", "Magic", "Item", "Defend", "Flee", "Swap"]
var _spell_list: Array = []
var _item_list: Array = []
var _target_list: Array = []
var _pending_action := {}

@onready var main_panel: VBoxContainer = $MainPanel
@onready var sub_panel: VBoxContainer = $SubPanel
@onready var cursor: Sprite2D = $Cursor
@onready var target_cursor: Sprite2D = $TargetCursor

func _ready() -> void:
	visible = false

func setup_for_character(char_id: String) -> void:
	_char_id = char_id
	_show_main_menu()
	AudioManager.play_sfx("menu_select")

func _show_main_menu() -> void:
	_current_menu = "main"
	_cursor_index = 0
	sub_panel.visible = false
	main_panel.visible = true

	for child in main_panel.get_children():
		child.queue_free()

	for i in _main_options.size():
		var btn := Label.new()
		btn.text = _main_options[i]
		btn.add_theme_font_size_override("font_size", 8)
		main_panel.add_child(btn)

	_update_cursor()

func _show_magic_menu() -> void:
	_current_menu = "magic"
	_cursor_index = 0
	main_panel.visible = false
	sub_panel.visible = true

	for child in sub_panel.get_children():
		child.queue_free()

	var char_state := PartyManager.get_character(_char_id)
	_spell_list = char_state.get("spells", [])

	for spell_id in _spell_list:
		var spell := SpellDatabase.get_spell(spell_id)
		var btn := Label.new()
		var mp_cost: int = spell.get("mp_cost", 0)
		var can_afford: bool = char_state.get("mp", 0) >= mp_cost
		btn.text = "%s  %dMP" % [spell.get("name", spell_id), mp_cost]
		btn.add_theme_font_size_override("font_size", 8)
		if not can_afford:
			btn.modulate = Color(0.5, 0.5, 0.5)
		sub_panel.add_child(btn)

	if _spell_list.is_empty():
		var empty := Label.new()
		empty.text = "(No spells)"
		empty.add_theme_font_size_override("font_size", 8)
		sub_panel.add_child(empty)

	_update_cursor()

func _show_item_menu() -> void:
	_current_menu = "item"
	_cursor_index = 0
	main_panel.visible = false
	sub_panel.visible = true

	for child in sub_panel.get_children():
		child.queue_free()

	_item_list = []
	for item_id in GameManager.items:
		if GameManager.items[item_id] > 0:
			_item_list.append(item_id)

	for item_id in _item_list:
		var count: int = GameManager.items[item_id]
		var btn := Label.new()
		btn.text = "%s  x%d" % [item_id.capitalize().replace("_", " "), count]
		btn.add_theme_font_size_override("font_size", 8)
		sub_panel.add_child(btn)

	if _item_list.is_empty():
		var empty := Label.new()
		empty.text = "(No items)"
		empty.add_theme_font_size_override("font_size", 8)
		sub_panel.add_child(empty)

	_update_cursor()

func _show_target_menu(targets: Array) -> void:
	_current_menu = "target"
	_cursor_index = 0
	_target_list = targets
	sub_panel.visible = true
	main_panel.visible = false

	for child in sub_panel.get_children():
		child.queue_free()

	for target in targets:
		var lbl := Label.new()
		lbl.text = target.get("name", "???")
		lbl.add_theme_font_size_override("font_size", 8)
		sub_panel.add_child(lbl)

	_update_cursor()

func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return

	var item_count := _get_current_item_count()

	if event.is_action_pressed("move_up"):
		_cursor_index = (_cursor_index - 1 + item_count) % item_count
		_update_cursor()
		AudioManager.play_sfx("menu_select")

	elif event.is_action_pressed("move_down"):
		_cursor_index = (_cursor_index + 1) % item_count
		_update_cursor()
		AudioManager.play_sfx("menu_select")

	elif event.is_action_pressed("action_confirm"):
		_on_confirm()
		AudioManager.play_sfx("menu_confirm")

	elif event.is_action_pressed("action_cancel"):
		_on_cancel()
		AudioManager.play_sfx("menu_cancel")

func _get_current_item_count() -> int:
	match _current_menu:
		"main": return _main_options.size()
		"magic": return max(1, _spell_list.size())
		"item": return max(1, _item_list.size())
		"target": return _target_list.size()
	return 1

func _on_confirm() -> void:
	match _current_menu:
		"main":
			_handle_main_confirm()
		"magic":
			_handle_magic_confirm()
		"item":
			_handle_item_confirm()
		"target":
			_handle_target_confirm()

func _handle_main_confirm() -> void:
	var selected: String = _main_options[_cursor_index]
	match selected:
		"Attack":
			_pending_action = {"type": "attack"}
			_show_enemy_targets()
		"Magic":
			_show_magic_menu()
		"Item":
			_show_item_menu()
		"Defend":
			action_selected.emit(_char_id, {"type": "defend"})
		"Flee":
			action_selected.emit(_char_id, {"type": "flee"})
		"Swap":
			_show_swap_menu()

func _show_enemy_targets() -> void:
	var targets := []
	for i in BattleManager.current_enemies.size():
		var enemy: Dictionary = BattleManager.current_enemies[i]
		if enemy.get("current_hp", 0) > 0:
			targets.append({"type": "enemy", "id": i, "name": enemy.get("name", "Enemy")})
	_show_target_menu(targets)

func _show_ally_targets(include_ko: bool = false) -> void:
	var targets := []
	for char_id in GameManager.get_active_characters():
		var char_state := PartyManager.get_character(char_id)
		var is_ko: bool = char_state.get("hp", 0) <= 0
		if include_ko or not is_ko:
			targets.append({
				"type": "character",
				"id": char_id,
				"name": PartyManager.CHARACTER_DATA.get(char_id, {}).get("name", char_id)
			})
	_show_target_menu(targets)

func _show_swap_menu() -> void:
	_pending_action = {"type": "swap"}
	var targets := []
	for char_id in GameManager.reserve_party:
		var char_state := PartyManager.get_character(char_id)
		if char_state.get("hp", 0) > 0:
			targets.append({
				"type": "bench",
				"id": char_id,
				"name": PartyManager.CHARACTER_DATA.get(char_id, {}).get("name", char_id)
			})
	if targets.is_empty():
		# No bench members available
		_show_main_menu()
		return
	_show_target_menu(targets)

func _handle_magic_confirm() -> void:
	if _spell_list.is_empty():
		return
	var spell_id: String = _spell_list[_cursor_index]
	var spell := SpellDatabase.get_spell(spell_id)
	var char_state := PartyManager.get_character(_char_id)

	if char_state.get("mp", 0) < spell.get("mp_cost", 0):
		return  # Can't afford

	_pending_action = {"type": "spell", "spell_id": spell_id}

	var target_type: String = spell.get("target", "single_enemy")
	match target_type:
		"single_enemy":
			_show_enemy_targets()
		"all_enemies":
			# Auto-select all enemies
			var targets := []
			for i in BattleManager.current_enemies.size():
				if BattleManager.current_enemies[i].get("current_hp", 0) > 0:
					targets.append({"type": "enemy", "id": i})
			_pending_action["targets"] = targets
			action_selected.emit(_char_id, _pending_action)
		"single_ally":
			_show_ally_targets(false)
		"all_allies":
			var targets := []
			for cid in GameManager.get_active_characters():
				targets.append({"type": "character", "id": cid})
			_pending_action["targets"] = targets
			action_selected.emit(_char_id, _pending_action)
		"ko_ally":
			_show_ally_targets(true)
		"all_ko_allies":
			var targets := []
			for cid in GameManager.get_active_characters():
				var cs := PartyManager.get_character(cid)
				if cs.get("hp", 0) <= 0:
					targets.append({"type": "character", "id": cid})
			_pending_action["targets"] = targets
			action_selected.emit(_char_id, _pending_action)

func _handle_item_confirm() -> void:
	if _item_list.is_empty():
		return
	var item_id: String = _item_list[_cursor_index]
	_pending_action = {"type": "item", "item_id": item_id}
	_show_ally_targets(true)  # Items can target KO'd allies

func _handle_target_confirm() -> void:
	if _target_list.is_empty():
		return
	var target: Dictionary = _target_list[_cursor_index]
	_pending_action["target"] = target
	_pending_action["targets"] = [target]

	if _pending_action.get("type") == "swap":
		_pending_action["bench_id"] = target["id"]

	action_selected.emit(_char_id, _pending_action)

func _on_cancel() -> void:
	match _current_menu:
		"main":
			pass  # Can't cancel main menu in battle
		"magic", "item":
			_show_main_menu()
		"target":
			if _pending_action.get("type") in ["spell"]:
				_show_magic_menu()
			elif _pending_action.get("type") == "item":
				_show_item_menu()
			else:
				_show_main_menu()

func _update_cursor() -> void:
	var panel := main_panel if main_panel.visible else sub_panel
	var children := panel.get_children()
	if children.is_empty():
		return
	var idx := clamp(_cursor_index, 0, children.size() - 1)
	var target_child: Control = children[idx]
	cursor.position = target_child.global_position - global_position + Vector2(-8, target_child.size.y / 2)
