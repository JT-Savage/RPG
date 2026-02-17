extends Node
## PartyManager - Manages all 12 characters, their stats, levels, equipment

const MAX_LEVEL_BASE := 75
const MAX_LEVEL_EVOLVED := 99

# All character states - populated on new_game / load
# Structure: char_id -> CharacterState dict
var character_states: Dictionary = {}

signal character_leveled_up(char_id: String, new_level: int)
signal character_evolved(char_id: String, new_class: String)

# ===== CHARACTER DATA DEFINITIONS =====
# Base stats at level 1, growth per level
const CHARACTER_DATA := {
	"javin": {
		"name": "Javin",
		"starting_class": "claw_noble",
		"evolved_class": "dreamwalker",
		"key_item_required": "ki_baby_dragon",
		"level_cap_base": 75,
		"level_cap_evolved": 99,
		"base_stats": {"hp": 280, "mp": 60, "attack": 22, "defense": 18, "magic_power": 12, "spell_resistance": 15, "speed": 20},
		"growth": {"hp": 14, "mp": 2, "attack": 1.2, "defense": 1.0, "magic_power": 0.5, "spell_resistance": 0.8, "speed": 0.8},
		"weapon_types": ["dagger", "short_sword"],
		"armor_types": ["light_armor", "accessory"],
		"can_use_shield": false,
		"starting_spells": ["fire_lv1"],
		"can_learn_spells": false,
		"attack_counter_max": 4,   # Baby Dragon fires at counter 4
		"portrait": "javin",
	},
	"frostbite": {
		"name": "Frostbite",
		"starting_class": "gunner",
		"evolved_class": "gunner",  # No class change, weapon upgrade only
		"key_item_required": "ki_shotgun_blueprint",
		"level_cap_base": 75,
		"level_cap_evolved": 99,
		"base_stats": {"hp": 260, "mp": 0, "attack": 28, "defense": 16, "magic_power": 0, "spell_resistance": 12, "speed": 18},
		"growth": {"hp": 12, "mp": 0, "attack": 1.5, "defense": 0.9, "magic_power": 0, "spell_resistance": 0.6, "speed": 0.9},
		"weapon_types": ["shotgun", "grenade"],
		"armor_types": ["light_armor", "medium_armor", "accessory"],
		"can_use_shield": false,
		"starting_spells": [],
		"can_learn_spells": false,
		"portrait": "frostbite",
	},
	"fei": {
		"name": "Fei",
		"starting_class": "warrior",
		"evolved_class": "weapon_master",
		"key_item_required": "ki_grizzly_skull",
		"level_cap_base": 75,
		"level_cap_evolved": 99,
		"base_stats": {"hp": 340, "mp": 20, "attack": 30, "defense": 22, "magic_power": 5, "spell_resistance": 10, "speed": 15},
		"growth": {"hp": 18, "mp": 0.5, "attack": 1.6, "defense": 1.2, "magic_power": 0, "spell_resistance": 0.5, "speed": 0.7},
		"weapon_types": ["sword", "axe", "spear"],
		"armor_types": ["medium_armor", "heavy_armor", "accessory", "shield"],
		"can_use_shield": true,
		"starting_spells": [],
		"can_learn_spells": false,
		"portrait": "fei",
	},
	"flood": {
		"name": "Flood",
		"starting_class": "ice_mage",
		"evolved_class": "ice_mage",  # Already max class
		"key_item_required": "",
		"level_cap_base": 99,
		"level_cap_evolved": 99,
		"base_stats": {"hp": 200, "mp": 120, "attack": 10, "defense": 8, "magic_power": 38, "spell_resistance": 25, "speed": 16},
		"growth": {"hp": 8, "mp": 6, "attack": 0.4, "defense": 0.4, "magic_power": 2.0, "spell_resistance": 1.2, "speed": 0.7},
		"weapon_types": ["staff", "rod"],
		"armor_types": ["light_armor", "robe", "accessory"],
		"can_use_shield": false,
		"starting_spells": ["blizzard_lv1", "blizzara_lv2"],
		"can_learn_spells": true,
		"can_double_cast": true,
		"portrait": "flood",
	},
	"hannah": {
		"name": "Hannah",
		"starting_class": "witch",
		"evolved_class": "magus",
		"key_item_required": "",
		"level_cap_base": 75,
		"level_cap_evolved": 99,
		"base_stats": {"hp": 210, "mp": 110, "attack": 12, "defense": 10, "magic_power": 35, "spell_resistance": 22, "speed": 17},
		"growth": {"hp": 9, "mp": 5, "attack": 0.5, "defense": 0.5, "magic_power": 1.9, "spell_resistance": 1.1, "speed": 0.8},
		"weapon_types": ["staff", "wand"],
		"armor_types": ["light_armor", "robe", "accessory"],
		"can_use_shield": false,
		"starting_spells": ["fire_lv1", "thunder_lv1"],
		"can_learn_spells": true,
		"can_double_cast": true,
		"portrait": "hannah",
	},
	"michael": {
		"name": "Michael",
		"starting_class": "cleric",
		"evolved_class": "paladin",
		"key_item_required": "ki_sentimental_pouch",
		"level_cap_base": 75,
		"level_cap_evolved": 99,
		"base_stats": {"hp": 300, "mp": 80, "attack": 20, "defense": 25, "magic_power": 20, "spell_resistance": 20, "speed": 13},
		"growth": {"hp": 16, "mp": 4, "attack": 1.0, "defense": 1.4, "magic_power": 1.0, "spell_resistance": 1.0, "speed": 0.6},
		"weapon_types": ["mace", "staff", "sword"],
		"armor_types": ["light_armor", "medium_armor", "heavy_armor", "plate_armor", "accessory", "shield"],
		"can_use_shield": true,
		"starting_spells": ["cure_lv1", "holy_lv1"],
		"can_learn_spells": true,
		"auto_taunt_when_paladin": true,
		"portrait": "michael",
	},
	"warghoul": {
		"name": "Warghoul",
		"starting_class": "undead_warrior",
		"evolved_class": "deathknight",
		"key_item_required": "ki_orc_funeral_totem",
		"level_cap_base": 75,
		"level_cap_evolved": 99,
		"base_stats": {"hp": 360, "mp": 40, "attack": 32, "defense": 20, "magic_power": 8, "spell_resistance": 8, "speed": 12},
		"growth": {"hp": 20, "mp": 2, "attack": 1.7, "defense": 1.1, "magic_power": 0.4, "spell_resistance": 0.4, "speed": 0.5},
		"weapon_types": ["sword", "axe", "mace"],
		"armor_types": ["medium_armor", "heavy_armor", "accessory"],
		"can_use_shield": false,
		"starting_spells": ["drain_lv1"],
		"can_learn_spells": true,
		"portrait": "warghoul",
	},
	"cookie": {
		"name": "Cookie",
		"starting_class": "druid",
		"evolved_class": "druidess",
		"key_item_required": "ki_crown_of_flowers",
		"level_cap_base": 75,
		"level_cap_evolved": 99,
		"base_stats": {"hp": 220, "mp": 100, "attack": 14, "defense": 12, "magic_power": 28, "spell_resistance": 18, "speed": 16},
		"growth": {"hp": 10, "mp": 5, "attack": 0.6, "defense": 0.6, "magic_power": 1.5, "spell_resistance": 0.9, "speed": 0.75},
		"weapon_types": ["staff", "wand", "rod"],
		"armor_types": ["light_armor", "robe", "accessory"],
		"can_use_shield": false,
		"starting_spells": ["cure_lv1"],
		"can_learn_spells": true,
		"portrait": "cookie",
	},
	"iris": {
		"name": "Iris",
		"starting_class": "nature_bound_druid",
		"evolved_class": "shapeshifter",
		"key_item_required": "ki_tuft_of_panda_fur",
		"level_cap_base": 75,
		"level_cap_evolved": 99,
		"base_stats": {"hp": 230, "mp": 70, "attack": 18, "defense": 14, "magic_power": 16, "spell_resistance": 14, "speed": 19},
		"growth": {"hp": 11, "mp": 3, "attack": 0.9, "defense": 0.7, "magic_power": 0.8, "spell_resistance": 0.7, "speed": 0.9},
		"weapon_types": ["claw", "staff"],
		"armor_types": ["light_armor", "robe", "accessory"],
		"can_use_shield": false,
		"starting_spells": [],
		"can_learn_spells": false,
		"learned_wildlife_attacks": [],
		"panda_form_available": false,
		"portrait": "iris",
	},
	"fritzzit": {
		"name": "Fritzzit",
		"starting_class": "sniper",
		"evolved_class": "sniper",  # No class change, weapon upgrade only
		"key_item_required": "ki_sniper_blueprint",
		"level_cap_base": 75,
		"level_cap_evolved": 99,
		"base_stats": {"hp": 240, "mp": 0, "attack": 26, "defense": 14, "magic_power": 0, "spell_resistance": 10, "speed": 17},
		"growth": {"hp": 11, "mp": 0, "attack": 1.4, "defense": 0.7, "magic_power": 0, "spell_resistance": 0.5, "speed": 0.85},
		"weapon_types": ["sniper_rifle"],
		"armor_types": ["light_armor", "medium_armor", "accessory"],
		"can_use_shield": false,
		"starting_spells": [],
		"can_learn_spells": false,
		"portrait": "fritzzit",
	},
	"crankpot": {
		"name": "Crankpot",
		"starting_class": "firemage",
		"evolved_class": "arsonist",
		"key_item_required": "ki_molotov_cocktail",
		"level_cap_base": 75,
		"level_cap_evolved": 99,
		"base_stats": {"hp": 215, "mp": 105, "attack": 13, "defense": 11, "magic_power": 33, "spell_resistance": 16, "speed": 16},
		"growth": {"hp": 9, "mp": 5, "attack": 0.55, "defense": 0.55, "magic_power": 1.8, "spell_resistance": 0.8, "speed": 0.75},
		"weapon_types": ["wand", "rod"],
		"armor_types": ["light_armor", "robe", "accessory"],
		"can_use_shield": false,
		"starting_spells": ["fire_lv1", "fira_lv2"],
		"can_learn_spells": true,
		"portrait": "crankpot",
	},
	"yipp": {
		"name": "Yipp",
		"starting_class": "necromancer",
		"evolved_class": "saint",  # OR "vampire" based on choice
		"key_item_required": "ki_holy_symbol",  # AND ki_pewter_wine_glass
		"level_cap_base": 75,
		"level_cap_evolved": 99,
		"base_stats": {"hp": 225, "mp": 108, "attack": 15, "defense": 12, "magic_power": 32, "spell_resistance": 20, "speed": 18},
		"growth": {"hp": 10, "mp": 5, "attack": 0.7, "defense": 0.6, "magic_power": 1.75, "spell_resistance": 1.0, "speed": 0.85},
		"weapon_types": ["staff", "wand"],
		"armor_types": ["light_armor", "robe", "accessory"],
		"can_use_shield": false,
		"starting_spells": ["drain_lv1", "bone_spike_lv1"],
		"can_learn_spells": true,
		"portrait": "yipp",
	},
}

