extends Control
## PauseMenu - Full pause menu: Party, Items, Equipment, Magic, Save, Tutorial, Settings

@onready var tab_bar: HBoxContainer = $TabBar
@onready var content_panel: Control = $ContentPanel
@onready var playtime_label: Label = $PlaytimeLabel
@onready var gil_label: Label = $GilLabel

var _tabs := ["Party", "Items", "Equipment", "Magic", "Key Items", "Save", "Tutorial", "Settings"]
var _current_tab := 0
var _previous_scene := ""

func _ready() -> void:
	get_tree().paused = true
	_update_header()
	_show_tab(0)

func _exit_tree() -> void:
	get_tree().paused = false

func _update_header() -> void:
	var total_seconds := int(GameManager.playtime_seconds)
	var hours := total_seconds / 3600
	var minutes := (total_seconds % 3600) / 60
	var seconds := total_seconds % 60
	playtime_label.text = "%02d:%02d:%02d" % [hours, minutes, seconds]
	gil_label.text = "Gil: %d" % GameManager.gil

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("action_cancel") or event.is_action_pressed("action_menu"):
		_close()
	elif event.is_action_pressed("move_left"):
		_current_tab = (_current_tab - 1 + _tabs.size()) % _tabs.size()
		_show_tab(_current_tab)
		AudioManager.play_sfx("menu_select")
	elif event.is_action_pressed("move_right"):
		_current_tab = (_current_tab + 1) % _tabs.size()
		_show_tab(_current_tab)
		AudioManager.play_sfx("menu_select")

func _show_tab(index: int) -> void:
	for child in content_panel.get_children():
		child.queue_free()

	match _tabs[index]:
		"Party":     _show_party_tab()
		"Items":     _show_items_tab()
		"Equipment": _show_equipment_tab()
		"Magic":     _show_magic_tab()
		"Key Items": _show_key_items_tab()
		"Save":      _show_save_tab()
		"Tutorial":  _show_tutorial_tab()
		"Settings":  _show_settings_tab()

# ===== PARTY TAB =====

func _show_party_tab() -> void:
	var party_list := VBoxContainer.new()
	content_panel.add_child(party_list)

	var all_chars := GameManager.get_active_characters() + GameManager.reserve_party
	for char_id in all_chars:
		var char_state := PartyManager.get_character(char_id)
		var data := PartyManager.CHARACTER_DATA.get(char_id, {})
		if char_state.is_empty():
			continue

		var row := HBoxContainer.new()
		party_list.add_child(row)

		var name_lbl := Label.new()
		name_lbl.text = data.get("name", char_id)
		name_lbl.custom_minimum_size = Vector2(50, 0)
		name_lbl.add_theme_font_size_override("font_size", 8)
		row.add_child(name_lbl)

		var lv_lbl := Label.new()
		lv_lbl.text = "Lv%d" % char_state.get("level", 1)
		lv_lbl.custom_minimum_size = Vector2(28, 0)
		lv_lbl.add_theme_font_size_override("font_size", 8)
		row.add_child(lv_lbl)

		var hp_lbl := Label.new()
		hp_lbl.text = "HP %d/%d" % [char_state.get("hp",0), char_state.get("max_hp",1)]
		hp_lbl.custom_minimum_size = Vector2(60, 0)
		hp_lbl.add_theme_font_size_override("font_size", 8)
		row.add_child(hp_lbl)

		var mp_lbl := Label.new()
		mp_lbl.text = "MP %d/%d" % [char_state.get("mp",0), char_state.get("max_mp",1)]
		mp_lbl.add_theme_font_size_override("font_size", 8)
		row.add_child(mp_lbl)

		# Class
		var class_lbl := Label.new()
		class_lbl.text = char_state.get("current_class","").replace("_"," ").capitalize()
		class_lbl.add_theme_font_size_override("font_size", 8)
		row.add_child(class_lbl)

		# In active / bench indicator
		var loc_lbl := Label.new()
		loc_lbl.text = "[Active]" if char_id in GameManager.active_party else "[Bench]"
		loc_lbl.add_theme_font_size_override("font_size", 8)
		row.add_child(loc_lbl)

