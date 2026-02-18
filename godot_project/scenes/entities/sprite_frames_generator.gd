## sprite_frames_generator.gd
## Static utility that creates SpriteFrames resources at runtime from PNG spritesheets.
## No scene instance needed; all methods are static.
class_name SpriteFramesGenerator


## Creates a SpriteFrames resource for a character from their spritesheet.
## char_id: e.g. "kella", "michael", "hannah"
## Character sheets are at res://assets/sprites/characters/{char_id}.png
## Each sheet is 64x96 pixels: 4 columns (walk frames 0-3) x 4 rows (down, left, right, up).
## Returns SpriteFrames with animations: walk_down, walk_left, walk_right, walk_up
## Each animation: 4 frames, 8fps, looping
static func create_character_frames(char_id: String) -> SpriteFrames:
	var texture_path: String = "res://assets/sprites/characters/%s.png" % char_id
	if not ResourceLoader.exists(texture_path):
		push_warning("SpriteFramesGenerator: No texture at %s" % texture_path)
		return _create_fallback_frames()

	var sheet: Texture2D = load(texture_path)
	var frames := SpriteFrames.new()

	var FRAME_W: int = 16
	var FRAME_H: int = 24
	var DIRS: Array = ["walk_down", "walk_left", "walk_right", "walk_up"]

	frames.remove_animation("default")

	for row in range(4):
		var anim_name: String = DIRS[row]
		frames.add_animation(anim_name)
		frames.set_animation_speed(anim_name, 8.0)
		frames.set_animation_loop(anim_name, true)
		for col in range(4):
			var atlas := AtlasTexture.new()
			atlas.atlas = sheet
			atlas.region = Rect2(col * FRAME_W, row * FRAME_H, FRAME_W, FRAME_H)
			atlas.filter_clip = true
			frames.add_frame(anim_name, atlas)

	return frames


## Creates a SpriteFrames for enemies from their enemy sprite PNG.
## Enemy sprites are either 16x16 (small), 32x32 (medium), or 64x64 (boss).
## Enemy sheets have 2 columns (idle frame 0, attack frame 1) x 1 row.
## enemy_id: e.g. "kobold_grunt", "slime_boss"
## size: sprite dimension in pixels (16, 32, or 64)
static func create_enemy_frames(enemy_id: String, size: int = 16) -> SpriteFrames:
	var texture_path: String = "res://assets/sprites/enemies/%s.png" % enemy_id
	if not ResourceLoader.exists(texture_path):
		push_warning("SpriteFramesGenerator: No enemy texture at %s" % texture_path)
		return _create_fallback_frames()

	var sheet: Texture2D = load(texture_path)
	var frames := SpriteFrames.new()

	frames.remove_animation("default")

	# idle animation: column 0
	frames.add_animation("idle")
	frames.set_animation_speed("idle", 4.0)
	frames.set_animation_loop("idle", true)
	var idle_atlas := AtlasTexture.new()
	idle_atlas.atlas = sheet
	idle_atlas.region = Rect2(0, 0, size, size)
	idle_atlas.filter_clip = true
	frames.add_frame("idle", idle_atlas)

	# attack animation: column 1
	frames.add_animation("attack")
	frames.set_animation_speed("attack", 8.0)
	frames.set_animation_loop("attack", false)
	var attack_atlas := AtlasTexture.new()
	attack_atlas.atlas = sheet
	attack_atlas.region = Rect2(size, 0, size, size)
	attack_atlas.filter_clip = true
	frames.add_frame("attack", attack_atlas)

	# hurt animation: reuse idle frame (single frame, brief pause)
	frames.add_animation("hurt")
	frames.set_animation_speed("hurt", 8.0)
	frames.set_animation_loop("hurt", false)
	var hurt_atlas := AtlasTexture.new()
	hurt_atlas.atlas = sheet
	hurt_atlas.region = Rect2(0, 0, size, size)
	hurt_atlas.filter_clip = true
	frames.add_frame("hurt", hurt_atlas)

	# death animation: attack frame held (played once)
	frames.add_animation("death")
	frames.set_animation_speed("death", 4.0)
	frames.set_animation_loop("death", false)
	var death_atlas := AtlasTexture.new()
	death_atlas.atlas = sheet
	death_atlas.region = Rect2(size, 0, size, size)
	death_atlas.filter_clip = true
	frames.add_frame("death", death_atlas)

	return frames


## Fallback: generates a SpriteFrames with a solid magenta 16x16 placeholder.
## Used when a spritesheet cannot be found so the game doesn't crash.
static func _create_fallback_frames() -> SpriteFrames:
	var frames := SpriteFrames.new()

	# Build a tiny magenta Image as a placeholder texture
	var img := Image.create(16, 16, false, Image.FORMAT_RGBA8)
	img.fill(Color(1.0, 0.0, 1.0, 1.0))
	var tex := ImageTexture.create_from_image(img)

	var anim_names: Array = ["walk_down", "walk_left", "walk_right", "walk_up",
							 "idle", "attack", "hurt", "death"]

	frames.remove_animation("default")

	for anim_name in anim_names:
		frames.add_animation(anim_name)
		frames.set_animation_speed(anim_name, 4.0)
		frames.set_animation_loop(anim_name, anim_name in ["walk_down", "walk_left",
														   "walk_right", "walk_up", "idle"])
		var atlas := AtlasTexture.new()
		atlas.atlas = tex
		atlas.region = Rect2(0, 0, 16, 16)
		atlas.filter_clip = true
		frames.add_frame(anim_name, atlas)

	return frames
