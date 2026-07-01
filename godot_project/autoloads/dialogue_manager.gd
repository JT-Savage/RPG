extends Node
## DialogueManager - Typewriter effect, portraits, branching dialogue

signal dialogue_started
signal dialogue_ended
signal choice_made(choice_index: int, choice_text: String)
signal line_displayed(speaker: String, text: String)

var is_active := false
var current_dialogue: Array = []
var current_line_index := 0
var typewriter_speed: float = 0.03  # seconds per character
var is_typing := false
var skip_requested := false

# Dialogue UI reference (set by battle/world scene)
var dialogue_ui = null

func start_dialogue(dialogue_id: String, context: Dictionary = {}) -> void:
	var dialogue_data := _load_dialogue(dialogue_id, context)
	if dialogue_data.is_empty():
		push_warning("DialogueManager: No dialogue found for '%s'" % dialogue_id)
		return

	is_active = true
	current_dialogue = dialogue_data
	current_line_index = 0
	dialogue_started.emit()
	_show_next_line()

func start_dialogue_direct(lines: Array) -> void:
	is_active = true
	current_dialogue = lines
	current_line_index = 0
	dialogue_started.emit()
	_show_next_line()

func _show_next_line() -> void:
	if current_line_index >= current_dialogue.size():
		end_dialogue()
		return

	var line: Dictionary = current_dialogue[current_line_index]
	var line_type: String = line.get("type", "text")

	match line_type:
		"text":
			_display_text_line(line)
		"choice":
			_display_choice(line)
		"flag_check":
			_process_flag_check(line)
		"flag_set":
			_process_flag_set(line)
		"branch":
			_process_branch(line)
		"recruit":
			_process_recruit(line)
		"key_item":
			_process_key_item(line)
		"cutscene":
			_process_cutscene(line)
		"end":
			end_dialogue()

func _display_text_line(line: Dictionary) -> void:
	var speaker: String = line.get("speaker", "")
	var text: String = line.get("text", "")
	var portrait: String = line.get("portrait", speaker.to_lower())

	# Apply substitutions
	text = _substitute_text(text)

	line_displayed.emit(speaker, text)

	if dialogue_ui and dialogue_ui.has_method("show_line"):
		dialogue_ui.show_line(speaker, text, portrait)
		await dialogue_ui.line_confirmed
	else:
		await _typewriter_wait(text)

	current_line_index += 1
	_show_next_line()

func _typewriter_wait(text: String) -> void:
	is_typing = true
	skip_requested = false
	var duration := text.length() * typewriter_speed

	if not skip_requested:
		await get_tree().create_timer(duration).timeout

	is_typing = false

func _display_choice(line: Dictionary) -> void:
	var choices: Array = line.get("choices", [])
	var filtered_choices := []

	# Filter choices by conditions
	for choice in choices:
		if _check_condition(choice.get("condition", {})):
			filtered_choices.append(choice)

	if filtered_choices.is_empty():
		current_line_index += 1
		_show_next_line()
		return

	if dialogue_ui and dialogue_ui.has_method("show_choices"):
		var chosen_index: int = await dialogue_ui.choice_selected
		var chosen_choice = filtered_choices[min(chosen_index, filtered_choices.size() - 1)]
		choice_made.emit(chosen_index, chosen_choice.get("text", ""))
		_follow_choice(chosen_choice)
	else:
		_follow_choice(filtered_choices[0])

func _follow_choice(choice: Dictionary) -> void:
	# Process choice effects
	if choice.has("flag_set"):
		for key in choice["flag_set"]:
			FlagManager.set_flag(key, choice["flag_set"][key])

	if choice.has("goto"):
		_jump_to_label(choice["goto"])
	elif choice.has("lines"):
		# Inline sub-dialogue
		var saved_dialogue := current_dialogue
		var saved_index := current_line_index
		current_dialogue = choice["lines"]
		current_line_index = 0
		await _wait_for_dialogue_end()
		current_dialogue = saved_dialogue
		current_line_index = saved_index + 1
		_show_next_line()
	else:
		current_line_index += 1
		_show_next_line()

func _process_flag_check(line: Dictionary) -> void:
	if _check_condition(line.get("condition", {})):
		if line.has("goto_true"):
			_jump_to_label(line["goto_true"])
		else:
			current_line_index += 1
			_show_next_line()
	else:
		if line.has("goto_false"):
			_jump_to_label(line["goto_false"])
		else:
			current_line_index += 1
			_show_next_line()

func _process_flag_set(line: Dictionary) -> void:
	for key in line.get("flags", {}):
		FlagManager.set_flag(key, line["flags"][key])
	current_line_index += 1
	_show_next_line()

func _process_branch(line: Dictionary) -> void:
	var branches: Array = line.get("branches", [])
	for branch in branches:
		if _check_condition(branch.get("condition", {})):
			if branch.has("goto"):
				_jump_to_label(branch["goto"])
			else:
				current_line_index += 1
				_show_next_line()
			return
	# Default: next line
	current_line_index += 1
	_show_next_line()

func _process_recruit(line: Dictionary) -> void:
	var char_id: String = line.get("char_id", "")
	if char_id == "":
		current_line_index += 1
		_show_next_line()
		return

	# Show join confirmation dialogue
	var join_text: String = line.get("join_text", "%s wants to join your party!" % char_id.capitalize())
	# Handled by recruitment system
	current_line_index += 1
	_show_next_line()

func _process_key_item(line: Dictionary) -> void:
	var item_id: String = line.get("item_id", "")
	if item_id != "":
		GameManager.add_key_item(item_id)
	current_line_index += 1
	_show_next_line()

func _process_cutscene(line: Dictionary) -> void:
	var cutscene_id: String = line.get("cutscene_id", "")
	# Signal to cutscene system
	current_line_index += 1
	_show_next_line()

func _jump_to_label(label: String) -> void:
	for i in range(current_dialogue.size()):
		if current_dialogue[i].get("label", "") == label:
			current_line_index = i
			_show_next_line()
			return
	push_warning("DialogueManager: Label '%s' not found" % label)
	current_line_index += 1
	_show_next_line()

func _check_condition(condition: Dictionary) -> bool:
	if condition.is_empty():
		return true

	for key in condition:
		var expected = condition[key]
		var actual = FlagManager.get_flag(key)
		if actual != expected:
			return false
	return true

func _substitute_text(text: String) -> String:
	# Replace placeholders
	text = text.replace("{baby_dragon_name}", str(FlagManager.get_flag("baby_dragon_name")))
	text = text.replace("{yipp_alignment}", str(FlagManager.get_flag("yipp_alignment")))
	text = text.replace("{playthrough_count}", str(GameManager.playthrough_count))
	return text

func _load_dialogue(dialogue_id: String, context: Dictionary) -> Array:
	var path := "res://data/dialogues/%s.json" % dialogue_id
	if not ResourceLoader.exists(path):
		return []
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return []
	var parsed := JSON.parse_string(file.get_as_text())
	file.close()
	if parsed == null:
		return []
	return parsed if parsed is Array else parsed.get("lines", [])

func _wait_for_dialogue_end() -> void:
	while is_active and current_dialogue != []:
		await get_tree().process_frame

func end_dialogue() -> void:
	is_active = false
	current_dialogue = []
	current_line_index = 0
	dialogue_ended.emit()

func skip_typewriter() -> void:
	skip_requested = true

func set_typewriter_speed(chars_per_second: float) -> void:
	typewriter_speed = 1.0 / chars_per_second