# Level-up abilities for each character
const LEVEL_UP_ABILITIES := {
	"javin": {
		10: "crit_plus_10", 20: "shadow_step", 30: "dream_heal",
		40: "nightmare_strike", 50: "evasion_plus_15", 60: "dream_shield",
		70: "assassinate", 80: "terror_wave", 90: "dreamwalker_mastery"
	},
	"frostbite": {
		10: "piercing_shot", 20: "range_damage_plus_10", 30: "grenade_mastery",
		40: "scatter_shot", 50: "quick_reload", 60: "explosive_round",
		70: "crit_damage_plus_20", 80: "suppressing_fire", 90: "gunner_focus"
	},
	"fei": {
		10: "power_strike", 20: "phys_defense_plus_15", 30: "shield_bash",
		40: "berserker_rage", 50: "battle_cry", 60: "whirlwind_attack",
		70: "max_hp_plus_20", 80: "precision_strike", 90: "weapon_masters_edge"
	},
	"flood": {
		10: "ice_shard", 20: "frost_aura", 30: "glacial_spike",
		40: "double_cast", 50: "magic_power_plus_15", 60: "blizzard_storm",
		70: "absolute_zero", 80: "ice_queens_blessing", 90: "diamond_dust"
	},
	"hannah": {
		10: "elemental_strike", 20: "magic_power_plus_10", 30: "mana_shield",
		40: "chain_lightning", 50: "spell_focus", 60: "multi_cast",
		70: "arcane_mastery", 80: "meteor_swarm", 90: "magus_supremacy"
	},
	"michael": {
		10: "holy_light", 20: "healing_power_plus_10", 30: "divine_shield",
		40: "smite", 50: "raise", 60: "phys_defense_plus_20",
		70: "holy_aura", 80: "judgment", 90: "paladin_resolve"
	},
	"warghoul": {
		10: "death_strike", 20: "phys_attack_plus_15", 30: "undead_resilience",
		40: "soul_harvest", 50: "summon_skeleton", 60: "dark_aura",
		70: "max_hp_plus_25", 80: "reapers_touch", 90: "deathknight_dominion"
	},
	"cookie": {
		10: "entangle", 20: "nature_damage_plus_10", 30: "sandstorm",
		40: "thorns", 50: "natures_wrath", 60: "excessive_vinegrowth",
		70: "spell_resistance_plus_15", 80: "bubble", 90: "druidess_supremacy"
	},
	"iris": {
		10: "animal_instinct", 20: "wild_strike", 30: "shapeshifter_agility",
		40: "panda_form", 50: "predator_focus", 60: "pack_tactics",
		70: "phys_attack_plus_20", 80: "feral_rage", 90: "shapeshifter_mastery"
	},
	"fritzzit": {
		10: "headshot", 20: "crit_chance_plus_15", 30: "armor_piercing",
		40: "explosive_shot", 50: "eagle_eye", 60: "crit_damage_plus_25",
		70: "killshot", 80: "snipers_focus", 90: "deadeye"
	},
	"crankpot": {
		10: "fireball", 20: "fire_damage_plus_10", 30: "flame_wall",
		40: "inferno", 50: "burn_mastery", 60: "spell_power_plus_15",
		70: "blazing_aura", 80: "arson", 90: "pyromancer_fury"
	},
	"yipp_saint": {
		10: "holy_bolt", 20: "holy_damage_plus_15", 30: "mass_heal",
		40: "turn_undead", 50: "divine_intervention", 60: "holy_nova",
		70: "healing_power_plus_20", 80: "resurrect_all", 90: "saints_grace"
	},
	"yipp_vampire": {
		10: "drain_life", 20: "dark_damage_plus_15", 30: "blood_mist",
		40: "dominate_undead", 50: "vampiric_resilience", 60: "life_siphon",
		70: "max_hp_plus_20", 80: "blood_frenzy", 90: "vampire_lord"
	},
	"yipp": {
		10: "bone_spike", 20: "dark_damage_plus_10", 30: "summon_zombie",
		40: "curse", 50: "death_coil", 60: "spell_power_plus_15",
		70: "plague", 80: "void_touch", 90: "necromancer_mastery"
	},
}

