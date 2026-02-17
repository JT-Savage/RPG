extends Node
## AudioManager - Music fade, SFX play, volume control

@onready var music_player: AudioStreamPlayer = $MusicPlayer
@onready var sfx_player: AudioStreamPlayer = $SFXPlayer
@onready var sfx_player2: AudioStreamPlayer = $SFXPlayer2  # For overlapping SFX

var current_music_track := ""
var music_volume_db := 0.0
var sfx_volume_db := 0.0
var master_volume_db := 0.0
var is_fading := false
var fade_tween: Tween

const MUSIC_TRACKS := {
	"title": "res://assets/audio/music/title_theme.ogg",
	"overworld": "res://assets/audio/music/overworld.ogg",
	"battle": "res://assets/audio/music/battle.ogg",
	"battle_kobold_heavy": "res://assets/audio/music/battle_kobold_heavy.ogg",
	"boss_battle": "res://assets/audio/music/boss_battle.ogg",
	"final_boss": "res://assets/audio/music/final_boss.ogg",
	"town": "res://assets/audio/music/town.ogg",
	"desert": "res://assets/audio/music/desert.ogg",
	"dungeon": "res://assets/audio/music/dungeon.ogg",
	"catacomb": "res://assets/audio/music/catacomb.ogg",
	"sad_theme": "res://assets/audio/music/sad_theme.ogg",
	"victory": "res://assets/audio/music/victory.ogg",
	"game_over": "res://assets/audio/music/game_over.ogg",
	"ending_good": "res://assets/audio/music/ending_good.ogg",
	"ending_best": "res://assets/audio/music/ending_best.ogg",
	"new_game_plus": "res://assets/audio/music/new_game_plus.ogg",
}

const SFX_FILES := {
	"menu_select": "res://assets/audio/sfx/menu_select.wav",
	"menu_confirm": "res://assets/audio/sfx/menu_confirm.wav",
	"menu_cancel": "res://assets/audio/sfx/menu_cancel.wav",
	"battle_hit_physical": "res://assets/audio/sfx/battle_hit_physical.wav",
	"battle_hit_magical": "res://assets/audio/sfx/battle_hit_magical.wav",
	"battle_miss": "res://assets/audio/sfx/battle_miss.wav",
	"spell_fire": "res://assets/audio/sfx/spell_fire.wav",
	"spell_water": "res://assets/audio/sfx/spell_ice.wav",
	"spell_ice": "res://assets/audio/sfx/spell_ice.wav",
	"spell_thunder": "res://assets/audio/sfx/spell_thunder.wav",
	"spell_heal": "res://assets/audio/sfx/spell_heal.wav",
	"spell_psychic": "res://assets/audio/sfx/spell_psychic.wav",
	"spell_none": "res://assets/audio/sfx/battle_hit_magical.wav",
	"spell_earth": "res://assets/audio/sfx/battle_hit_physical.wav",
	"spell_darkness": "res://assets/audio/sfx/spell_psychic.wav",
	"spell_light": "res://assets/audio/sfx/spell_heal.wav",
	"status_burn_tick": "res://assets/audio/sfx/status_burn_tick.wav",
	"bubble_pop": "res://assets/audio/sfx/bubble_pop.wav",
	"level_up": "res://assets/audio/sfx/level_up.wav",
	"key_item_get": "res://assets/audio/sfx/key_item_get.wav",
	"treasure_chest": "res://assets/audio/sfx/treasure_chest.wav",
	"save_point": "res://assets/audio/sfx/save_point.wav",
	"door_open": "res://assets/audio/sfx/door_open.wav",
	"character_join": "res://assets/audio/sfx/character_join.wav",
	"flood_death_impact": "res://assets/audio/sfx/flood_death_impact.wav",
	"hannah_scream": "res://assets/audio/sfx/hannah_scream.wav",
	"iris_berserk_roar": "res://assets/audio/sfx/iris_berserk_roar.wav",
	"skeleton_summon": "res://assets/audio/sfx/skeleton_summon.wav",
	"panda_transform": "res://assets/audio/sfx/panda_transform.wav",
	"hannah_ultimate_spell": "res://assets/audio/sfx/hannah_ultimate_spell.wav",
}