# ===== ITEMS TAB =====

func _show_items_tab() -> void:
	var list := VBoxContainer.new()
	content_panel.add_child(list)

	if GameManager.items.is_empty():
		var empty := Label.new()
		empty.text = "No items."
		empty.add_theme_font_size_override("font_size", 8)
		list.add_child(empty)
		return

	for item_id in GameManager.items:
		var count: int = GameManager.items[item_id]
		if count <= 0:
			continue
		var row := HBoxContainer.new()
		list.add_child(row)

		var name_lbl := Label.new()
		name_lbl.text = item_id.replace("_"," ").capitalize()
		name_lbl.custom_minimum_size = Vector2(100, 0)
		name_lbl.add_theme_font_size_override("font_size", 8)
		row.add_child(name_lbl)

		var count_lbl := Label.new()
		count_lbl.text = "x%d" % count
		count_lbl.add_theme_font_size_override("font_size", 8)
		row.add_child(count_lbl)

# ===== EQUIPMENT TAB =====

func _show_equipment_tab() -> void:
	var list := VBoxContainer.new()
	content_panel.add_child(list)

	for char_id in GameManager.get_active_characters():
		var char_state := PartyManager.get_character(char_id)
		var data := PartyManager.CHARACTER_DATA.get(char_id, {})

		var char_lbl := Label.new()
		char_lbl.text = "— %s —" % data.get("name", char_id)
		char_lbl.add_theme_font_size_override("font_size", 8)
		list.add_child(char_lbl)

		var equip := char_state.get("equipment", {})
		for slot_name in ["weapon","armor","shield","accessory","special"]:
			var row := HBoxContainer.new()
			list.add_child(row)

			var slot_lbl := Label.new()
			slot_lbl.text = slot_name.capitalize() + ":"
			slot_lbl.custom_minimum_size = Vector2(55, 0)
			slot_lbl.add_theme_font_size_override("font_size", 8)
			row.add_child(slot_lbl)

			var equip_id: String = equip.get(slot_name, "")
			var equip_lbl := Label.new()
			equip_lbl.text = equip_id.replace("_"," ").capitalize() if equip_id != "" else "(empty)"
			equip_lbl.add_theme_font_size_override("font_size", 8)
			row.add_child(equip_lbl)

# ===== MAGIC TAB =====

func _show_magic_tab() -> void:
	var list := VBoxContainer.new()
	content_panel.add_child(list)

	for char_id in GameManager.get_active_characters():
		var char_state := PartyManager.get_character(char_id)
		var data := PartyManager.CHARACTER_DATA.get(char_id, {})

		var char_lbl := Label.new()
		char_lbl.text = "— %s —" % data.get("name", char_id)
		char_lbl.add_theme_font_size_override("font_size", 8)
		list.add_child(char_lbl)

		var spells: Array = char_state.get("spells", [])
		if spells.is_empty():
			var empty := Label.new()
			empty.text = "  No spells"
			empty.add_theme_font_size_override("font_size", 8)
			list.add_child(empty)
		else:
			for spell_id in spells:
				var spell := SpellDatabase.get_spell(spell_id)
				var row := Label.new()
				row.text = "  %s (%dMP)" % [spell.get("name", spell_id), spell.get("mp_cost", 0)]
				row.add_theme_font_size_override("font_size", 8)
				list.add_child(row)

# ===== KEY ITEMS TAB =====

func _show_key_items_tab() -> void:
	var list := VBoxContainer.new()
	content_panel.add_child(list)

	if GameManager.key_items.is_empty():
		var empty := Label.new()
		empty.text = "No key items."
		empty.add_theme_font_size_override("font_size", 8)
		list.add_child(empty)
		return

	for item_id in GameManager.key_items:
		var lbl := Label.new()
		lbl.text = item_id.replace("_"," ").capitalize()
		lbl.add_theme_font_size_override("font_size", 8)
		list.add_child(lbl)