func initialize_party(ng_plus_data: Dictionary = {}) -> void:
	character_states.clear()
	for char_id in CHARACTER_DATA:
		var data := CHARACTER_DATA[char_id]
		var starting_level := 1

		if not ng_plus_data.is_empty():
			# New Game+ starting levels
			var prev_class := ng_plus_data.get("character_classes", {}).get(char_id, "")
			var has_evolved := (prev_class != "" and prev_class != data["starting_class"])
			var had_ultimate := char_id in ng_plus_data.get("ultimate_weapons", [])

			if char_id == "flood":
				starting_level = 99
			elif has_evolved or (char_id in ["frostbite","fritzzit"] and had_ultimate):
				starting_level = 99
			else:
				starting_level = 75

		character_states[char_id] = _create_character_state(char_id, starting_level)

func _create_character_state(char_id: String, level: int = 1) -> Dictionary:
	var data := CHARACTER_DATA[char_id]
	var stats := _calculate_stats_at_level(char_id, level)

	return {
		"char_id": char_id,
		"level": level,
		"exp": 0,
		"exp_to_next": _exp_to_level(level + 1),
		"current_class": data["starting_class"],
		"has_evolved": false,
		"hp": stats.hp,
		"max_hp": stats.hp,
		"mp": stats.mp,
		"max_mp": stats.mp,
		"stats": stats,
		"equipment": {
			"weapon": "",
			"armor": "",
			"shield": "",
			"accessory": "",
			"special": "",
		},
		"spells": data["starting_spells"].duplicate(),
		"abilities": [],
		"status_effects": [],
		"learned_wildlife_attacks": [],  # For Iris
		"baby_dragon_counter": 0,        # For Javin
	}