func _ready() -> void:
	_setup_audio_players()

func _setup_audio_players() -> void:
	if not has_node("MusicPlayer"):
		var player := AudioStreamPlayer.new()
		player.name = "MusicPlayer"
		player.bus = "Music"
		add_child(player)
	if not has_node("SFXPlayer"):
		var player := AudioStreamPlayer.new()
		player.name = "SFXPlayer"
		player.bus = "SFX"
		add_child(player)
	if not has_node("SFXPlayer2"):
		var player := AudioStreamPlayer.new()
		player.name = "SFXPlayer2"
		player.bus = "SFX"
		add_child(player)

func play_music(track_name: String, fade_time: float = 1.0) -> void:
	if track_name == current_music_track:
		return

	var path := MUSIC_TRACKS.get(track_name, "")
	if path == "":
		return

	var stream := load(path) if ResourceLoader.exists(path) else null

	if fade_time > 0 and get_node_or_null("MusicPlayer") != null:
		_fade_to_track(stream, fade_time)
	else:
		_play_track_direct(stream)

	current_music_track = track_name

func _fade_to_track(new_stream: AudioStream, fade_time: float) -> void:
	if fade_tween:
		fade_tween.kill()
	fade_tween = create_tween()
	var player := get_node("MusicPlayer")

	fade_tween.tween_property(player, "volume_db", -80.0, fade_time / 2.0)
	fade_tween.tween_callback(func():
		if new_stream:
			player.stream = new_stream
			player.play()
		else:
			player.stop()
	)
	if new_stream:
		fade_tween.tween_property(player, "volume_db", music_volume_db, fade_time / 2.0)

func _play_track_direct(stream: AudioStream) -> void:
	var player := get_node_or_null("MusicPlayer")
	if player == null:
		return
	if stream:
		player.stream = stream
		player.volume_db = music_volume_db
		player.play()
	else:
		player.stop()

func stop_music(fade_time: float = 1.0) -> void:
	if fade_time > 0:
		_fade_to_track(null, fade_time)
	else:
		get_node("MusicPlayer").stop()
	current_music_track = ""

func play_sfx(sfx_name: String) -> void:
	var path := SFX_FILES.get(sfx_name, "")
	if path == "" or not ResourceLoader.exists(path):
		return

	var stream := load(path)

	# Use whichever SFX player is free
	var player := get_node("SFXPlayer")
	var player2 := get_node("SFXPlayer2")
	var target_player := player if not player.playing else player2
	target_player.stream = stream
	target_player.volume_db = sfx_volume_db
	target_player.play()

func play_hannah_scream() -> void:
	# FF6-style scream: pitch shift + distortion + echo
	var path := SFX_FILES.get("hannah_scream", "")
	if not ResourceLoader.exists(path):
		return
	var player := get_node("SFXPlayer")
	player.stream = load(path)

	# Apply pitch shift effect for screaming quality
	var audio_effect := AudioEffectPitchShift.new()
	audio_effect.pitch_scale = 1.8
	AudioServer.add_bus_effect(AudioServer.get_bus_index("SFX"), audio_effect)

	player.play()
	# Remove effect after playback
	await get_tree().create_timer(3.0).timeout
	AudioServer.remove_bus_effect(AudioServer.get_bus_index("SFX"), 0)

func set_music_volume(volume_normalized: float) -> void:
	music_volume_db = linear_to_db(clamp(volume_normalized, 0.001, 1.0))
	if get_node_or_null("MusicPlayer"):
		get_node("MusicPlayer").volume_db = music_volume_db

func set_sfx_volume(volume_normalized: float) -> void:
	sfx_volume_db = linear_to_db(clamp(volume_normalized, 0.001, 1.0))
