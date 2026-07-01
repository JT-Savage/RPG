# CutscenePlayer.gd
# Autoload singleton for "There Will Be Kobolds"
#
# REGISTRATION REMINDER:
# In Project > Project Settings > Autoloads, add this file as "CutscenePlayer"
# (Node name: CutscenePlayer, Path: res://autoloads/cutscene_player.gd)
# It must load before BattleManager and any scene that calls CutscenePlayer.play().

extends Node
class_name CutscenePlayer

signal cutscene_finished(cutscene_id: String)

# ---------------------------------------------------------------------------
# Action type reference:
#   "dialogue"      : { "dialogue_id": String }
#   "wait"          : { "duration": float }
#   "play_sfx"      : { "sfx_name": String, "volume_db": float (opt) }
#   "play_music"    : { "track_name": String, "fade_in": float (opt) }
#   "flash"         : { "color": Color, "duration": float (opt) }
#   "fade_out"      : { "duration": float (opt) }
#   "fade_in"       : { "duration": float (opt) }
#   "move_npc"      : { "npc_id": String, "target_pos": Vector2, "duration": float (opt) }
#   "set_flag"      : { "flag": String, "value": Variant (opt, default true) }
#   "spawn_effect"  : { "effect_name": String, "anchor": String (opt), "position": Vector2 (opt) }
#   "shake_camera"  : { "strength": String ("light"|"medium"|"strong"), "duration": float }
# ---------------------------------------------------------------------------

const CUTSCENES: Dictionary = {

	# ------------------------------------------------------------------
	# warren_infection_spread
	# Quick environmental horror beat — the warren is fully lost.
	# ------------------------------------------------------------------
	"warren_infection_spread": [
		{
			"type": "shake_camera",
			"strength": "medium",
			"duration": 0.6
		},
		{
			"type": "play_sfx",
			"sfx_name": "status_poison",
			"volume_db": 0.0
		},
		{
			"type": "wait",
			"duration": 0.4
		},
		{
			"type": "shake_camera",
			"strength": "light",
			"duration": 2.0
		},
		{
			"type": "set_flag",
			"flag": "warren_full_infection",
			"value": true
		}
	],

	# ------------------------------------------------------------------
	# jerod_detonates
	# Jerod's self-detonation. Flash, boom, shake, fade to black.
	# ------------------------------------------------------------------
	"jerod_detonates": [
		{
			"type": "flash",
			"color": Color(1.0, 1.0, 1.0, 1.0),
			"duration": 0.15,
			"sfx_trigger": "hannah_scream_flash"
		},
		{
			"type": "wait",
			"duration": 0.5
		},
		{
			"type": "play_sfx",
			"sfx_name": "jerod_explosion",
			"volume_db": 3.0
		},
		{
			"type": "shake_camera",
			"strength": "strong",
			"duration": 1.0
		},
		{
			"type": "fade_out",
			"duration": 0.4
		},
		{
			"type": "wait",
			"duration": 1.5
		},
		{
			"type": "fade_in",
			"duration": 0.6
		}
	],

	# ------------------------------------------------------------------
	# flood_dramatic_death
	# Flood dies. A moment of silence, then Hannah's scream, then gone.
	# ------------------------------------------------------------------
	"flood_dramatic_death": [
		{
			"type": "play_sfx",
			"sfx_name": "flood_death",
			"volume_db": 0.0
		},
		{
			"type": "wait",
			"duration": 1.0
		},
		{
			"type": "play_sfx",
			"sfx_name": "hannah_scream",
			"volume_db": 2.0
		},
		{
			"type": "flash",
			"color": Color(1.0, 1.0, 1.0, 0.85),
			"duration": 0.25
		},
		{
			"type": "set_flag",
			"flag": "flood_permanent_death",
			"value": true
		}
	],

	# ------------------------------------------------------------------
	# orisia_class_evolution
	# Each party member with a completed sidequest evolves their class.
	# The anchor "kella_position" is resolved at runtime via context.
	# Flags use the template "class_evolved_{char_id}" — resolved at runtime.
	# ------------------------------------------------------------------
	"orisia_class_evolution": [
		{
			"type": "play_music",
			"track_name": "orisia_theme",
			"fade_in": 1.5
		},
		{
			"type": "spawn_effect",
			"effect_name": "spell_light",
			"anchor": "kella_position"
		},
		{
			"type": "wait",
			"duration": 1.5
		},
		{
			"type": "set_flag",
			"flag": "class_evolved_{char_id}",
			"value": true,
			"mode": "per_party_member",
			"condition": "sidequest_complete"
		}
	],

	# ------------------------------------------------------------------
	# final_boss_intro
	# Fade out, music swap, fade in, shake, darkness blooms.
	# ------------------------------------------------------------------
	"final_boss_intro": [
		{
			"type": "fade_out",
			"duration": 0.8
		},
		{
			"type": "play_music",
			"track_name": "battle_final",
			"fade_in": 0.0
		},
		{
			"type": "fade_in",
			"duration": 1.2
		},
		{
			"type": "shake_camera",
			"strength": "medium",
			"duration": 2.0
		},
		{
			"type": "spawn_effect",
			"effect_name": "spell_darkness",
			"anchor": "screen_center"
		}
	],

	# ------------------------------------------------------------------
	# secret_boss_intro
	# Something is wrong. The game itself feels wrong.
	# ------------------------------------------------------------------
	"secret_boss_intro": [
		{
			"type": "shake_camera",
			"strength": "strong",
			"duration": 0.5
		},
		{
			"type": "flash",
			"color": Color(0.0, 0.0, 0.0, 1.0),
			"duration": 0.1
		},
		{
			"type": "play_sfx",
			"sfx_name": "error",
			"volume_db": -6.0,
			"pitch_scale": 0.6
		},
		{
			"type": "wait",
			"duration": 1.0
		}
	],

	# ------------------------------------------------------------------
	# good_ending_credits
	# Slow fade, gentle music. Let it breathe.
	# ------------------------------------------------------------------
	"good_ending_credits": [
		{
			"type": "fade_out",
			"duration": 3.0
		},
		{
			"type": "play_music",
			"track_name": "ending_good",
			"fade_in": 2.0
		}
	],

	# ------------------------------------------------------------------
	# baby_dragon_egg_hatches
	# Small and precious. A chest-open sound, a burst of light, a pause.
	# ------------------------------------------------------------------
	"baby_dragon_egg_hatches": [
		{
			"type": "wait",
			"duration": 0.5
		},
		{
			"type": "play_sfx",
			"sfx_name": "chest_open",
			"volume_db": 0.0
		},
		{
			"type": "spawn_effect",
			"effect_name": "spell_light",
			"anchor": "egg_position"
		},
		{
			"type": "wait",
			"duration": 1.0
		}
	]
}

