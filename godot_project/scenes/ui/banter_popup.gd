extends Control

## BanterPopup — a non-blocking overlay that appears briefly in the top-left
## corner of the screen when the BanterSystem fires a banter_triggered signal.
## The popup fades + slides in, holds for DISPLAY_DURATION seconds, then fades
## + slides out.  It never pauses the battle; all animation runs via Tweens so
## the ATB continues uninterrupted.
##
## Expected scene tree:
##   BanterPopup (Control, this script)
##   └─ Panel
##      ├─ SpeakerLabel (Label)
##      └─ TextLabel   (Label)
##
## Suggested anchors: top-left corner, position (16, 16), width ~340 px.

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

## How many seconds the popup stays fully visible before fading out.
const DISPLAY_DURATION: float = 3.0

## Duration of the fade-in / slide-in animation.
const ANIM_IN_DURATION: float = 0.25

## Duration of the fade-out / slide-out animation.
const ANIM_OUT_DURATION: float = 0.35

## How many pixels the panel slides in from the left edge on entry.
const SLIDE_OFFSET_X: float = -24.0

# ---------------------------------------------------------------------------
# Node references — populated by @onready so the scene tree must match above.
# ---------------------------------------------------------------------------

@onready var speaker_label: Label = $Panel/SpeakerLabel
@onready var text_label: Label    = $Panel/TextLabel
@onready var panel: Panel         = $Panel

# ---------------------------------------------------------------------------
# Private state
# ---------------------------------------------------------------------------

## Reference to the active tween so we can kill it if a new banter line
## arrives while the current one is still animating.
var _tween: Tween = null

## Resting position of the panel (recorded once in _ready so animations are
## always relative to the authored position, not an accumulated offset).
var _panel_rest_position: Vector2 = Vector2.ZERO

# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------

func _ready() -> void:
	# Hide immediately; the popup should be invisible until triggered.
	modulate.a = 0.0
	visible = false

	# Record the panel's designed position before any animation touches it.
	_panel_rest_position = panel.position

	# Connect to the global banter system if it is registered as an autoload.
	if Engine.has_singleton("BanterSystem"):
		BanterSystem.banter_triggered.connect(_on_banter_triggered)
	else:
		# Fallback: allow callers to invoke show_banter() directly, e.g. from
		# a battle manager that holds its own reference to BanterSystem.
		push_warning("BanterPopup: BanterSystem singleton not found; connect manually.")

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

## Display a banter line.  Safe to call while a previous line is still showing
## — the old animation is cancelled and the new line takes over immediately.
func show_banter(speaker: String, text: String) -> void:
	# Cancel any animation that is currently running.
	if _tween != null and _tween.is_valid():
		_tween.kill()
		_tween = null

	# Populate labels.
	speaker_label.text = speaker
	text_label.text    = text

	# Reset panel to its off-screen starting position before animating in.
	panel.position = _panel_rest_position + Vector2(SLIDE_OFFSET_X, 0.0)

	visible    = true
	modulate.a = 0.0

	# Build a single chained tween: in → hold → out.
	_tween = create_tween()
	_tween.set_parallel(false)  # Steps run sequentially.

	# --- Step 1: Animate in (fade + slide) ---
	_tween.tween_property(self,  "modulate:a",   1.0,                 ANIM_IN_DURATION).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)
	_tween.parallel().tween_property(panel, "position", _panel_rest_position, ANIM_IN_DURATION).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)

	# --- Step 2: Hold for DISPLAY_DURATION ---
	_tween.tween_interval(DISPLAY_DURATION)

	# --- Step 3: Animate out (fade only; panel stays in place) ---
	_tween.tween_property(self, "modulate:a", 0.0, ANIM_OUT_DURATION).set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_CUBIC)

	# --- Step 4: Hide the node so it does not intercept input ---
	_tween.tween_callback(_on_animation_finished)


## Hide the popup immediately, cutting any running animation.  Useful if the
## battle ends while a banter line is in flight.
func dismiss() -> void:
	if _tween != null and _tween.is_valid():
		_tween.kill()
		_tween = null
	modulate.a = 0.0
	visible    = false

# ---------------------------------------------------------------------------
# Private callbacks
# ---------------------------------------------------------------------------

func _on_banter_triggered(speaker: String, text: String) -> void:
	show_banter(speaker, text)


func _on_animation_finished() -> void:
	visible    = false
	modulate.a = 0.0
	# Restore panel position so the next show_banter() starts from a clean state.
	panel.position = _panel_rest_position
