extends Control

# Mode is either "save" or "load"
var mode: String = "save"
var selected_slot: int = -1
var slot_buttons: Array = []

const TOTAL_SLOTS: int = 100

@onready var title_label: Label = $Panel/VBoxContainer/TitleLabel
@onready var slot_list: VBoxContainer = $Panel/VBoxContainer/ScrollContainer/SlotList
@onready var save_button: Button = $Panel/VBoxContainer/ButtonRow/SaveButton
@onready var load_button: Button = $Panel/VBoxContainer/ButtonRow/LoadButton
@onready var delete_button: Button = $Panel/VBoxContainer/ButtonRow/DeleteButton
@onready var cancel_button: Button = $Panel/VBoxContainer/ButtonRow/CancelButton


func _ready() -> void:
	cancel_button.pressed.connect(_on_cancel_pressed)
	save_button.pressed.connect(_on_save_pressed)
	load_button.pressed.connect(_on_load_pressed)
	delete_button.pressed.connect(_on_delete_pressed)
	_build_slot_list()
	_update_mode_ui()


func set_mode(new_mode: String) -> void:
	mode = new_mode
	_update_mode_ui()


func _update_mode_ui() -> void:
	if mode == "save":
		title_label.text = "Save Game"
		save_button.disabled = false
		load_button.disabled = true
	else:
		title_label.text = "Load Game"
		save_button.disabled = true
		load_button.disabled = false


func _build_slot_list() -> void:
	for child in slot_list.get_children():
		child.queue_free()
	slot_buttons.clear()

	for i in range(1, TOTAL_SLOTS + 1):
		var slot_data = SaveSystem.get_slot_info(i) if SaveSystem else null
		var btn := Button.new()
		btn.text = _format_slot_text(i, slot_data)
		btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
		btn.toggle_mode = true
		btn.pressed.connect(_on_slot_selected.bind(i, btn))
		slot_list.add_child(btn)
		slot_buttons.append(btn)


func _format_slot_text(slot_num: int, data) -> String:
	var prefix := "Slot %02d" % slot_num
	if data == null or not data.get("exists", false):
		return prefix + " — Empty"
	var char_name: String = data.get("character_name", "Unknown")
	var location: String = data.get("location", "Unknown")
	var play_time: String = data.get("play_time", "00:00:00")
	var save_date: String = data.get("date", "")
	return "%s | %s | %s | %s | %s" % [prefix, char_name, location, play_time, save_date]


func _on_slot_selected(slot_num: int, btn: Button) -> void:
	selected_slot = slot_num
	for b in slot_buttons:
		if b != btn:
			b.button_pressed = false


func _on_save_pressed() -> void:
	if selected_slot < 1:
		return
	if SaveSystem:
		SaveSystem.save_slot(selected_slot)
	_build_slot_list()


func _on_load_pressed() -> void:
	if selected_slot < 1:
		return
	if SaveSystem:
		SaveSystem.load_slot(selected_slot)
	if SceneManager:
		SceneManager.transition_to_game()


func _on_delete_pressed() -> void:
	if selected_slot < 1:
		return
	if SaveSystem:
		SaveSystem.delete_slot(selected_slot)
	_build_slot_list()
	selected_slot = -1


func _on_cancel_pressed() -> void:
	queue_free()
