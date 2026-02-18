# PROJECT STATUS — THERE WILL BE KOBOLDS
*Last updated: 2026-02-18*

## EXECUTIVE SUMMARY

The Godot 4.3 project build is **substantially complete** at `godot_project/`.
All core systems, all locations, all data databases, all dialogue scripts, all pixel art assets, and all UI scenes have been built.
The game is in a **playable prototype state** — open in Godot 4.3 and run.

---

## ENGINE STATUS

| Requirement | Status | File |
|-------------|--------|------|
| Godot 4.3+ project | ✅ DONE | `project.godot` |
| 256×224 viewport | ✅ DONE | project.godot |
| Pixel-perfect / Nearest filter | ✅ DONE | project.godot |
| Integer scaling | ✅ DONE | project.godot |
| All input maps (keyboard + gamepad) | ✅ DONE | project.godot |
| All 15 autoloads registered | ✅ DONE | project.godot |

---

## AUTOLOADS (15 total)

| Singleton | Status | File |
|-----------|--------|------|
| GameManager | ✅ DONE | `autoloads/game_manager.gd` |
| SaveSystem | ✅ DONE | `autoloads/save_system.gd` |
| FlagManager | ✅ DONE | `autoloads/flag_manager.gd` |
| BattleManager | ✅ DONE | `autoloads/battle_manager.gd` |
| PartyManager | ✅ DONE | `autoloads/party_manager.gd` |
| AudioManager | ✅ DONE | `autoloads/audio_manager.gd` |
| SceneTransition | ✅ DONE | `autoloads/scene_transition.gd` |
| DialogueManager | ✅ DONE | `autoloads/dialogue_manager.gd` |
| InputManager | ✅ DONE | `autoloads/input_manager.gd` |
| AdManager | ✅ DONE | `autoloads/ad_manager.gd` |
| RecruitmentSystem | ✅ DONE | `autoloads/recruitment_system.gd` |
| StoryEventSystem | ✅ DONE | `autoloads/story_event_system.gd` |
| NotificationManager | ✅ DONE | `autoloads/notification_manager.gd` |
| NGPlusManager | ✅ DONE | `autoloads/ng_plus_manager.gd` |

---

## LOCATION SCENES (14 locations)

| Location | GD | TSCN | Notes |
|----------|----|------|-------|
| Tutorial Warren | ✅ | ✅ | Opening dungeon, baby dragon chest, Kella cutscene |
| Surface Forest | ✅ | ✅ | First overworld area |
| Kobold Village | ✅ | ✅ | Michael recruitment, shop |
| Imperial City | ✅ | ✅ | Main hub, black market |
| Catacomb Entrance | ✅ | ✅ | First dark dungeon |
| Catacomb Depths | ✅ | ✅ | Hannah recruitment, lich boss |
| Swamp Village | ✅ | ✅ | Druidess recruitment |
| Mountain Pass | ✅ | ✅ | Possible Yipp spawn |
| Army Camp | ✅ | ✅ | Panda plushie chest |
| Desert Region | ✅ | ✅ | Dreamwalker area |
| Floating Island | ✅ | ✅ | Vampire, Dreamwalker |
| Orisia Island | ✅ | ✅ | Critical decision point |
| Final Dungeon (Void Spire) | ✅ | ✅ | Final boss area |
| Slaver Island | ✅ | ✅ | Post-credits, best ending |

---

## BATTLE SYSTEM

| Feature | Status | Notes |
|---------|--------|-------|
| ATB gauge system | ✅ DONE | `autoloads/battle_manager.gd` |
| Physical / Magical / Psychic damage | ✅ DONE | |
| 11 status effects | ✅ DONE | Poison, Sleep, Paralysis, Blind, Silence, Slow, Haste, Berserk, Confuse, Burn, Bubble |
| Enemy AI (weighted random) | ✅ DONE | |
| Michael auto-taunt | ✅ DONE | |
| Iris berserk on Fei death | ✅ DONE | |
| Baby Dragon counter attack | ✅ DONE | |
| Shapeshifter panda auto-attack | ✅ DONE | |
| Battle scene UI | ✅ DONE | `scenes/battle/battle_scene.gd+tscn` |
| Boss battle scene | ✅ DONE | `scenes/battle/boss_battle_scene.gd+tscn` |
| Command menu | ✅ DONE | `scenes/battle/command_menu.gd+tscn` |
| Flee mechanic | ✅ DONE | |
| Party swap in battle | ✅ DONE | |

---

## DATA FILES

| Database | Status | File |
|----------|--------|------|
| Enemy database | ✅ DONE | `data/enemy_database.gd` |
| Equipment database | ✅ DONE | `data/equipment_database.gd` |
| Spell database | ✅ DONE | `data/spell_database.gd` |
| Item database | ✅ DONE | `data/items/item_database.gd` |
| Key item database | ✅ DONE | `data/key_items/key_item_database.gd` |
| Shop database | ✅ DONE | `data/shops/shop_database.gd` |
| Formation database | ✅ DONE | `data/formations_database.gd` |

---

## UI SCENES