# ===== SAVE TAB =====

func _show_save_tab() -> void:
	var options := VBoxContainer.new()
	content_panel.add_child(options)

	var qs_btn := _make_button("Quicksave", func():
		SaveSystem.quicksave()
		_close()
	)
	options.add_child(qs_btn)

	var save_btn := _make_button("Save to Slot...", func():
		_show_save_slot_picker()
	)
	options.add_child(save_btn)

	var load_btn := _make_button("Load Game", func():
		SceneTransition.change_scene("res://scenes/ui/save_select.tscn")
	)
	options.add_child(load_btn)

func _show_save_slot_picker() -> void:
	# Simple slot picker (1-10 visible at a time)
	pass

func _make_button(text: String, callback: Callable) -> Button:
	var btn := Button.new()
	btn.text = text
	btn.add_theme_font_size_override("font_size", 8)
	btn.pressed.connect(callback)
	return btn

# ===== TUTORIAL TAB =====

func _show_tutorial_tab() -> void:
	var sections := [
		"1. Movement & Navigation",
		"2. Combat Basics (ATB)",
		"3. Magic System",
		"4. Equipment & Slots",
		"5. Status Effects",
		"6. Party Management",
		"7. Save System",
		"8. Shops",
		"9. Character Evolution",
		"10. Recruitment & Deadline",
		"11. Key Items",
		"12. Level-Up Abilities",
		"13. Endings Guide",
	]

	const TUTORIAL_TEXT := {
		"1. Movement & Navigation": "Use arrow keys/D-pad to move. Press A/X for menu. Interact with objects by facing them and pressing Z/A.",
		"2. Combat Basics (ATB)": "ATB gauges fill over time based on Speed. When full, choose an action. Options: Attack, Magic, Item, Defend (halves damage), Flee (75% success), Swap (bring in bench member).",
		"3. Magic System": "MP cost = Spell Level (Lv1=1MP, Lv9=9MP). Buy spells from magic shops. Each class has different spell access. Flood and Hannah can spend 2x MP to double spell power.",
		"4. Equipment & Slots": "5 slots: Weapon, Armor, Shield, Accessory, Special. Shield enables Taunt for Fei (manual) and auto-Taunt for Paladin Michael. Fei loses shield when he evolves.",
		"5. Status Effects": "POISON: damage/turn. SLEEP: can't act, wakes on hit. PARALYSIS: can't act, doesn't wake. BLIND: miss more. SILENCE: no magic. SLOW/HASTE: ATB speed. BERSERK: AI-only attacks, +power. CONFUSE: may hit allies. BURN: damage/turn, ONLY water removes it; Arsonist Crankpot's burn spreads. BUBBLE: silence+no attack, pops if hit.",
		"6. Party Management": "3 active in battle. Swap brings in a bench member during battle (uses turn). All recruited characters gain EXP after battles.",
		"7. Save System": "Quicksave: anytime (Y button). Manual saves: up to 100 slots. Autosave: after major events. All carry over between play sessions.",
		"8. Shops": "Weapon/armor shops sell equipment. Magic shops sell spells (must be right class). Item shops sell consumables. Buy Shotgun Blueprint and Sniper Blueprint from Imperial City weapons shop!",
		"9. Character Evolution": "Find each character's Key Item, then complete Orisia's sidequest. Unlocks new class with level cap raised from 75 to 99. Yipp's evolution depends on your choice.",
		"10. Recruitment & Deadline": "Required: Javin, Frostbite, Fei, Michael, Flood, Hannah, Warghoul. Optional: Cookie, Iris, Fritzzit+Crankpot (pair!), Yipp. Once you say YES to Orisia, it's too late — missed characters become zombie enemies.",
		"11. Key Items": "Cannot be sold or destroyed. Each unlocks a character's evolution sidequest. Blueprints must be PURCHASED. Holy Symbol and Wine Glass are in random dungeons each playthrough.",
		"12. Level-Up Abilities": "Every 10 levels you gain an ability permanently. These are fixed — no choices to make. Some abilities require evolved class to activate (shown in description).",
		"13. Endings Guide": "GOOD: All optionals recruited + cure found + Yipp not Vampire. NORMAL: Cure found but not all recruited. BAD: Cure NOT found. BEST: Good ending + Yipp became Saint, then return after credits.",
	}

	var list := VBoxContainer.new()
	content_panel.add_child(list)

	var selected_section := 0
	var section_btns := []

	for i in sections.size():
		var btn := Button.new()
		btn.text = sections[i]
		btn.add_theme_font_size_override("font_size", 7)
		btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
		list.add_child(btn)

		var desc_lbl := Label.new()
		desc_lbl.text = TUTORIAL_TEXT.get(sections[i], "")
		desc_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		desc_lbl.add_theme_font_size_override("font_size", 7)
		desc_lbl.visible = false
		list.add_child(desc_lbl)

		btn.pressed.connect(func():
			desc_lbl.visible = not desc_lbl.visible
		)

