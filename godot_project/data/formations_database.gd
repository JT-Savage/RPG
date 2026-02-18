class_name FormationsDatabase

const FORMATIONS: Dictionary = {

	# -------------------------------------------------------------------------
	# WARREN AREA
	# -------------------------------------------------------------------------
	"kobold_scouts": {
		"enemies": ["infected_kobold", "infected_kobold"],
		"weight": 30,
		"location": "warren",
	},
	"kobold_pack": {
		"enemies": ["infected_kobold", "infected_kobold", "infected_kobold"],
		"weight": 20,
		"location": "warren",
	},
	"zombie_ambush": {
		"enemies": ["zombie_kobold", "zombie_kobold", "infected_kobold"],
		"weight": 15,
		"location": "warren",
	},
	"warren_ambush": {
		"enemies": ["infected_kobold", "infected_kobold", "infected_kobold", "infected_kobold"],
		"weight": 10,
		"location": "warren",
	},

	# -------------------------------------------------------------------------
	# SURFACE FOREST
	# -------------------------------------------------------------------------
	"wolf_pair": {
		"enemies": ["forest_wolf", "forest_wolf"],
		"weight": 30,
		"location": "surface_forest",
	},
	"goblin_gang": {
		"enemies": ["goblin", "goblin", "goblin"],
		"weight": 25,
		"location": "surface_forest",
	},
	"forest_ambush": {
		"enemies": ["forest_wolf", "goblin", "goblin"],
		"weight": 20,
		"location": "surface_forest",
	},
	"lone_troll": {
		"enemies": ["forest_troll"],
		"weight": 10,
		"location": "surface_forest",
	},

	# -------------------------------------------------------------------------
	# CATACOMB
	# -------------------------------------------------------------------------
	"skeleton_pair": {
		"enemies": ["skeleton", "skeleton"],
		"weight": 30,
		"location": "catacomb",
	},
	"undead_trio": {
		"enemies": ["skeleton", "zombie", "ghost"],
		"weight": 20,
		"location": "catacomb",
	},
	"catacomb_ambush": {
		"enemies": ["skeleton_warrior", "skeleton_warrior", "skeleton"],
		"weight": 15,
		"location": "catacomb",
	},
	"lich_encounter_pre_boss": {
		"enemies": ["lich_minion", "lich_minion"],
		"weight": 10,
		"location": "catacomb",
	},
	"catacomb_lich": {
		"enemies": ["catacomb_lich"],
		"weight": 0,
		"location": "catacomb",
		"boss": true,
	},

	# -------------------------------------------------------------------------
	# SWAMP
	# -------------------------------------------------------------------------
	"poison_pair": {
		"enemies": ["poison_frog", "poison_frog"],
		"weight": 30,
		"location": "swamp",
	},
	"swamp_pack": {
		"enemies": ["swamp_beast", "poison_frog", "poison_frog"],
		"weight": 20,
		"location": "swamp",
	},
	"bog_terror": {
		"enemies": ["swamp_beast", "swamp_beast"],
		"weight": 15,
		"location": "swamp",
	},
	"swamp_witch_random": {
		"enemies": ["swamp_witch"],
		"weight": 5,
		"location": "swamp",
		"rare": true,
	},

	# -------------------------------------------------------------------------
	# DESERT
	# -------------------------------------------------------------------------
	"scorpion_scout": {
		"enemies": ["sand_scorpion", "sand_scorpion"],
		"weight": 30,
		"location": "desert",
	},
	"desert_pack": {
		"enemies": ["desert_wraith", "sand_scorpion", "sand_scorpion"],
		"weight": 20,
		"location": "desert",
	},
	"sandstorm_spawn": {
		"enemies": ["desert_wraith", "desert_wraith", "desert_wraith"],
		"weight": 15,
		"location": "desert",
	},
	"desert_warlord": {
		"enemies": ["desert_warlord"],
		"weight": 0,
		"location": "desert",
		"boss": true,
	},

	# -------------------------------------------------------------------------
	# MOUNTAIN
	# -------------------------------------------------------------------------
	"troll_pair": {
		"enemies": ["mountain_troll", "mountain_troll"],
		"weight": 25,
		"location": "mountain",
	},
	"ice_patrol": {
		"enemies": ["ice_witch", "ice_witch"],
		"weight": 20,
		"location": "mountain",
	},
	"mountain_ambush": {
		"enemies": ["mountain_troll", "ice_witch", "ice_knight"],
		"weight": 15,
		"location": "mountain",
	},

	# -------------------------------------------------------------------------
	# ARMY CAMP
	# -------------------------------------------------------------------------
	"imperial_patrol": {
		"enemies": ["imperial_guard", "imperial_guard", "imperial_guard"],
		"weight": 25,
		"location": "army_camp",
	},
	"elite_squad": {
		"enemies": ["imperial_elite", "imperial_elite", "captain"],
		"weight": 15,
		"location": "army_camp",
	},
	"captain_donald_boss": {
		"enemies": ["captain_donald"],
		"weight": 0,
		"location": "army_camp",
		"boss": true,
	},

	# -------------------------------------------------------------------------
	# FLOATING ISLAND
	# -------------------------------------------------------------------------
	"sky_serpent_pair": {
		"enemies": ["sky_serpent", "sky_serpent"],
		"weight": 30,
		"location": "floating_island",
	},
	"wind_elemental_trio": {
		"enemies": ["wind_elemental", "wind_elemental", "wind_elemental"],
		"weight": 20,
		"location": "floating_island",
	},
	"sky_ambush": {
		"enemies": ["sky_serpent", "wind_elemental", "wind_elemental"],
		"weight": 15,
		"location": "floating_island",
	},

	# -------------------------------------------------------------------------
	# FINAL DUNGEON
	# -------------------------------------------------------------------------
	"void_knight_patrol": {
		"enemies": ["void_knight", "void_knight"],
		"weight": 25,
		"location": "final_dungeon",
	},
	"shadow_dragons": {
		"enemies": ["shadow_dragon", "shadow_dragon"],
		"weight": 20,
		"location": "final_dungeon",
	},
	"void_elite": {
		"enemies": ["void_knight", "shadow_dragon", "corrupted_saint"],
		"weight": 15,
		"location": "final_dungeon",
	},
	"void_architect": {
		"enemies": ["void_architect"],
		"weight": 0,
		"location": "final_dungeon",
		"boss": true,
		"music": "battle_secret_boss",
	},

	# -------------------------------------------------------------------------
	# SPECIAL
	# -------------------------------------------------------------------------
	# Post-Orisia-deadline formation. Enemy list is populated at runtime by
	# FlagManager, which fills slots with any party members who were never
	# recruited, resurrected as zombies. The "dynamic": true flag signals
	# BattleManager to call FormationsDatabase.build_zombie_party() instead of
	# using the enemies array directly.
	"zombie_party_members": {
		"enemies": [],
		"weight": 0,
		"location": "all",
		"dynamic": true,
		"dynamic_builder": "build_zombie_party",
	},
}