func _calculate_stats_at_level(char_id: String, level: int) -> Dictionary:
	var data := CHARACTER_DATA[char_id]
	var base := data["base_stats"]
	var growth := data["growth"]
	var lv := max(1, level - 1)

	return {
		"hp": int(base["hp"] + growth["hp"] * lv),
		"mp": int(base["mp"] + growth["mp"] * lv),
		"attack": int(base["attack"] + growth["attack"] * lv),
		"defense": int(base["defense"] + growth["defense"] * lv),
		"magic_power": int(base["magic_power"] + growth["magic_power"] * lv),
		"spell_resistance": int(base["spell_resistance"] + growth["spell_resistance"] * lv),
		"speed": int(base["speed"] + growth["speed"] * lv),
	}

func _exp_to_level(target_level: int) -> int:
	# FF6-style exponential curve
	if target_level <= 1:
		return 0
	return int(pow(target_level, 2.8) * 12)

func get_character(char_id: String) -> Dictionary:
	return character_states.get(char_id, {})

func add_exp(char_id: String, exp: int) -> void:
	if not character_states.has(char_id):
		return
	var char_state := character_states[char_id]
	var data := CHARACTER_DATA[char_id]
	var max_lv := data["level_cap_evolved"] if char_state["has_evolved"] else data["level_cap_base"]

	char_state["exp"] += exp
	while char_state["level"] < max_lv and char_state["exp"] >= char_state["exp_to_next"]:
		char_state["exp"] -= char_state["exp_to_next"]
		char_state["level"] += 1
		_on_level_up(char_id)

