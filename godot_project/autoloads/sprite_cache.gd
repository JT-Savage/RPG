## sprite_cache.gd
## Autoload singleton that caches SpriteFrames resources so they are not
## regenerated every time a character or NPC is spawned.
## Access via: SpriteCache.get_character_frames("kella")
extends Node
class_name SpriteCache

var _character_cache: Dictionary = {}
var _enemy_cache: Dictionary = {}


## Returns a cached (or freshly generated) SpriteFrames for the given character.
## char_id: matches the PNG filename under res://assets/sprites/characters/
func get_character_frames(char_id: String) -> SpriteFrames:
	if char_id in _character_cache:
		return _character_cache[char_id]
	var frames: SpriteFrames = SpriteFramesGenerator.create_character_frames(char_id)
	_character_cache[char_id] = frames
	return frames


## Returns a cached (or freshly generated) SpriteFrames for the given enemy.
## enemy_id: matches the PNG filename under res://assets/sprites/enemies/
## size: sprite dimension in pixels (16 = small, 32 = medium, 64 = boss)
func get_enemy_frames(enemy_id: String, size: int = 16) -> SpriteFrames:
	var key: String = "%s_%d" % [enemy_id, size]
	if key in _enemy_cache:
		return _enemy_cache[key]
	var frames: SpriteFrames = SpriteFramesGenerator.create_enemy_frames(enemy_id, size)
	_enemy_cache[key] = frames
	return frames


## Drops all cached SpriteFrames. Call between scenes if memory is a concern.
func clear_cache() -> void:
	_character_cache.clear()
	_enemy_cache.clear()