# Returns the formation dictionary for a given ID, or an empty dict if not found.
static func get_formation(id: String) -> Dictionary:
	return FORMATIONS.get(id, {})


# Returns every formation whose location matches one of the strings in pool,
# or whose location is "all". Boss formations (weight == 0) are excluded.
static func get_formations_for_pool(pool: Array) -> Array:
	var result: Array = []
	for id in FORMATIONS:
		var f: Dictionary = FORMATIONS[id]
		if f.get("boss", false):
			continue
		if f.get("weight", 0) <= 0:
			continue
		var loc: String = f.get("location", "all")
		if loc == "all" or loc in pool:
			result.append(f.duplicate())
			result[-1]["id"] = id
	return result


# Picks a random formation from the pool using weighted selection.
# Returns an empty dictionary if the pool is empty.
static func pick_random_formation(pool: Array) -> Dictionary:
	var formations: Array = get_formations_for_pool(pool)
	if formations.is_empty():
		return {}

	var total_weight: int = 0
	for f in formations:
		total_weight += f.get("weight", 0)

	if total_weight <= 0:
		return formations[randi() % formations.size()]

	var roll: int = randi() % total_weight
	var cumulative: int = 0
	for f in formations:
		cumulative += f.get("weight", 0)
		if roll < cumulative:
			return f

	return formations[-1]


# Called by BattleManager when the dynamic_builder field equals
# "build_zombie_party". Queries FlagManager for unrecruited characters and
# returns a formation dictionary with their zombie enemy IDs.
static func build_zombie_party() -> Dictionary:
	var zombie_enemies: Array = []

	# FlagManager is an autoload; access it through the engine singleton map.
	# Each unrecruited character ID maps to a corresponding zombie enemy ID.
	var character_to_zombie: Dictionary = {
		"protagonist": "zombie_protagonist",
		"healer":      "zombie_healer",
		"warrior":     "zombie_warrior",
		"rogue":       "zombie_rogue",
		"mage":        "zombie_mage",
		"druidess":    "zombie_druidess",
		"dreamwalker": "zombie_dreamwalker",
	}

	if Engine.has_singleton("FlagManager"):
		var fm = Engine.get_singleton("FlagManager")
		for char_id in character_to_zombie:
			if not fm.is_recruited(char_id):
				zombie_enemies.append(character_to_zombie[char_id])
	else:
		# Fallback: fill with generic zombie kobolds so the battle still fires.
		zombie_enemies = ["zombie_kobold", "zombie_kobold", "zombie_kobold"]

	# Cap at four enemies to stay within the battle system's slot limit.
	zombie_enemies = zombie_enemies.slice(0, 4)

	return {
		"id":       "zombie_party_members",
		"enemies":  zombie_enemies,
		"weight":   0,
		"location": "all",
		"dynamic":  true,
	}