func _on_level_up(char_id: String) -> void:
	var char_state := character_states[char_id]
	var new_level := char_state["level"]
	var new_stats := _calculate_stats_at_level(char_id, new_level)

	# Update stats, preserve HP/MP percentages
	var hp_pct := float(char_state["hp"]) / float(char_state["max_hp"])
	var mp_pct := float(char_state["mp"]) / float(char_state["max_mp"]) if char_state["max_mp"] > 0 else 1.0

	char_state["max_hp"] = new_stats.hp
	char_state["max_mp"] = new_stats.mp
	char_state["hp"] = int(new_stats.hp * hp_pct)
	char_state["mp"] = int(new_stats.mp * mp_pct)
	char_state["stats"] = new_stats
	char_state["exp_to_next"] = _exp_to_level(new_level + 1)

	# Check for level-up ability
	if new_level % 10 == 0:
		_grant_level_up_ability(char_id, new_level)

	AudioManager.play_sfx("level_up")
	character_leveled_up.emit(char_id, new_level)

func _grant_level_up_ability(char_id: String, level: int) -> void:
	var char_state := character_states[char_id]
	var alignment := FlagManager.get_flag("yipp_alignment")

	# Choose correct ability table for Yipp based on alignment
	var ability_table_key := char_id
	if char_id == "yipp" and alignment == "saint":
		ability_table_key = "yipp_saint"
	elif char_id == "yipp" and alignment == "vampire":
		ability_table_key = "yipp_vampire"

	var abilities := LEVEL_UP_ABILITIES.get(ability_table_key, {})
	if abilities.has(level):
		var ability_id: String = abilities[level]
		if not ability_id in char_state["abilities"]:
			char_state["abilities"].append(ability_id)

