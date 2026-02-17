## enemy_database.gd
## Static enemy data for "There Will Be Kobolds"
## Contains all enemy stats, actions, and encounter formations.
class_name EnemyDatabase


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

## Returns a Dictionary with full stats for the given enemy id.
## Returns an empty Dictionary if the id is not found.
static func get_enemy(id: String) -> Dictionary:
	var db := _build_enemy_db()
	if db.has(id):
		return db[id]
	push_warning("EnemyDatabase: unknown enemy id '%s'" % id)
	return {}


## Returns an Array of enemy id Strings that make up the named formation.
## Returns an empty Array if the formation_id is not found.
static func get_formation(formation_id: String) -> Array:
	var db := _build_formation_db()
	if db.has(formation_id):
		return db[formation_id]
	push_warning("EnemyDatabase: unknown formation id '%s'" % formation_id)
	return []


# ---------------------------------------------------------------------------
# Enemy database builder
# ---------------------------------------------------------------------------

static func _build_enemy_db() -> Dictionary:
	return {

		# ===================================================================
		# TUTORIAL / WARREN ENEMIES  (easy)
		# ===================================================================

		"infected_kobold": {
			"id": "infected_kobold",
			"name": "Infected Kobold",
			"region": "warren",
			"difficulty": "easy",
			"type": "normal",
			"hp": 45,
			"atk": 12,
			"def": 5,
			"speed": 14,
			"exp": 8,
			"gil": 3,
			"weaknesses": [],
			"immunities": [],
			"actions": [
				{"id": "attack",      "weight": 80, "tags": []},
				{"id": "infect_bite", "weight": 20, "tags": ["inflicts_poison"]},
			],
			"sprite_size": "16x16",
		},

		"kobold_warrior": {
			"id": "kobold_warrior",
			"name": "Kobold Warrior",
			"region": "warren",
			"difficulty": "easy",
			"type": "normal",
			"hp": 65,
			"atk": 16,
			"def": 8,
			"speed": 12,
			"exp": 12,
			"gil": 5,
			"weaknesses": [],
			"immunities": [],
			"actions": [
				{"id": "attack",      "weight": 70, "tags": []},
				{"id": "shield_bash", "weight": 30, "tags": []},
			],
			"sprite_size": "16x16",
		},

		"zombie_kobold": {
			"id": "zombie_kobold",
			"name": "Zombie Kobold",
			"region": "warren",
			"difficulty": "easy",
			"type": "undead",
			"hp": 55,
			"atk": 13,
			"def": 6,
			"speed": 8,
			"exp": 10,
			"gil": 4,
			"weaknesses": ["light"],
			"immunities": ["poison", "sleep"],
			"actions": [
				{"id": "attack", "weight": 100, "tags": []},
			],
			"sprite_size": "16x16",
		},

		# ===================================================================
		# SURFACE ENEMIES  (easy-medium)
		# ===================================================================

		"lycanthrope": {
			"id": "lycanthrope",
			"name": "Lycanthrope",
			"region": "surface",
			"difficulty": "easy_medium",
			"type": "wildlife",
			"hp": 120,
			"atk": 22,
			"def": 12,
			"speed": 16,
			"exp": 25,
			"gil": 15,
			"weaknesses": [],
			"immunities": [],
			"actions": [
				{"id": "claw",  "weight": 60, "tags": []},
				{"id": "howl",  "weight": 20, "tags": ["haste_self"]},
				{"id": "bite",  "weight": 20, "tags": []},
			],
			"sprite_size": "16x16",
		},

		"forest_wolf": {
			"id": "forest_wolf",
			"name": "Forest Wolf",
			"region": "surface",
			"difficulty": "easy_medium",
			"type": "wildlife",
			"hp": 80,
			"atk": 18,
			"def": 8,
			"speed": 18,
			"exp": 15,
			"gil": 8,
			"weaknesses": [],
			"immunities": [],
			"actions": [
				{"id": "attack", "weight": 70, "tags": []},
				{"id": "bite",   "weight": 30, "tags": []},
			],
			"sprite_size": "16x16",
		},

		# Only available before the jerod_house_explosion story flag is set.
		"fungal_deer": {
			"id": "fungal_deer",
			"name": "Fungal Deer",
			"region": "surface",
			"difficulty": "easy_medium",
			"type": "wildlife",
			"hp": 95,
			"atk": 20,
			"def": 10,
			"speed": 14,
			"exp": 20,
			"gil": 10,
			"weaknesses": [],
			"immunities": [],
			"spawn_condition": "before_flag:jerod_house_explosion",
			"actions": [
				{"id": "attack",  "weight": 60, "tags": []},
				{"id": "gore",    "weight": 40, "tags": []},
			],
			"sprite_size": "16x16",
		},

		# ===================================================================
		# IMPERIAL CITY ENEMIES  (medium)
		# ===================================================================

		"city_guard": {
			"id": "city_guard",
			"name": "City Guard",
			"region": "imperial_city",
			"difficulty": "medium",
			"type": "normal",
			"hp": 180,
			"atk": 28,
			"def": 20,
			"speed": 13,
			"exp": 35,
			"gil": 25,
			"weaknesses": [],
			"immunities": [],
			"actions": [
				{"id": "attack",      "weight": 70, "tags": []},
				{"id": "shield_bash", "weight": 30, "tags": []},
			],
			"sprite_size": "16x16",
		},

		# Appears in groups of 3-5 (see formations).
		"infected_kobold_swarm": {
			"id": "infected_kobold_swarm",
			"name": "Infected Kobold (Swarm)",
			"region": "imperial_city",
			"difficulty": "medium",
			"type": "normal",
			"hp": 40,
			"atk": 15,
			"def": 4,
			"speed": 16,
			"exp": 6,
			"gil": 2,
			"weaknesses": [],
			"immunities": [],
			"group_size_min": 3,
			"group_size_max": 5,
			"actions": [
				{"id": "attack",      "weight": 70, "tags": []},
				{"id": "infect_bite", "weight": 30, "tags": ["inflicts_poison"]},
			],
			"sprite_size": "16x16",
		},

		"cultist": {
			"id": "cultist",
			"name": "Cultist",
			"region": "imperial_city",
			"difficulty": "medium",
			"type": "normal",
			"hp": 150,
			"atk": 25,
			"def": 15,
			"speed": 15,
			"exp": 40,
			"gil": 30,
			"weaknesses": [],
			"immunities": [],
			"actions": [
				{"id": "attack",     "weight": 50, "tags": []},
				{"id": "dark_spell", "weight": 30, "tags": ["element:darkness", "power:35"]},
				{"id": "confuse",    "weight": 20, "tags": ["inflicts_confuse"]},
			],
			"sprite_size": "16x16",
		},

		# ===================================================================
		# UNDEAD LANDS ENEMIES  (medium)
		# ===================================================================

		"skeleton": {
			"id": "skeleton",
			"name": "Skeleton",
			"region": "undead_lands",
			"difficulty": "medium",
			"type": "undead",
			"hp": 130,
			"atk": 24,
			"def": 18,
			"speed": 10,
			"exp": 30,
			"gil": 20,
			"weaknesses": ["light", "earth"],
			"immunities": ["poison", "sleep"],
			"actions": [
				{"id": "attack", "weight": 70, "tags": []},
				{"id": "bone_throw", "weight": 30, "tags": []},
			],
			"sprite_size": "16x16",
		},

		"skeleton_warrior": {
			"id": "skeleton_warrior",
			"name": "Skeleton Warrior",
			"region": "undead_lands",
			"difficulty": "medium",
			"type": "undead",
			"hp": 170,
			"atk": 32,
			"def": 22,
			"speed": 9,
			"exp": 45,
			"gil": 35,
			"weaknesses": ["light", "earth"],
			"immunities": ["poison", "sleep"],
			"actions": [
				{"id": "attack",      "weight": 60, "tags": []},
				{"id": "shield_bash", "weight": 25, "tags": []},
				{"id": "bone_slam",   "weight": 15, "tags": []},
			],
			"sprite_size": "16x16",
		},

		"zombie_orc": {
			"id": "zombie_orc",
			"name": "Zombie Orc",
			"region": "undead_lands",
			"difficulty": "medium",
			"type": "undead",
			"hp": 200,
			"atk": 30,
			"def": 20,
			"speed": 8,
			"exp": 50,
			"gil": 40,
			"weaknesses": ["light"],
			"immunities": ["poison", "sleep"],
			"actions": [
				{"id": "attack",     "weight": 70, "tags": []},
				{"id": "heavy_slam", "weight": 30, "tags": []},
			],
			"sprite_size": "16x16",
		},

		# ===================================================================
		# DESERT ENEMIES  (hard - significant difficulty spike)
		# ===================================================================

		"desert_wraith": {
			"id": "desert_wraith",
			"name": "Desert Wraith",
			"region": "desert",
			"difficulty": "hard",
			"type": "undead",
			"hp": 380,
			"atk": 55,
			"def": 30,
			"speed": 20,
			"exp": 120,
			"gil": 80,
			"weaknesses": ["light"],
			"immunities": ["poison", "sleep"],
			"actions": [
				{"id": "attack", "weight": 40, "tags": []},
				{"id": "drain",  "weight": 30, "tags": ["drain_hp"]},
				{"id": "silence","weight": 30, "tags": ["inflicts_silence"]},
			],
			"sprite_size": "16x16",
		},

		"sand_scorpion": {
			"id": "sand_scorpion",
			"name": "Sand Scorpion",
			"region": "desert",
			"difficulty": "hard",
			"type": "wildlife",
			"hp": 420,
			"atk": 60,
			"def": 45,
			"speed": 18,
			"exp": 140,
			"gil": 100,
			"weaknesses": ["water"],
			"immunities": [],
			"actions": [
				{"id": "sting",  "weight": 60, "tags": ["inflicts_poison"]},
				{"id": "pincer", "weight": 40, "tags": []},
			],
			"sprite_size": "16x16",
		},

		"desert_cultist": {
			"id": "desert_cultist",
			"name": "Desert Cultist",
			"region": "desert",
			"difficulty": "hard",
			"type": "normal",
			"hp": 350,
			"atk": 50,
			"def": 28,
			"speed": 17,
			"exp": 130,
			"gil": 90,
			"weaknesses": [],
			"immunities": [],
			"actions": [
				{"id": "attack",   "weight": 30, "tags": []},
				{"id": "fire_lv3", "weight": 30, "tags": ["element:fire", "power:60"]},
				{"id": "quake",    "weight": 20, "tags": ["element:earth", "aoe"]},
				{"id": "poison",   "weight": 20, "tags": ["inflicts_poison", "aoe"]},
			],
			"sprite_size": "16x16",
		},

		"undead_knight": {
			"id": "undead_knight",
			"name": "Undead Knight",
			"region": "desert",
			"difficulty": "hard",
			"type": "undead",
			"hp": 500,
			"atk": 65,
			"def": 50,
			"speed": 12,
			"exp": 160,
			"gil": 120,
			"weaknesses": ["light"],
			"immunities": ["poison", "sleep"],
			"actions": [
				{"id": "attack",      "weight": 50, "tags": []},
				{"id": "dark_strike", "weight": 30, "tags": ["element:darkness"]},
				{"id": "shield_bash", "weight": 20, "tags": []},
			],
			"sprite_size": "16x16",
		},

		# ===================================================================
		# CATACOMB ENEMIES  (hard)
		# ===================================================================

		"catacomb_cultist": {
			"id": "catacomb_cultist",
			"name": "Catacomb Cultist",
			"region": "catacombs",
			"difficulty": "hard",
			"type": "normal",
			"hp": 450,
			"atk": 58,
			"def": 35,
			"speed": 16,
			"exp": 150,
			"gil": 110,
			"weaknesses": [],
			"immunities": [],
			"actions": [
				{"id": "attack",     "weight": 40, "tags": []},
				{"id": "dark_spell", "weight": 35, "tags": ["element:darkness", "power:50"]},
				{"id": "confuse",    "weight": 25, "tags": ["inflicts_confuse"]},
			],
			"sprite_size": "16x16",
		},

		"risen_warrior": {
			"id": "risen_warrior",
			"name": "Risen Warrior",
			"region": "catacombs",
			"difficulty": "hard",
			"type": "undead",
			"hp": 550,
			"atk": 70,
			"def": 45,
			"speed": 11,
			"exp": 180,
			"gil": 140,
			"weaknesses": ["light"],
			"immunities": ["poison", "sleep"],
			"actions": [
				{"id": "attack",      "weight": 60, "tags": []},
				{"id": "dark_strike", "weight": 25, "tags": ["element:darkness"]},
				{"id": "bone_slam",   "weight": 15, "tags": []},
			],
			"sprite_size": "16x16",
		},

		"vampire_bat": {
			"id": "vampire_bat",
			"name": "Vampire Bat",
			"region": "catacombs",
			"difficulty": "hard",
			"type": "undead",
			"hp": 300,
			"atk": 52,
			"def": 25,
			"speed": 22,
			"exp": 130,
			"gil": 90,
			"weaknesses": ["light"],
			"immunities": ["poison"],
			"actions": [
				{"id": "attack",    "weight": 50, "tags": []},
				{"id": "drain",     "weight": 30, "tags": ["drain_hp"]},
				{"id": "wing_gust", "weight": 20, "tags": []},
			],
			"sprite_size": "16x16",
		},

		# ===================================================================
		# BOSSES
		# ===================================================================

		"jerod_fungal_boss": {
			"id": "jerod_fungal_boss",
			"name": "Jerod (Fungal Abomination)",
			"region": "warren",
			"difficulty": "boss",
			"type": "normal",
			"is_boss": true,
			"hp": 2800,
			"atk": 45,
			"def": 25,
			"mag_pow": 38,
			"sp_res": 20,
			"speed": 10,
			"weaknesses": ["fire"],
			"immunities": ["poison"],
			"actions": [
				{
					"id": "fungal_spore",
					"weight": 30,
					"tags": ["aoe", "inflicts_poison"],
				},
				{
					"id": "slam",
					"weight": 35,
					"tags": ["single_target", "heavy"],
				},
				{
					"id": "spread_infection",
					"weight": 25,
					"tags": ["aoe", "inflicts_blind", "inflicts_poison"],
				},
				{
					"id": "enrage",
					"weight": 10,
					"tags": ["self_buff", "atk_up"],
					"condition": "hp_below_50_percent",
				},
			],
			"sprite_size": "32x32",
		},

		"black_dragon": {
			"id": "black_dragon",
			"name": "Black Dragon",
			"region": "imperial_city",
			"difficulty": "boss",
			"type": "dragon",
			"is_boss": true,
			"hp": 8500,
			"atk": 80,
			"def": 55,
			"mag_pow": 70,
			"sp_res": 40,
			"speed": 15,
			"weaknesses": [],
			"immunities": ["fire"],
			"absorbs": [],
			"actions": [
				{
					"id": "fire_breath",
					"weight": 35,
					"tags": ["aoe", "element:fire"],
				},
				{
					"id": "claw",
					"weight": 30,
					"tags": ["single_target", "heavy", "physical"],
				},
				{
					"id": "tail_sweep",
					"weight": 20,
					"tags": ["aoe", "physical"],
				},
				{
					"id": "roar",
					"weight": 15,
					"tags": ["aoe", "inflicts_slow"],
				},
			],
			"sprite_size": "64x64",
		},

		"undead_dragon": {
			"id": "undead_dragon",
			"name": "Undead Dragon",
			"region": "catacombs",
			"difficulty": "boss",
			"type": "undead",
			"is_boss": true,
			"hp": 10000,
			"atk": 85,
			"def": 60,
			"mag_pow": 80,
			"sp_res": 70,
			"speed": 14,
			"weaknesses": ["light"],
			"immunities": ["poison", "sleep", "fire", "ice", "thunder", "earth", "water", "wind", "darkness"],
			# +50% spell resistance vs all elements
			"spell_resistance_bonus": 50,
			"actions": [
				{
					"id": "dark_breath",
					"weight": 35,
					"tags": ["aoe", "element:darkness"],
				},
				{
					"id": "bone_crush",
					"weight": 30,
					"tags": ["single_target", "heavy", "physical"],
				},
				{
					"id": "death_gaze",
					"weight": 20,
					"tags": ["single_target", "inflicts_doom"],
				},
				{
					"id": "magic_absorb",
					"weight": 15,
					"tags": ["reactive", "absorb_next_spell"],
				},
			],
			"sprite_size": "64x64",
		},

		"necromancer_lich": {
			"id": "necromancer_lich",
			"name": "Necromancer Lich",
			"region": "catacombs",
			"difficulty": "boss",
			"type": "undead",
			"is_boss": true,
			"hp": 18000,
			"atk": 90,
			"def": 65,
			"mag_pow": 110,
			"sp_res": 80,
			"speed": 18,
			"weaknesses": ["light"],
			"immunities": ["poison", "sleep"],
			"phase_2_threshold": 0.5,
			"actions": [
				# Phase 1 and 2 actions
				{
					"id": "summon_undead",
					"weight": 20,
					"tags": ["summon", "adds_zombie_enemies"],
				},
				{
					"id": "dark_nova",
					"weight": 25,
					"tags": ["aoe", "element:darkness"],
				},
				{
					"id": "drain_life",
					"weight": 25,
					"tags": ["single_target", "heavy", "drain_hp"],
				},
				{
					"id": "time_stop",
					"weight": 15,
					"tags": ["aoe", "inflicts_stop", "duration:1_turn"],
				},
				# Phase 2 only actions
				{
					"id": "meteor",
					"weight": 30,
					"tags": ["aoe", "phase_2_only"],
				},
				{
					"id": "doom",
					"weight": 20,
					"tags": ["single_target", "instant_kill", "phase_2_only"],
				},
				{
					"id": "resurrection",
					"weight": 10,
					"tags": ["self_heal", "once_per_battle", "restore_3000_hp", "phase_2_only"],
				},
			],
			"sprite_size": "64x64",
		},

		# Bad ending boss
		"kella_double_infected": {
			"id": "kella_double_infected",
			"name": "Kella (Doubly Infected)",
			"region": "bad_ending",
			"difficulty": "boss",
			"type": "normal",
			"is_boss": true,
			"ending": "bad",
			"hp": 15000,
			"atk": 85,
			"def": 55,
			"mag_pow": 95,
			"sp_res": 0,
			"speed": 12,
			"weaknesses": ["light"],
			"immunities": [],
			"actions": [
				{
					"id": "plague_breath",
					"weight": 30,
					"tags": ["aoe", "inflicts_poison", "inflicts_blind"],
				},
				{
					"id": "fungal_surge",
					"weight": 30,
					"tags": ["aoe", "heavy"],
				},
				{
					"id": "infection_wave",
					"weight": 25,
					"tags": ["single_target", "inflicts_all_statuses"],
				},
				{
					"id": "heal_self",
					"weight": 15,
					"tags": ["self_heal", "restore_2000_hp"],
				},
			],
			"sprite_size": "64x64",
		},

		# Best ending boss
		"captain_donald": {
			"id": "captain_donald",
			"name": "Captain Donald",
			"region": "best_ending",
			"difficulty": "boss",
			"type": "normal",
			"is_boss": true,
			"ending": "best",
			"hp": 6000,
			"atk": 75,
			"def": 45,
			"sp_res": 0,
			"speed": 20,
			"weaknesses": [],
			"immunities": [],
			"actions": [
				{
					"id": "pistol_shot",
					"weight": 35,
					"tags": ["single_target", "ranged"],
				},
				{
					"id": "chain_whip",
					"weight": 25,
					"tags": ["aoe", "physical"],
				},
				{
					"id": "call_guards",
					"weight": 25,
					"tags": ["summon", "adds_slaver_guards", "count:2"],
				},
				{
					"id": "rally",
					"weight": 15,
					"tags": ["self_buff", "haste_self", "atk_up", "condition:hp_below_25_percent"],
				},
			],
			"sprite_size": "32x32",
		},

	}