# ---------------------------------------------------------------------------
# Internal state
# ---------------------------------------------------------------------------
var _is_playing: bool = false
var _current_cutscene_id: String = ""

# Node references — resolved at play() time via context dict.
# context keys (all optional):
#   "sfx_player"    : AudioStreamPlayer node for SFX
#   "music_player"  : AudioStreamPlayer node for music
#   "camera"        : Camera2D node
#   "overlay"       : ColorRect / CanvasLayer for flash/fade
#   "npc_nodes"     : Dictionary { npc_id: Node2D }
#   "effect_spawner": Node that exposes spawn_effect(name, pos) method
#   "flag_manager"  : Node that exposes set_flag(key, value) and get_flag(key)
#   "party"         : Array of character Dictionaries ({ "id", "sidequest_complete", ... })
#   "anchors"       : Dictionary { anchor_name: Vector2 } for effect spawn positions

var _context: Dictionary = {}

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

## Play a cutscene by ID.
## context: runtime node/data references (see above).
## Returns immediately; await cutscene_finished signal if you need to block.
func play(cutscene_id: String, context: Dictionary = {}) -> void:
	if _is_playing:
		push_warning("CutscenePlayer: tried to play '%s' while '%s' is running. Ignored." \
			% [cutscene_id, _current_cutscene_id])
		return

	if not CUTSCENES.has(cutscene_id):
		push_error("CutscenePlayer: unknown cutscene_id '%s'." % cutscene_id)
		return

	_is_playing = true
	_current_cutscene_id = cutscene_id
	_context = context

	var actions: Array = CUTSCENES[cutscene_id]
	await _execute_sequence(actions)

	_is_playing = false
	_current_cutscene_id = ""
	_context = {}
	cutscene_finished.emit(cutscene_id)


## Returns true if a cutscene is currently running.
func is_playing() -> bool:
	return _is_playing


