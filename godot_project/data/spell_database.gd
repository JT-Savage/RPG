extends Node
class_name SpellDatabase
## SpellDatabase - All spells: MP cost = spell level, class restrictions, elements

const SPELLS := {
	# ===== LEVEL 1 SPELLS (1 MP) =====
	"fire_lv1": {
		"name": "Fire", "level": 1, "mp_cost": 1, "element": "fire",
		"base_power": 18, "target": "single_enemy", "is_offensive": true,
		"classes_allowed": ["firemage","arsonist","witch","magus","cleric","paladin",
							"necromancer","deathknight","dreamwalker","saint","vampire",
							"druid","druidess"],
		"description": "A small burst of fire damage.",
	},
	"blizzard_lv1": {
		"name": "Blizzard", "level": 1, "mp_cost": 1, "element": "water",
		"base_power": 18, "target": "single_enemy", "is_offensive": true,
		"classes_allowed": ["ice_mage","witch","magus","cleric","paladin",
							"necromancer","deathknight","saint","druid","druidess"],
		"description": "A shard of ice deals water damage.",
	},
	"thunder_lv1": {
		"name": "Thunder", "level": 1, "mp_cost": 1, "element": "thunder",
		"base_power": 18, "target": "single_enemy", "is_offensive": true,
		"classes_allowed": ["witch","magus","firemage","arsonist","necromancer",
							"deathknight","saint","druid","druidess"],
		"description": "A bolt of lightning strikes one enemy.",
	},
	"cure_lv1": {
		"name": "Cure", "level": 1, "mp_cost": 1, "element": "none",
		"base_power": 45, "target": "single_ally", "is_heal": true,
		"classes_allowed": ["cleric","paladin","witch","magus","druid","druidess","saint"],
		"description": "Restores a small amount of HP.",
	},
	"drain_lv1": {
		"name": "Drain", "level": 1, "mp_cost": 1, "element": "darkness",
		"base_power": 15, "target": "single_enemy", "is_offensive": true, "is_drain": true,
		"classes_allowed": ["necromancer","deathknight","vampire","witch","magus"],
		"description": "Drains HP from an enemy to heal the caster.",
	},
	"bone_spike_lv1": {
		"name": "Bone Spike", "level": 1, "mp_cost": 1, "element": "earth",
		"base_power": 20, "target": "single_enemy", "is_offensive": true,
		"classes_allowed": ["necromancer","deathknight"],
		"description": "A spike of bone erupts from the ground.",
	},

	# ===== LEVEL 2 SPELLS (2 MP) =====
	"fira_lv2": {
		"name": "Fira", "level": 2, "mp_cost": 2, "element": "fire",
		"base_power": 42, "target": "single_enemy", "is_offensive": true,
		"classes_allowed": ["firemage","arsonist","witch","magus","dreamwalker"],
		"description": "A larger fire attack.",
	},
	"blizzara_lv2": {
		"name": "Blizzara", "level": 2, "mp_cost": 2, "element": "water",
		"base_power": 42, "target": "single_enemy", "is_offensive": true,
		"classes_allowed": ["ice_mage","witch","magus"],
		"description": "A stronger ice attack.",
	},
	"thundara_lv2": {
		"name": "Thundara", "level": 2, "mp_cost": 2, "element": "thunder",
		"base_power": 42, "target": "single_enemy", "is_offensive": true,
		"classes_allowed": ["witch","magus","firemage","arsonist"],
		"description": "A stronger thunder bolt.",
	},
	"cura_lv2": {
		"name": "Cura", "level": 2, "mp_cost": 2, "element": "none",
		"base_power": 110, "target": "single_ally", "is_heal": true,
		"classes_allowed": ["cleric","paladin","witch","magus","druid","druidess","saint"],
		"description": "Restores a moderate amount of HP.",
	},
	"sleep_lv2": {
		"name": "Sleep", "level": 2, "mp_cost": 2, "element": "none",
		"base_power": 0, "target": "single_enemy", "inflicts_status": "sleep",
		"classes_allowed": ["necromancer","deathknight","witch","magus","druid","druidess"],
		"description": "Puts an enemy to sleep.",
	},

	# ===== LEVEL 3 SPELLS (3 MP) =====
	"firaga_lv3": {
		"name": "Firaga", "level": 3, "mp_cost": 3, "element": "fire",
		"base_power": 80, "target": "single_enemy", "is_offensive": true,
		"classes_allowed": ["firemage","arsonist","witch","magus"],
		"description": "A powerful burst of fire.",
	},
	"blizzaga_lv3": {
		"name": "Blizzaga", "level": 3, "mp_cost": 3, "element": "water",
		"base_power": 80, "target": "single_enemy", "is_offensive": true,
		"classes_allowed": ["ice_mage","witch","magus"],
		"description": "A powerful ice attack.",
	},
	"thundaga_lv3": {
		"name": "Thundaga", "level": 3, "mp_cost": 3, "element": "thunder",
		"base_power": 80, "target": "single_enemy", "is_offensive": true,
		"classes_allowed": ["witch","magus"],
		"description": "A powerful lightning strike.",
	},
	"curaga_lv3": {
		"name": "Curaga", "level": 3, "mp_cost": 3, "element": "none",
		"base_power": 250, "target": "single_ally", "is_heal": true,
		"classes_allowed": ["cleric","paladin","witch","magus","druid","druidess","saint"],
		"description": "Restores a large amount of HP.",
	},
	"poison_lv3": {
		"name": "Poison", "level": 3, "mp_cost": 3, "element": "none",
		"base_power": 0, "target": "single_enemy", "inflicts_status": "poison",
		"classes_allowed": ["necromancer","deathknight","witch","magus","druid","druidess"],
		"description": "Poisons the target.",
	},
	"bio_lv3": {
		"name": "Bio", "level": 3, "mp_cost": 3, "element": "none",
		"base_power": 55, "target": "single_enemy", "is_offensive": true, "inflicts_status": "poison",
		"classes_allowed": ["necromancer","deathknight","witch","magus"],
		"description": "Toxic damage that also poisons.",
	},

	# ===== LEVEL 4 SPELLS (4 MP) =====
	"haste_lv4": {
		"name": "Haste", "level": 4, "mp_cost": 4, "element": "none",
		"base_power": 0, "target": "single_ally", "inflicts_status": "haste",
		"classes_allowed": ["cleric","paladin","witch","magus","druid","druidess","saint"],
		"description": "Speeds up an ally's ATB gauge.",
	},
	"slow_lv4": {
		"name": "Slow", "level": 4, "mp_cost": 4, "element": "none",
		"base_power": 0, "target": "single_enemy", "inflicts_status": "slow",
		"classes_allowed": ["witch","magus","necromancer","deathknight","druid","druidess"],
		"description": "Slows an enemy's ATB gauge.",
	},
	"protect_lv4": {
		"name": "Protect", "level": 4, "mp_cost": 4, "element": "none",
		"base_power": 0, "target": "single_ally", "buff": "defense_up",
		"classes_allowed": ["cleric","paladin","witch","magus","saint"],
		"description": "Raises physical defense temporarily.",
	},
	"shell_lv4": {
		"name": "Shell", "level": 4, "mp_cost": 4, "element": "none",
		"base_power": 0, "target": "single_ally", "buff": "spell_resistance_up",
		"classes_allowed": ["cleric","paladin","witch","magus","saint"],
		"description": "Raises magic resistance temporarily.",
	},
	"confuse_lv4": {
		"name": "Confuse", "level": 4, "mp_cost": 4, "element": "none",
		"base_power": 0, "target": "single_enemy", "inflicts_status": "confuse",
		"classes_allowed": ["necromancer","deathknight","witch","magus","vampire"],
		"description": "Confuses an enemy.",
	},

	# ===== LEVEL 5 SPELLS (5 MP) =====
	"quake_lv5": {
		"name": "Quake", "level": 5, "mp_cost": 5, "element": "earth",
		"base_power": 120, "target": "all_enemies", "is_offensive": true,
		"classes_allowed": ["witch","magus","druid","druidess","firemage","arsonist"],
		"description": "Massive earth damage to all enemies.",
	},
	"tornado_lv5": {
		"name": "Tornado", "level": 5, "mp_cost": 5, "element": "none",
		"base_power": 140, "target": "single_enemy", "is_offensive": true,
		"classes_allowed": ["witch","magus","druid","druidess"],
		"description": "A devastating wind attack.",
	},
	"esuna_lv5": {
		"name": "Esuna", "level": 5, "mp_cost": 5, "element": "none",
		"base_power": 0, "target": "single_ally", "is_heal": true, "is_esuna": true,
		"classes_allowed": ["cleric","paladin","witch","magus","druid","druidess","saint"],
		"description": "Removes all status effects from an ally.",
	},
	"raise_lv5": {
		"name": "Raise", "level": 5, "mp_cost": 5, "element": "light",
		"base_power": 0, "target": "ko_ally", "is_raise": true,
		"classes_allowed": ["paladin"],
		"description": "Resurrects a fallen ally with 30% HP. (Paladin only)",
	},

	# ===== LEVEL 6 SPELLS (6 MP) =====
	"flare_lv6": {
		"name": "Flare", "level": 6, "mp_cost": 6, "element": "fire",
		"base_power": 200, "target": "single_enemy", "is_offensive": true,
		"classes_allowed": ["firemage","arsonist","witch","magus"],
		"description": "Non-elemental fire annihilation.",
	},
	"holy_lv6": {
		"name": "Holy", "level": 6, "mp_cost": 6, "element": "light",
		"base_power": 190, "target": "single_enemy", "is_offensive": true,
		"bonus_vs_undead": 1.5,
		"classes_allowed": ["cleric","paladin","saint"],
		"description": "Sacred light that deals bonus damage to undead.",
	},
	"dark_lv6": {
		"name": "Dark", "level": 6, "mp_cost": 6, "element": "darkness",
		"base_power": 185, "target": "single_enemy", "is_offensive": true, "is_drain": true,
		"classes_allowed": ["necromancer","deathknight","vampire","witch","magus"],
		"description": "Drains life from target to heal caster.",
	},

	# ===== LEVEL 7 SPELLS (7 MP) =====
	"meteor_lv7": {
		"name": "Meteor", "level": 7, "mp_cost": 7, "element": "none",
		"base_power": 260, "target": "all_enemies", "is_offensive": true,
		"classes_allowed": ["witch","magus","firemage","arsonist"],
		"description": "Rains meteors on all enemies.",
	},
	"ultima_lv7": {
		"name": "Ultima", "level": 7, "mp_cost": 7, "element": "none",
		"base_power": 300, "target": "all_enemies", "is_offensive": true,
		"classes_allowed": ["magus","saint"],
		"description": "The ultimate spell, damages all enemies.",
	},
	"doom_lv7": {
		"name": "Doom", "level": 7, "mp_cost": 7, "element": "darkness",
		"base_power": 0, "target": "single_enemy", "instant_kill": true,
		"no_effect_on_boss": true,
		"classes_allowed": ["necromancer","deathknight","vampire"],
		"description": "Instantly kills a non-boss enemy.",
	},

	# ===== LEVEL 8 SPELLS (8 MP) =====
	"absolute_zero_lv8": {
		"name": "Absolute Zero", "level": 8, "mp_cost": 8, "element": "water",
		"base_power": 350, "target": "single_enemy", "is_offensive": true, "inflicts_status": "slow",
		"classes_allowed": ["ice_mage"],
		"description": "Freezes one enemy solid. (Ice Mage ability)",
	},
	"death_coil_lv8": {
		"name": "Death Coil", "level": 8, "mp_cost": 8, "element": "darkness",
		"base_power": 280, "target": "all_enemies", "is_offensive": true,
		"classes_allowed": ["necromancer","deathknight","vampire"],
		"description": "Dark energy coils strike all enemies.",
	},

	# ===== LEVEL 9 SPELLS (9 MP) =====
	"diamond_dust_lv9": {
		"name": "Diamond Dust", "level": 9, "mp_cost": 9, "element": "water",
		"base_power": 500, "target": "all_enemies", "is_offensive": true,
		"classes_allowed": ["ice_mage"],
		"description": "Flood's ultimate. Massive AoE ice damage. (Ice Mage only)",
	},
	"sensory_deprivation_lv9": {
		"name": "Sensory Deprivation", "level": 9, "mp_cost": 9, "element": "none",
		"base_power": 0, "target": "all_enemies",
		"inflicts_multiple": ["silence", "spell_resistance_down"],
		"duration": 5,
		"classes_allowed": ["druidess"],
		"shop_location": "desert_only",
		"description": "All enemies lose magic resistance and are Silenced for 5 turns. (Druidess only, desert purchase)",
	},

	# ===== DREAMWALKER EXCLUSIVE SPELLS (Psychic damage) =====
	"nightmare_bolt_lv4": {
		"name": "Nightmare Bolt", "level": 4, "mp_cost": 4, "element": "psychic",
		"base_power": 14, "target": "single_enemy", "is_offensive": true,
		"damage_type": "psychic",
		"classes_allowed": ["dreamwalker"],
		"description": "Unresistable psychic damage. (Dreamwalker only)",
	},
	"dream_heal_lv3": {
		"name": "Dream Heal", "level": 3, "mp_cost": 3, "element": "none",
		"base_power": 180, "target": "single_ally", "is_heal": true,
		"classes_allowed": ["dreamwalker"],
		"description": "Heals an ally with dream energy. (Dreamwalker only)",
	},
	"dream_shield_lv5": {
		"name": "Dream Shield", "level": 5, "mp_cost": 5, "element": "none",
		"base_power": 0, "target": "all_allies", "buff": "psychic_shield",
		"classes_allowed": ["dreamwalker"],
		"description": "Shields all allies with psychic energy. (Dreamwalker only)",
	},
	"nightmare_storm_lv6": {
		"name": "Nightmare Storm", "level": 6, "mp_cost": 6, "element": "psychic",
		"base_power": 20, "target": "all_enemies", "is_offensive": true,
		"damage_type": "psychic",
		"classes_allowed": ["dreamwalker"],
		"description": "Psychic storm hits all enemies. Unresistable. (Dreamwalker only)",
	},
	"terror_wave_lv8": {
		"name": "Terror Wave", "level": 8, "mp_cost": 8, "element": "psychic",
		"base_power": 28, "target": "all_enemies", "is_offensive": true,
		"damage_type": "psychic", "inflicts_status": "confuse",
		"classes_allowed": ["dreamwalker"],
		"description": "Massive psychic AoE + Confuse. (Dreamwalker only)",
	},

	# ===== DRUIDESS EXCLUSIVE =====
	"sandstorm_lv4": {
		"name": "Sandstorm", "level": 4, "mp_cost": 4, "element": "earth",
		"base_power": 0, "target": "all_enemies", "inflicts_status": "blind",
		"classes_allowed": ["druidess"],
		"description": "Blinds all enemies. (Druidess only)",
	},
	"excessive_vinegrowth_lv5": {
		"name": "Excessive Vinegrowth", "level": 5, "mp_cost": 5, "element": "none",
		"base_power": 0, "target": "all_enemies", "inflicts_status": "slow",
		"classes_allowed": ["druidess"],
		"description": "Slows all enemies. (Druidess only)",
	},
	"bubble_lv6": {
		"name": "Bubble", "level": 6, "mp_cost": 6, "element": "none",
		"base_power": 0, "target": "single_enemy", "inflicts_status": "bubble",
		"classes_allowed": ["druidess"],
		"description": "Silences and prevents attacking. Pops if hit. (Druidess only)",
	},

	# ===== SAINT EXCLUSIVE =====
	"mass_heal_lv6": {
		"name": "Mass Heal", "level": 6, "mp_cost": 6, "element": "none",
		"base_power": 200, "target": "all_allies", "is_heal": true,
		"classes_allowed": ["saint"],
		"description": "Heals all allies. (Saint only)",
	},
	"holy_nova_lv7": {
		"name": "Holy Nova", "level": 7, "mp_cost": 7, "element": "light",
		"base_power": 220, "target": "all_enemies", "is_offensive": true,
		"bonus_vs_undead": 1.75,
		"classes_allowed": ["saint"],
		"description": "AoE holy damage, devastating to undead. (Saint only)",
	},
	"resurrect_all_lv9": {
		"name": "Resurrect All", "level": 9, "mp_cost": 9, "element": "light",
		"base_power": 0, "target": "all_ko_allies", "is_raise": true,
		"classes_allowed": ["saint"],
		"description": "Revives all fallen allies with 50% HP. (Saint only)",
	},

	# ===== VAMPIRE EXCLUSIVE =====
	"drain_life_lv4": {
		"name": "Drain Life", "level": 4, "mp_cost": 4, "element": "darkness",
		"base_power": 100, "target": "single_enemy", "is_drain": true,
		"classes_allowed": ["vampire"],
		"description": "Steals HP from an enemy. (Vampire only)",
	},
	"blood_mist_lv6": {
		"name": "Blood Mist", "level": 6, "mp_cost": 6, "element": "darkness",
		"base_power": 130, "target": "all_enemies", "is_drain": true, "party_heal": true,
		"classes_allowed": ["vampire"],
		"description": "Damages all living enemies, heals party. (Vampire only)",
	},
	"dominate_undead_lv5": {
		"name": "Dominate Undead", "level": 5, "mp_cost": 5, "element": "darkness",
		"base_power": 0, "target": "single_undead_enemy", "is_control": true,
		"classes_allowed": ["vampire"],
		"description": "Control a non-boss undead enemy. (Vampire only)",
	},

	# ===== PALADIN EXCLUSIVE (already in Lv5 above) =====

	# ===== DEATHKNIGHT EXCLUSIVE =====
	"dark_aura_lv6": {
		"name": "Dark Aura", "level": 6, "mp_cost": 6, "element": "darkness",
		"base_power": 40, "target": "all_enemies", "is_offensive": true, "persistent": true,
		"classes_allowed": ["deathknight"],
		"description": "Dark energy damages nearby enemies each turn. (Deathknight only)",
	},
}

# ===== API =====

static func get_spell(spell_id: String) -> Dictionary:
	return SPELLS.get(spell_id, {})

static func get_spells_for_class(class_name_str: String) -> Array:
	var result := []
	for spell_id in SPELLS:
		var spell := SPELLS[spell_id]
		if class_name_str in spell.get("classes_allowed", []):
			result.append(spell_id)
	return result

static func can_learn_spell(spell_id: String, class_name_str: String) -> bool:
	var spell := SPELLS.get(spell_id, {})
	return class_name_str in spell.get("classes_allowed", [])

static func get_mp_cost(spell_id: String) -> int:
	return SPELLS.get(spell_id, {}).get("mp_cost", 1)

static func is_purchasable(spell_id: String, location: String) -> bool:
	var spell := SPELLS.get(spell_id, {})
	var shop_loc := spell.get("shop_location", "any")
	if shop_loc == "desert_only":
		return location.begins_with("desert")
	return true

static func get_all_spell_ids() -> Array:
	return SPELLS.keys()
