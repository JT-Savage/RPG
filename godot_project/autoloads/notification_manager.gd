## notification_manager.gd
## Shows floating item/key item pickup notifications and other brief popups.
## Used by locations when player opens chests or receives items.
extends CanvasLayer

const NOTIFY_DURATION: float = 2.5
const FLOAT_SPEED: float = 30.0

var _active_notifications: Array[Control] = []


func _ready() -> void:
	layer = 90  # Below pause menu but above gameplay


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

## Show a key item acquisition popup (large, centered)
func show_key_item(item_id: String) -> void:
	var KeyItemDB = load("res://data/key_items/key_item_database.gd")
	var data: Dictionary = {}
	if KeyItemDB:
		data = KeyItemDB.get_key_item(item_id)

	var name_text: String = data.get("name", item_id.replace("_", " ").capitalize())
	var desc_text: String = data.get("description", "")

	_show_popup("Obtained: %s" % name_text, desc_text, Color(1.0, 0.9, 0.3))


## Show a regular item acquisition notification (small, corner)
func show_item(item_id: String, quantity: int = 1) -> void:
	var ItemDB = load("res://data/items/item_database.gd")
	var data: Dictionary = {}
	if ItemDB:
		data = ItemDB.get_item(item_id)

	var name_text: String = data.get("name", item_id.replace("_", " ").capitalize())
	var msg: String = "Got %s" % name_text
	if quantity > 1:
		msg = "Got %s x%d" % [name_text, quantity]

	_show_toast(msg, Color(0.8, 1.0, 0.8))


## Show a Gil earned notification
func show_gil(amount: int) -> void:
	_show_toast("+ %d Gil" % amount, Color(1.0, 0.9, 0.2))


## Show a level-up notification
func show_level_up(char_name: String, new_level: int) -> void:
	_show_popup("%s reached Level %d!" % [char_name, new_level], "", Color(0.5, 0.8, 1.0))


## Show a custom message
func show_message(text: String, color: Color = Color.WHITE) -> void:
	_show_toast(text, color)


# ---------------------------------------------------------------------------
# Internal – small floating toast (bottom-left)
# ---------------------------------------------------------------------------
func _show_toast(text: String, color: Color) -> void:
	var label := Label.new()
	label.text = text
	label.modulate = color
	label.add_theme_font_size_override("font_size", 8)

	var panel := Panel.new()
	panel.add_child(label)
	label.set_anchors_and_offsets_preset(Control.PRESET_CENTER)

	# Position: bottom-left stack, floating up
	var start_y: float = 200.0 - float(_active_notifications.size()) * 14.0
	panel.size = Vector2(120, 12)
	panel.position = Vector2(4, start_y)
	add_child(panel)
	_active_notifications.append(panel)

	_animate_and_remove(panel)


# ---------------------------------------------------------------------------
# Internal – large centered popup (for key items)
# ---------------------------------------------------------------------------
func _show_popup(title: String, desc: String, color: Color) -> void:
	AudioManager.play_sfx("key_item_get")

	var bg := Panel.new()
	bg.size = Vector2(200, 60)
	bg.position = Vector2(28, 82)    # Centered in 256x224
	add_child(bg)

	var vbox := VBoxContainer.new()
	vbox.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	bg.add_child(vbox)

	var title_label := Label.new()
	title_label.text = title
	title_label.modulate = color
	title_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title_label.add_theme_font_size_override("font_size", 9)
	vbox.add_child(title_label)

	if not desc.is_empty():
		var desc_label := Label.new()
		desc_label.text = desc
		desc_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		desc_label.add_theme_font_size_override("font_size", 7)
		desc_label.autowrap_mode = TextServer.AUTOWRAP_WORD
		vbox.add_child(desc_label)

	_active_notifications.append(bg)

	# Wait for player input or timeout to dismiss
	await get_tree().create_timer(NOTIFY_DURATION).timeout
	if Input.is_anything_pressed():
		pass  # Dismiss immediately
	_remove_notification(bg)


func _animate_and_remove(node: Control) -> void:
	var tween := create_tween()
	# Float up then fade
	tween.tween_property(node, "position:y", node.position.y - 20.0, NOTIFY_DURATION * 0.7)
	tween.parallel().tween_property(node, "modulate:a", 0.0, NOTIFY_DURATION)
	await tween.finished
	_remove_notification(node)


func _remove_notification(node: Control) -> void:
	_active_notifications.erase(node)
	if is_instance_valid(node):
		node.queue_free()