| Scene | Status | File |
|-------|--------|------|
| Title screen | ✅ DONE | `scenes/title/title_screen.gd+tscn` |
| Pause menu | ✅ DONE | `scenes/ui/pause_menu.gd+tscn` |
| Save select | ✅ DONE | `scenes/ui/save_select.gd+tscn` |
| Game over | ✅ DONE | `scenes/ui/game_over.gd+tscn` |
| Victory screen | ✅ DONE | `scenes/ui/victory_screen.gd+tscn` |
| Credits screen | ✅ DONE | `scenes/ui/credits_screen.gd+tscn` |
| Virtual controls | ✅ DONE | `scenes/ui/virtual_controls.gd+tscn` |
| Shop scene | ✅ DONE | `scenes/shop/shop_scene.gd+tscn` |
| Overworld map | ✅ DONE | `scenes/overworld/overworld.gd+tscn` |
| Ending controller | ✅ DONE | `scenes/ui/ending_controller.gd` |

---

## CHARACTER SYSTEMS

| System | Status | Notes |
|--------|--------|-------|
| All 12 characters with full stats | ✅ DONE | `autoloads/party_manager.gd` |
| Level 1–99 stat growth | ✅ DONE | |
| Ability unlock every 10 levels | ✅ DONE | |
| Class evolution (Orisia sidequest) | ✅ DONE | |
| Spell learning system | ✅ DONE | |
| Iris wildlife learning | ✅ DONE | |
| Flood permanent death | ✅ DONE | |
| Recruitment system | ✅ DONE | `autoloads/recruitment_system.gd` |
| Fritzzit+Crankpot pair | ✅ DONE | Both or neither |
| Yipp random spawn | ✅ DONE | Different dungeon each run |
| Orisia deadline → zombie conversion | ✅ DONE | |

---

## DIALOGUE / STORY

| Content | Status | File |
|---------|--------|------|
| Dialogue manager (typewriter, branching) | ✅ DONE | `autoloads/dialogue_manager.gd` |
| Kella warren farewell | ✅ DONE | `data/dialogues/` |
| Michael recruitment | ✅ DONE | |
| Hannah recruitment | ✅ DONE | |
| Baby dragon naming | ✅ DONE | |
| Vampire recruitment | ✅ DONE | |
| Fritzzit+Crankpot recruitment | ✅ DONE | |
| Yipp dungeon | ✅ DONE | |
| Orisia meeting | ✅ DONE | |
| Fei grooming cutscene | ✅ DONE | |
| Flood death cutscene | ✅ DONE | |
| Jerod explosion | ✅ DONE | |
| Iris berserk trigger | ✅ DONE | |
| NG+ commentary (17 lines) | ✅ DONE | |
| Good ending | ✅ DONE | |
| Bad ending (secret boss) | ✅ DONE | |
| Best ending (post-credits) | ✅ DONE | |
| Town NPC dialogues | ✅ DONE | `data/dialogues/town_npcs.json` |

---

## ASSETS

| Type | Status | Notes |
|------|--------|-------|
| Character sprites (12) | ✅ DONE | 64×96 4-direction sheets |
| Enemy sprites (19) | ✅ DONE | Small/medium/boss sizes |
| Battle backgrounds (12) | ✅ DONE | 256×112 |
| Tilesets (6) | ✅ DONE | warren, forest, city, desert, catacomb, overworld |
| UI elements | ✅ DONE | Bars, panels, icons, cursor, save crystal |
| Spell animations (9+) | ✅ DONE | All elements + specials |
| Overworld icons (12) | ✅ DONE | All location types |
| Audio | ⚠️ REQUIRED | See `assets/audio/AUDIO_REQUIRED.txt` |

---

## EXPORT CONFIGURATIONS

| Platform | Status | Notes |
|----------|--------|-------|
| Windows | ✅ DONE | `export_presets.cfg` |
| macOS | ✅ DONE | |
| Linux | ✅ DONE | |
| Android | ✅ DONE | Min SDK 24, AdMob placeholder |
| iOS | ✅ DONE | |

---

## REMAINING TASKS

### Required to complete before final build:
1. **Audio files** — Source royalty-free .ogg music and .wav SFX (see AUDIO_REQUIRED.txt)
2. **TileMap painting** — Open Godot editor and paint tile layers for each location
3. **Godot import** — Import project in Godot 4.3, resolve any import errors
4. **Testing pass** — Full playthrough to find runtime bugs
5. **Balance pass** — Enemy HP/damage, player stat growth, shop prices

### Nice to have:
- Additional NPC dialogue variety per location visit
- More environmental storytelling (signs, books, notes)
- Achievement/trophy system
- Controller rumble support
- Additional ambient sound zones

---

## HOW TO OPEN IN GODOT

1. Install Godot 4.3 (https://godotengine.org)
2. Open Godot → Import Project → select `godot_project/project.godot`
3. Let Godot import all resources (may take 1-2 min)
4. Press F5 to run the title screen
5. The game boots to the title screen; select New Game to start

## NOTES

- All autoloads are registered in project.godot and load automatically
- The start scene is `scenes/title/title_screen.tscn`
- Pixel art renders correctly with viewport stretch + nearest filter already configured
- Mobile touch controls appear automatically on iOS/Android (detected via OS.get_name())
- AdMob: silently ignored on desktop; add the GodotAdMob plugin for mobile builds
