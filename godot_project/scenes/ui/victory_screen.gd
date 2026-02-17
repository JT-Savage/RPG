extends Control
## VictoryScreen - Post-battle rewards then returns to overworld

@onready var exp_label: Label = $ExpLabel
@onready var gil_label: Label = $GilLabel
@onready var level_up_container: VBoxContainer = $LevelUpsContainer
@onready var continue_label: Label = $ContinueLabel

func _ready() -> void:
	AudioManager.play_music("victory", 0.2)
	_show_results()

func _show_results() -> void:
	exp_label.text = "EXP gained: %d" % BattleManager.pending_exp
	gil_label.text = "Gil gained: %d" % BattleManager.pending_gil
	continue_label.text = "Press [Z] / [A] to continue"

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("action_confirm"):
		_return_to_world()

func _return_to_world() -> void:
	SceneTransition.change_scene(
		"res://scenes/locations/%s.tscn" % GameManager.current_location)
