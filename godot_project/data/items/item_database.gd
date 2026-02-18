class_name ItemDatabase

const ITEMS: Dictionary = {
	# --- Healing ---
	"potion": {
		"name": "Potion",
		"description": "Restores 100 HP.",
		"price": 50,
		"sell_price": 25,
		"effect": "heal_hp",
		"value": 100,
		"target": "single",
		"sold_in_shops": true,
		"category": "healing"
	},
	"hi_potion": {
		"name": "Hi-Potion",
		"description": "Restores 500 HP.",
		"price": 200,
		"sell_price": 100,
		"effect": "heal_hp",
		"value": 500,
		"target": "single",
		"sold_in_shops": true,
		"category": "healing"
	},
	"mega_potion": {
		"name": "Mega Potion",
		"description": "Restores 2000 HP.",
		"price": 800,
		"sell_price": 400,
		"effect": "heal_hp",
		"value": 2000,
		"target": "single",
		"sold_in_shops": true,
		"category": "healing"
	},
	"elixir": {
		"name": "Elixir",
		"description": "Fully restores HP and MP.",
		"price": 5000,
		"sell_price": 2500,
		"effect": "heal_hp_mp_full",
		"value": 0,
		"target": "single",
		"sold_in_shops": false,
		"category": "healing"
	},
	"ether": {
		"name": "Ether",
		"description": "Restores 50 MP.",
		"price": 150,
		"sell_price": 75,
		"effect": "heal_mp",
		"value": 50,
		"target": "single",
		"sold_in_shops": true,
		"category": "healing"
	},
	"hi_ether": {
		"name": "Hi-Ether",
		"description": "Restores 200 MP.",
		"price": 600,
		"sell_price": 300,
		"effect": "heal_mp",
		"value": 200,
		"target": "single",
		"sold_in_shops": true,
		"category": "healing"
	},

	# --- Status Cure ---
	"antidote": {
		"name": "Antidote",
		"description": "Cures poison.",
		"price": 30,
		"sell_price": 15,
		"effect": "cure_status",
		"value": "poison",
		"target": "single",
		"sold_in_shops": true,
		"category": "status_cure"
	},
	"eye_drops": {
		"name": "Eye Drops",
		"description": "Cures blindness.",
		"price": 30,
		"sell_price": 15,
		"effect": "cure_status",
		"value": "blind",
		"target": "single",
		"sold_in_shops": true,
		"category": "status_cure"
	},
	"echo_herb": {
		"name": "Echo Herb",
		"description": "Cures silence.",
		"price": 30,
		"sell_price": 15,
		"effect": "cure_status",
		"value": "silence",
		"target": "single",
		"sold_in_shops": true,
		"category": "status_cure"
	},
	"soft": {
		"name": "Soft",
		"description": "Cures paralysis.",
		"price": 80,
		"sell_price": 40,
		"effect": "cure_status",
		"value": "paralysis",
		"target": "single",
		"sold_in_shops": true,
		"category": "status_cure"
	},
	"dream_powder": {
		"name": "Dream Powder",
		"description": "Cures sleep.",
		"price": 40,
		"sell_price": 20,
		"effect": "cure_status",
		"value": "sleep",
		"target": "single",
		"sold_in_shops": true,
		"category": "status_cure"
	},
	"smelling_salts": {
		"name": "Smelling Salts",
		"description": "Cures confusion.",
		"price": 40,
		"sell_price": 20,
		"effect": "cure_status",
		"value": "confuse",
		"target": "single",
		"sold_in_shops": true,
		"category": "status_cure"
	},
	"remedy": {
		"name": "Remedy",
		"description": "Cures all status ailments.",
		"price": 500,
		"sell_price": 250,
		"effect": "cure_all_status",
		"value": "all",
		"target": "single",
		"sold_in_shops": true,
		"category": "status_cure"
	},

	# --- Revive ---
	"phoenix_down": {
		"name": "Phoenix Down",
		"description": "Revives a fallen ally at 25% HP.",
		"price": 500,
		"sell_price": 250,
		"effect": "revive",
		"value": 0.25,
		"target": "single",
		"sold_in_shops": true,
		"category": "revive"
	},
	"mega_phoenix": {
		"name": "Mega Phoenix",
		"description": "Revives all fallen allies.",
		"price": 3000,
		"sell_price": 1500,
		"effect": "revive_all",
		"value": 0.25,
		"target": "all_allies",
		"sold_in_shops": false,
		"category": "revive"
	},

	# --- Battle Items ---
	"fire_bomb": {
		"name": "Fire Bomb",
		"description": "Deals fire damage to one enemy.",
		"price": 100,
		"sell_price": 50,
		"effect": "damage_element",
		"value": 200,
		"element": "fire",
		"target": "single_enemy",
		"sold_in_shops": true,
		"category": "battle"
	},
	"thunder_gem": {
		"name": "Thunder Gem",
		"description": "Deals thunder damage to all enemies.",
		"price": 300,
		"sell_price": 150,
		"effect": "damage_element",
		"value": 300,
		"element": "thunder",
		"target": "all_enemies",
		"sold_in_shops": true,
		"category": "battle"
	},
	"earth_crystal": {
		"name": "Earth Crystal",
		"description": "Deals earth damage to all enemies.",
		"price": 300,
		"sell_price": 150,
		"effect": "damage_element",
		"value": 300,
		"element": "earth",
		"target": "all_enemies",
		"sold_in_shops": true,
		"category": "battle"
	},
	"holy_water": {
		"name": "Holy Water",
		"description": "Deals water damage to one enemy and cures burn.",
		"price": 80,
		"sell_price": 40,
		"effect": "damage_and_cure_status",
		"value": 150,
		"element": "water",
		"cure_status": "burn",
		"target": "single_enemy",
		"sold_in_shops": true,
		"category": "battle"
	},
	"darkness_shard": {
		"name": "Darkness Shard",
		"description": "Deals dark damage to one enemy.",
		"price": 150,
		"sell_price": 75,
		"effect": "damage_element",
		"value": 250,
		"element": "dark",
		"target": "single_enemy",
		"sold_in_shops": true,
		"category": "battle"
	},

	# --- Special ---
	"bubble_flask": {
		"name": "Bubble Flask",
		"description": "Applies Bubble status to an ally, doubling their max HP.",
		"price": 200,
		"sell_price": 100,
		"effect": "apply_status",
		"value": "bubble",
		"target": "single",
		"sold_in_shops": true,
		"category": "special"
	},
	"haste_tonic": {
		"name": "Haste Tonic",
		"description": "Applies Haste to an ally, increasing their action speed.",
		"price": 400,
		"sell_price": 200,
		"effect": "apply_status",
		"value": "haste",
		"target": "single",
		"sold_in_shops": true,
		"category": "special"
	},
	"iron_shield_pill": {
		"name": "Iron Shield Pill",
		"description": "Halves the next physical damage taken by an ally.",
		"price": 200,
		"sell_price": 100,
		"effect": "apply_status",
		"value": "iron_shield",
		"target": "single",
		"sold_in_shops": true,
		"category": "special"
	},

	# --- Rare / Key-Adjacent (not sold) ---
	"dragons_blood": {
		"name": "Dragon's Blood",
		"description": "A vial of ancient draconic ichor. Revives a fallen ally to full HP.",
		"price": 0,
		"sell_price": 0,
		"effect": "revive_full_hp",
		"value": 1.0,
		"target": "single",
		"sold_in_shops": false,
		"obtain_note": "Rare drop from Baby Dragon (rage state only)",
		"category": "rare"
	},
	"void_essence": {
		"name": "Void Essence",
		"description": "A fragment of nothingness. Deals 9999 psychic damage to all enemies.",
		"price": 0,
		"sell_price": 0,
		"effect": "damage_fixed",
		"value": 9999,
		"element": "psychic",
		"target": "all_enemies",
		"sold_in_shops": false,
		"obtain_note": "Found in final dungeon only",
		"category": "rare"
	},

	# --- Misc ---
	"tent": {
		"name": "Tent",
		"description": "Sets up camp at a save point. Fully restores HP and MP for all allies.",
		"price": 500,
		"sell_price": 250,
		"effect": "full_restore_all",
		"value": 0,
		"target": "all_allies",
		"sold_in_shops": true,
		"use_restriction": "save_point_only",
		"category": "misc"
	},
}

static func get_item(item_id: String) -> Dictionary:
	return ITEMS.get(item_id, {})

static func get_all_items() -> Dictionary:
	return ITEMS

static func get_purchasable() -> Array:
	var result: Array = []
	for item_id in ITEMS:
		if ITEMS[item_id].get("sold_in_shops", false):
			result.append(item_id)
	return result

static func get_by_category(category: String) -> Array:
	var result: Array = []
	for item_id in ITEMS:
		if ITEMS[item_id].get("category", "") == category:
			result.append(item_id)
	return result

static func has_item(item_id: String) -> bool:
	return ITEMS.has(item_id)