## Cancel the current cutscene immediately (does not finish pending await timers).
## Emits cutscene_finished with the interrupted id.
func cancel() -> void:
	if not _is_playing:
		return
	var interrupted_id := _current_cutscene_id
	_is_playing = false
	_current_cutscene_id = ""
	_context = {}
	cutscene_finished.emit(interrupted_id)

# ---------------------------------------------------------------------------
# Sequence executor
# ---------------------------------------------------------------------------

func _execute_sequence(actions: Array) -> void:
	for action in actions:
		if not _is_playing:
			# Cancelled mid-sequence.
			return
		await _execute_action(action)


func _execute_action(action: Dictionary) -> void:
	var t: String = action.get("type", "")
	match t:
		"wait":
			await _action_wait(action)
		"play_sfx":
			_action_play_sfx(action)
		"play_music":
			_action_play_music(action)
		"flash":
			await _action_flash(action)
		"fade_out":
			await _action_fade_out(action)
		"fade_in":
			await _action_fade_in(action)
		"shake_camera":
			await _action_shake_camera(action)
		"move_npc":
			await _action_move_npc(action)
		"set_flag":
			_action_set_flag(action)
		"spawn_effect":
			_action_spawn_effect(action)
		"dialogue":
			await _action_dialogue(action)
		_:
			push_warning("CutscenePlayer: unknown action type '%s'." % t)

# ---------------------------------------------------------------------------
# Individual action handlers
# ---------------------------------------------------------------------------

func _action_wait(action: Dictionary) -> void:
	var duration: float = action.get("duration", 1.0)
	await get_tree().create_timer(duration).timeout


func _action_play_sfx(action: Dictionary) -> void:
	var sfx_name: String = action.get("sfx_name", "")
	var volume_db: float = action.get("volume_db", 0.0)
	var pitch_scale: float = action.get("pitch_scale", 1.0)

	var sfx_player = _context.get("sfx_player", null)
	if sfx_player == null:
		push_warning("CutscenePlayer: no sfx_player in context for sfx '%s'." % sfx_name)
		return

	# Assumes sfx_player has a play_named(name, volume_db, pitch) method,
	# or is an AudioStreamPlayer whose stream is swapped by an SFX bus.
	if sfx_player.has_method("play_named"):
		sfx_player.play_named(sfx_name, volume_db, pitch_scale)
	else:
		push_warning("CutscenePlayer: sfx_player has no play_named() method.")


func _action_play_music(action: Dictionary) -> void:
	var track_name: String = action.get("track_name", "")
	var fade_in: float = action.get("fade_in", 0.0)

	var music_player = _context.get("music_player", null)
	if music_player == null:
		push_warning("CutscenePlayer: no music_player in context for track '%s'." % track_name)
		return

	if music_player.has_method("play_track"):
		music_player.play_track(track_name, fade_in)
	else:
		push_warning("CutscenePlayer: music_player has no play_track() method.")


func _action_flash(action: Dictionary) -> void:
	var color: Color = action.get("color", Color(1, 1, 1, 1))
	var duration: float = action.get("duration", 0.15)

	var overlay: CanvasItem = _context.get("overlay", null)
	if overlay == null:
		push_warning("CutscenePlayer: no overlay in context for flash.")
		await get_tree().create_timer(duration).timeout
		return

	overlay.modulate = color
	overlay.visible = true
	var tween := get_tree().create_tween()
	tween.tween_property(overlay, "modulate:a", 0.0, duration)
	await tween.finished
	overlay.visible = false
	overlay.modulate = color


func _action_fade_out(action: Dictionary) -> void:
	var duration: float = action.get("duration", 0.5)
	var overlay: CanvasItem = _context.get("overlay", null)
	if overlay == null:
		push_warning("CutscenePlayer: no overlay in context for fade_out.")
		await get_tree().create_timer(duration).timeout
		return

	overlay.modulate = Color(0, 0, 0, 0)
	overlay.visible = true
	var tween := get_tree().create_tween()
	tween.tween_property(overlay, "modulate:a", 1.0, duration)
	await tween.finished


func _action_fade_in(action: Dictionary) -> void:
	var duration: float = action.get("duration", 0.5)
	var overlay: CanvasItem = _context.get("overlay", null)
	if overlay == null:
		push_warning("CutscenePlayer: no overlay in context for fade_in.")
		await get_tree().create_timer(duration).timeout
		return

	var tween := get_tree().create_tween()
	tween.tween_property(overlay, "modulate:a", 0.0, duration)
	await tween.finished
	overlay.visible = false


