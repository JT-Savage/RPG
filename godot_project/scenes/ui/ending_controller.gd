## ending_controller.gd
## Routes to the correct ending sequence based on story flags.
## Triggered by StoryEventSystem after the final boss is defeated.
## Handles credits roll and NG+ save prompt.
extends Node
class_name EndingController

# ---------------------------------------------------------------------------
# Signals
# ---------------------------------------------------------------------------
signal ending_complete(ending_type: String)

# ---------------------------------------------------------------------------
# Ending types
# ---------------------------------------------------------------------------
const ENDING_GOOD: String = "good"
const ENDING_NORMAL: String = "normal"
const ENDING_BAD: String = "bad"       # Secret boss ending
const ENDING_BEST: String = "best"    # All recruited + Orisia sidequest complete


# ---------------------------------------------------------------------------
# _ready
# ---------------------------------------------------------------------------
func _ready() -> void:
	# Triggered externally by StoryEventSystem
	pass


# ---------------------------------------------------------------------------
# Public – called by StoryEventSystem.determine_ending()
# ---------------------------------------------------------------------------
func play_ending(ending_type: String) -> void:
	FlagManager.set_flag("ending_achieved", ending_type)
	AudioManager.play_sfx("victory_fanfare")

	match ending_type:
		ENDING_BEST:
			await _play_best_ending()
		ENDING_GOOD:
			await _play_good_ending()
		ENDING_BAD:
			await _play_bad_ending()
		_:
			await _play_normal_ending()

	# After credits, offer NG+
	await _prompt_ng_plus(ending_type)


# ---------------------------------------------------------------------------
# Ending sequences
# ---------------------------------------------------------------------------
func _play_good_ending() -> void:
	AudioManager.play_music("ending_good")
	DialogueManager.start_dialogue("good_ending")
	await DialogueManager.dialogue_ended
	await _roll_credits(ENDING_GOOD)


func _play_normal_ending() -> void:
	AudioManager.play_music("ending_normal")
	# Brief ending narration
	DialogueManager.start_dialogue_direct([
		{"id": "line", "type": "text", "speaker": "Narrator", "text": "The darkness was beaten back. Not destroyed—it never is. But pushed back far enough that sunlight returned to places that had forgotten it.", "next": "end"},
		{"id": "end", "type": "end"}
	])
	await DialogueManager.dialogue_ended
	await _roll_credits(ENDING_NORMAL)


func _play_bad_ending() -> void:
	# Secret boss defeated
	AudioManager.play_music("ending_bad")
	DialogueManager.start_dialogue("bad_ending")
	await DialogueManager.dialogue_ended
	FlagManager.set_flag("secret_boss_defeated", true)
	await _roll_credits(ENDING_BAD)


func _play_best_ending() -> void:
	AudioManager.play_music("ending_best")
	FlagManager.set_flag("best_ending_achieved", true)
	DialogueManager.start_dialogue("good_ending")
	await DialogueManager.dialogue_ended   # Good ending first
	await _roll_credits(ENDING_BEST)
	# Post-credits sequence
	await get_tree().create_timer(1.0).timeout
	DialogueManager.start_dialogue("best_ending")
	await DialogueManager.dialogue_ended   # Then post-credits


# ---------------------------------------------------------------------------
# Credits roll
# ---------------------------------------------------------------------------
func _roll_credits(ending_type: String) -> void:
	var credits_scene: PackedScene = load("res://scenes/ui/credits_screen.tscn")
	if credits_scene == null:
		push_error("EndingController: Could not load credits_screen.tscn")
		return

	var credits = credits_scene.instantiate()
	credits.set_meta("ending_type", ending_type)
	get_tree().root.add_child(credits)

	# Wait for credits to finish (credits emits "credits_finished" signal)
	if credits.has_signal("credits_finished"):
		await credits.credits_finished
	else:
		await get_tree().create_timer(30.0).timeout

	if is_instance_valid(credits):
		credits.queue_free()


# ---------------------------------------------------------------------------
# NG+ prompt
# ---------------------------------------------------------------------------
func _prompt_ng_plus(ending_type: String) -> void:
	# Determine NG+ starting level
	var start_level: int = 75
	if FlagManager.is_flag("orisia_sidequest_complete"):
		start_level = 99
	elif ending_type == ENDING_BEST:
		start_level = 99

	# Ask player if they want to start NG+
	var confirmed: bool = await _show_ng_plus_dialog(start_level)

	if confirmed:
		# Save NG+ data and restart
		var ng_data: Dictionary = NGPlusManager.collect_ng_plus_data()
		SaveSystem.save_ng_plus_data()
		await SceneTransition.fade_out()
		GameManager.new_game(ng_data)
		SceneTransition.change_scene("res://scenes/title/title_screen.tscn")
	else:
		# Return to title
		SceneTransition.change_scene("res://scenes/title/title_screen.tscn")

	emit_signal("ending_complete", ending_type)


func _show_ng_plus_dialog(start_level: int) -> bool:
	# Simple confirmation dialog
	var dialog: AcceptDialog = AcceptDialog.new()
	dialog.title = "New Game+"
	dialog.dialog_text = (
		"Start New Game+?\n\n"
		+ "Your party begins at Level %d.\n" % start_level
		+ "Story decisions carry over as commentary.\n"
		+ "Character unlocks and progress reset."
	)
	dialog.add_cancel_button("Return to Title")
	get_tree().root.add_child(dialog)
	dialog.popup_centered()

	var result: bool = false
	if dialog.has_signal("confirmed"):
		var confirmed_signal = await _wait_for_dialog(dialog)
		result = confirmed_signal

	if is_instance_valid(dialog):
		dialog.queue_free()
	return result


func _wait_for_dialog(dialog: AcceptDialog) -> bool:
	var result: Array[bool] = [false]

	var confirmed_cb = func():
		result[0] = true
	var cancelled_cb = func():
		result[0] = false

	dialog.confirmed.connect(confirmed_cb, CONNECT_ONE_SHOT)
	dialog.canceled.connect(cancelled_cb, CONNECT_ONE_SHOT)

	# Wait until one fires
	while dialog.visible:
		await get_tree().process_frame

	return result[0]