func evolve_character(char_id: String) -> bool:
	if not character_states.has(char_id):
		return false
	var char_state := character_states[char_id]
	if char_state["has_evolved"]:
		return false

	var data := CHARACTER_DATA[char_id]
	# Yipp's evolution depends on sidequest choice
	var new_class := data["evolved_class"]
	if char_id == "yipp":
		var alignment := FlagManager.get_flag("yipp_alignment")
		new_class = alignment if alignment in ["saint","vampire"] else "necromancer"

	char_state["current_class"] = new_class
	char_state["has_evolved"] = true

	# Fei loses shield slot when becoming Weapon Master
	if new_class == "weapon_master":
		char_state["equipment"]["shield"] = ""

	character_evolved.emit(char_id, new_class)
	return true

func learn_spell(char_id: String, spell_id: String) -> bool:
	if not character_states.has(char_id):
		return false
	var char_state := character_states[char_id]
	var data := CHARACTER_DATA[char_id]

	# Check if character can learn spells
	if not data.get("can_learn_spells", false):
		return false

	# Javin exception: only starts with fire_lv1, can learn psychic if Dreamwalker
	if char_id == "javin":
		if not char_state["has_evolved"]:
			return false

	if not spell_id in char_state["spells"]:
		char_state["spells"].append(spell_id)
	return true

func learn_wildlife_attack(iris_attack_data: Dictionary) -> void:
	if not character_states.has("iris"):
		return
	var iris := character_states["iris"]
	iris["learned_wildlife_attacks"].append(iris_attack_data)

func get_all_final_levels() -> Dictionary:
	var levels := {}
	for char_id in character_states:
		levels[char_id] = character_states[char_id]["level"]
	return levels

func get_all_classes() -> Dictionary:
	var classes := {}
	for char_id in character_states:
		classes[char_id] = character_states[char_id]["current_class"]
	return classes

func get_ultimate_weapons() -> Array:
	var uw := []
	if FlagManager.is_flag("frostbite_ultimate_weapon"):
		uw.append("frostbite")
	if FlagManager.is_flag("fritzzit_ultimate_weapon"):
		uw.append("fritzzit")
	return uw

func export_state() -> Dictionary:
	return character_states.duplicate(true)

func import_state(data: Dictionary) -> void:
	character_states = data.duplicate(true)

func flood_permanent_death() -> void:
	if character_states.has("flood"):
		# Drop equipment to inventory
		var flood_equip := character_states["flood"]["equipment"]
		for slot in flood_equip:
			if flood_equip[slot] != "":
				GameManager.equipment.get_or_add("dropped", [])
				# Add equipment back to inventory pool
				pass
		FlagManager.set_flag("flood_dead", true)
		GameManager.active_party.erase("flood")
		GameManager.reserve_party.erase("flood")