func _action_shake_camera(action: Dictionary) -> void:
	var strength_key: String = action.get("strength", "medium")
	var duration: float = action.get("duration", 0.5)

	var camera = _context.get("camera", null)
	if camera == null:
		push_warning("CutscenePlayer: no camera in context for shake_camera.")
		await get_tree().create_timer(duration).timeout
		return

	var amplitude: float = _shake_amplitude(strength_key)

	if camera.has_method("shake"):
		# Prefer a dedicated shake method if the camera exposes one.
		camera.shake(amplitude, duration)
		await get_tree().create_timer(duration).timeout
	else:
		# Fallback: manual random offset tween loop.
		var original_offset: Vector2 = camera.offset
		var elapsed: float = 0.0
		while elapsed < duration:
			var delta: float = get_process_delta_time()
			elapsed += delta
			var t_remaining: float = 1.0 - clampf(elapsed / duration, 0.0, 1.0)
			camera.offset = original_offset + Vector2(
				randf_range(-amplitude, amplitude) * t_remaining,
				randf_range(-amplitude, amplitude) * t_remaining
			)
			await get_tree().process_frame
		camera.offset = original_offset


func _action_move_npc(action: Dictionary) -> void:
	var npc_id: String = action.get("npc_id", "")
	var target_pos: Vector2 = action.get("target_pos", Vector2.ZERO)
	var duration: float = action.get("duration", 1.0)

	var npc_nodes: Dictionary = _context.get("npc_nodes", {})
	if not npc_nodes.has(npc_id):
		push_warning("CutscenePlayer: npc_id '%s' not found in context npc_nodes." % npc_id)
		await get_tree().create_timer(duration).timeout
		return

	var npc: Node2D = npc_nodes[npc_id]
	var tween := get_tree().create_tween()
	tween.tween_property(npc, "position", target_pos, duration).set_trans(Tween.TRANS_SINE)
	await tween.finished


func _action_set_flag(action: Dictionary) -> void:
	var flag_manager = _context.get("flag_manager", null)
	var mode: String = action.get("mode", "single")
	var base_flag: String = action.get("flag", "")
	var value: Variant = action.get("value", true)

	if flag_manager == null:
		push_warning("CutscenePlayer: no flag_manager in context. Flag '%s' not set." % base_flag)
		return

	if mode == "per_party_member":
		# Expand template flag for each qualifying party member.
		var party: Array = _context.get("party", [])
		var condition: String = action.get("condition", "")
		for member in party:
			if condition == "" or member.get(condition, false):
				var resolved_flag: String = base_flag.replace("{char_id}", member.get("id", "unknown"))
				if flag_manager.has_method("set_flag"):
					flag_manager.set_flag(resolved_flag, value)
	else:
		if flag_manager.has_method("set_flag"):
			flag_manager.set_flag(base_flag, value)


func _action_spawn_effect(action: Dictionary) -> void:
	var effect_name: String = action.get("effect_name", "")
	var anchor_key: String = action.get("anchor", "screen_center")
	var override_pos: Variant = action.get("position", null)

	var effect_spawner = _context.get("effect_spawner", null)
	if effect_spawner == null:
		push_warning("CutscenePlayer: no effect_spawner in context for effect '%s'." % effect_name)
		return

	var spawn_pos: Vector2
	if override_pos != null:
		spawn_pos = override_pos
	else:
		var anchors: Dictionary = _context.get("anchors", {})
		spawn_pos = anchors.get(anchor_key, Vector2.ZERO)

	if effect_spawner.has_method("spawn_effect"):
		effect_spawner.spawn_effect(effect_name, spawn_pos)
	else:
		push_warning("CutscenePlayer: effect_spawner has no spawn_effect() method.")


func _action_dialogue(action: Dictionary) -> void:
	var dialogue_id: String = action.get("dialogue_id", "")
	# Assumes a DialogueManager autoload or similar exists.
	# DialogueManager is an autoload (not an Engine singleton) — call directly.
	DialogueManager.start_dialogue(dialogue_id)
	await DialogueManager.dialogue_ended

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

func _shake_amplitude(strength_key: String) -> float:
	match strength_key:
		"light":  return 4.0
		"medium": return 10.0
		"strong": return 22.0
		_:
			push_warning("CutscenePlayer: unknown shake strength '%s', defaulting to medium." % strength_key)
			return 10.0
