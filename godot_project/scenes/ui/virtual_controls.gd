extends CanvasLayer
## VirtualControls - Mobile touch D-pad and action buttons (landscape layout)

## Left side: 4-way D-pad
## Right side: A (confirm), B (cancel), X (menu), Y (quicksave)

@onready var dpad_up: TouchScreenButton = $DPad/Up
@onready var dpad_down: TouchScreenButton = $DPad/Down
@onready var dpad_left: TouchScreenButton = $DPad/Left
@onready var dpad_right: TouchScreenButton = $DPad/Right
@onready var btn_a: TouchScreenButton = $Buttons/A
@onready var btn_b: TouchScreenButton = $Buttons/B
@onready var btn_x: TouchScreenButton = $Buttons/X
@onready var btn_y: TouchScreenButton = $Buttons/Y

func _ready() -> void:
	add_to_group("virtual_controls")

	# Only show on mobile
	visible = GameManager.is_mobile

	_connect_buttons()
	layer = 10  # Above game, below transition fades

func _connect_buttons() -> void:
	dpad_up.pressed.connect(func(): InputManager.set_virtual_input("up", true))
	dpad_up.released.connect(func(): InputManager.set_virtual_input("up", false))

	dpad_down.pressed.connect(func(): InputManager.set_virtual_input("down", true))
	dpad_down.released.connect(func(): InputManager.set_virtual_input("down", false))

	dpad_left.pressed.connect(func(): InputManager.set_virtual_input("left", true))
	dpad_left.released.connect(func(): InputManager.set_virtual_input("left", false))

	dpad_right.pressed.connect(func(): InputManager.set_virtual_input("right", true))
	dpad_right.released.connect(func(): InputManager.set_virtual_input("right", false))

	btn_a.pressed.connect(func(): InputManager.set_virtual_input("confirm", true))
	btn_a.released.connect(func(): InputManager.set_virtual_input("confirm", false))

	btn_b.pressed.connect(func(): InputManager.set_virtual_input("cancel", true))
	btn_b.released.connect(func(): InputManager.set_virtual_input("cancel", false))

	btn_x.pressed.connect(func(): InputManager.set_virtual_input("menu", true))
	btn_x.released.connect(func(): InputManager.set_virtual_input("menu", false))

	btn_y.pressed.connect(func(): InputManager.set_virtual_input("quicksave", true))
	btn_y.released.connect(func(): InputManager.set_virtual_input("quicksave", false))