# ===== SETTINGS TAB =====

func _show_settings_tab() -> void:
	var list := VBoxContainer.new()
	content_panel.add_child(list)

	# Music volume
	var music_row := HBoxContainer.new()
	list.add_child(music_row)
	var music_lbl := Label.new()
	music_lbl.text = "Music:"
	music_lbl.add_theme_font_size_override("font_size", 8)
	music_row.add_child(music_lbl)
	var music_slider := HSlider.new()
	music_slider.min_value = 0
	music_slider.max_value = 100
	music_slider.value = 80
	music_slider.custom_minimum_size = Vector2(80, 0)
	music_slider.value_changed.connect(func(v): AudioManager.set_music_volume(v / 100.0))
	music_row.add_child(music_slider)

	# SFX volume
	var sfx_row := HBoxContainer.new()
	list.add_child(sfx_row)
	var sfx_lbl := Label.new()
	sfx_lbl.text = "SFX:"
	sfx_lbl.add_theme_font_size_override("font_size", 8)
	sfx_row.add_child(sfx_lbl)
	var sfx_slider := HSlider.new()
	sfx_slider.min_value = 0
	sfx_slider.max_value = 100
	sfx_slider.value = 100
	sfx_slider.custom_minimum_size = Vector2(80, 0)
	sfx_slider.value_changed.connect(func(v): AudioManager.set_sfx_volume(v / 100.0))
	sfx_row.add_child(sfx_slider)

	# ATB pause toggle
	var atb_row := HBoxContainer.new()
	list.add_child(atb_row)
	var atb_lbl := Label.new()
	atb_lbl.text = "Pause ATB in menus:"
	atb_lbl.add_theme_font_size_override("font_size", 8)
	atb_row.add_child(atb_lbl)
	var atb_check := CheckBox.new()
	atb_check.button_pressed = GameManager.atb_paused_in_menu
	atb_check.toggled.connect(func(v): GameManager.atb_paused_in_menu = v)
	atb_row.add_child(atb_check)

	# Turn-based mode
	var tb_row := HBoxContainer.new()
	list.add_child(tb_row)
	var tb_lbl := Label.new()
	tb_lbl.text = "Turn-based mode:"
	tb_lbl.add_theme_font_size_override("font_size", 8)
	tb_row.add_child(tb_lbl)
	var tb_check := CheckBox.new()
	tb_check.button_pressed = GameManager.turn_based_mode
	tb_check.toggled.connect(func(v): GameManager.turn_based_mode = v)
	tb_row.add_child(tb_check)

func _close() -> void:
	get_tree().paused = false
	queue_free()