# ---------------------------------------------------------------------------
# Formation database builder
# ---------------------------------------------------------------------------

static func _build_formation_db() -> Dictionary:
	return {

		# ===================================================================
		# WARREN / TUTORIAL FORMATIONS
		# ===================================================================

		"warren_single_infected": ["infected_kobold"],
		"warren_pair_infected":   ["infected_kobold", "infected_kobold"],
		"warren_trio_infected":   ["infected_kobold", "infected_kobold", "infected_kobold"],
		"warren_warrior_pair":    ["kobold_warrior", "infected_kobold"],
		"warren_warrior_group":   ["kobold_warrior", "kobold_warrior", "infected_kobold"],
		"warren_zombie_pair":     ["zombie_kobold", "zombie_kobold"],
		"warren_mixed":           ["kobold_warrior", "zombie_kobold", "infected_kobold"],

		# ===================================================================
		# SURFACE FORMATIONS
		# ===================================================================

		"surface_lone_wolf":      ["forest_wolf"],
		"surface_wolf_pack":      ["forest_wolf", "forest_wolf", "forest_wolf"],
		"surface_lycanthrope":    ["lycanthrope"],
		"surface_lycanthrope_wolves": ["lycanthrope", "forest_wolf", "forest_wolf"],
		"surface_fungal_deer":    ["fungal_deer"],
		"surface_deer_pair":      ["fungal_deer", "fungal_deer"],
		"surface_wolf_deer":      ["forest_wolf", "forest_wolf", "fungal_deer"],

		# ===================================================================
		# IMPERIAL CITY FORMATIONS
		# ===================================================================

		"city_guard_pair":        ["city_guard", "city_guard"],
		"city_guard_trio":        ["city_guard", "city_guard", "city_guard"],
		"city_cultist":           ["cultist"],
		"city_cultist_guards":    ["cultist", "city_guard", "city_guard"],
		"city_swarm_small":       [
			"infected_kobold_swarm",
			"infected_kobold_swarm",
			"infected_kobold_swarm",
		],
		"city_swarm_large":       [
			"infected_kobold_swarm",
			"infected_kobold_swarm",
			"infected_kobold_swarm",
			"infected_kobold_swarm",
			"infected_kobold_swarm",
		],
		"city_mixed_threat":      ["cultist", "city_guard", "infected_kobold_swarm", "infected_kobold_swarm"],

		# ===================================================================
		# UNDEAD LANDS FORMATIONS
		# ===================================================================

		"undead_skeleton_pair":   ["skeleton", "skeleton"],
		"undead_skeleton_trio":   ["skeleton", "skeleton", "skeleton"],
		"undead_warrior":         ["skeleton_warrior"],
		"undead_warrior_escort":  ["skeleton_warrior", "skeleton", "skeleton"],
		"undead_zombie_orc":      ["zombie_orc"],
		"undead_zombie_pair":     ["zombie_orc", "zombie_orc"],
		"undead_mixed":           ["skeleton_warrior", "skeleton", "zombie_orc"],

		# ===================================================================
		# DESERT FORMATIONS
		# ===================================================================

		"desert_wraith":          ["desert_wraith"],
		"desert_wraith_pair":     ["desert_wraith", "desert_wraith"],
		"desert_scorpion":        ["sand_scorpion"],
		"desert_scorpion_pack":   ["sand_scorpion", "sand_scorpion"],
		"desert_cultist":         ["desert_cultist"],
		"desert_cultist_pair":    ["desert_cultist", "desert_cultist"],
		"desert_undead_knight":   ["undead_knight"],
		"desert_knight_wraith":   ["undead_knight", "desert_wraith"],
		"desert_knight_cultist":  ["undead_knight", "desert_cultist"],
		"desert_mixed_hard":      ["undead_knight", "desert_cultist", "desert_wraith"],

		# ===================================================================
		# CATACOMB FORMATIONS
		# ===================================================================

		"catacombs_cultist":          ["catacomb_cultist"],
		"catacombs_cultist_pair":     ["catacomb_cultist", "catacomb_cultist"],
		"catacombs_risen_warrior":    ["risen_warrior"],
		"catacombs_risen_pair":       ["risen_warrior", "risen_warrior"],
		"catacombs_bat_swarm":        ["vampire_bat", "vampire_bat", "vampire_bat"],
		"catacombs_warrior_cultist":  ["risen_warrior", "catacomb_cultist"],
		"catacombs_mixed":            ["risen_warrior", "catacomb_cultist", "vampire_bat", "vampire_bat"],

		# ===================================================================
		# BOSS FORMATIONS  (single-entry for encounter system)
		# ===================================================================

		"boss_jerod_fungal":          ["jerod_fungal_boss"],
		"boss_black_dragon":          ["black_dragon"],
		"boss_undead_dragon":         ["undead_dragon"],
		"boss_necromancer_lich":      ["necromancer_lich"],
		"boss_kella_bad_ending":      ["kella_double_infected"],
		"boss_captain_donald":        ["captain_donald"],

	}
