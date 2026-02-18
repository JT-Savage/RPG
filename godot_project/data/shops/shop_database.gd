class_name ShopDatabase

const SHOPS: Dictionary = {
	"kobold_village_shop": {
		"name": "Survivor's Supplies",
		"shop_keeper_npc": "kobold_merchant",
		"flavor_text": "\"We don't have much, but what we have won't kill you. Probably.\"",
		"location": "kobold_village",
		"access_requirement": "",
		"items": [
			"potion",
			"antidote",
			"eye_drops",
			"echo_herb",
			"tent"
		],
		"equipment": []
	},

	"imperial_city_market": {
		"name": "Imperial Bazaar",
		"shop_keeper_npc": "imperial_merchant",
		"flavor_text": "\"Quality goods at quality prices. The Empire demands nothing less.\"",
		"location": "imperial_city",
		"access_requirement": "",
		"items": [
			"potion",
			"hi_potion",
			"ether",
			"antidote",
			"eye_drops",
			"echo_herb",
			"soft",
			"dream_powder",
			"smelling_salts",
			"phoenix_down",
			"fire_bomb",
			"tent"
		],
		"equipment": [
			"iron_sword",
			"short_bow",
			"wooden_staff",
			"leather_armor",
			"chain_mail",
			"mage_robe"
		]
	},

	"imperial_city_black_market": {
		"name": "The Unmarked Door",
		"shop_keeper_npc": "black_market_fence",
		"flavor_text": "\"You've got the seal. I've got the goods. Let's not complicate it.\"",
		"location": "imperial_city",
		"access_requirement": "empire_seal",
		"items": [
			"hi_potion",
			"mega_potion",
			"hi_ether",
			"remedy",
			"phoenix_down",
			"mega_phoenix",
			"haste_tonic",
			"bubble_flask",
			"iron_shield_pill",
			"darkness_shard",
			"thunder_gem",
			"earth_crystal"
		],
		"equipment": [
			"steel_sword",
			"battle_axe",
			"silver_staff",
			"plate_armor",
			"mage_coat"
		]
	},

	"swamp_village_herbalist": {
		"name": "Mirefoot Remedies",
		"shop_keeper_npc": "swamp_herbalist",
		"flavor_text": "\"The swamp provides. You just have to know where not to step.\"",
		"location": "swamp_village",
		"access_requirement": "",
		"items": [
			"antidote",
			"soft",
			"dream_powder",
			"smelling_salts",
			"echo_herb",
			"holy_water",
			"swamp_root"
		],
		"equipment": []
	},

	"mountain_pass_trader": {
		"name": "Highrock Trading Post",
		"shop_keeper_npc": "mountain_trader",
		"flavor_text": "\"Wind's bad today. Buy something and move along.\"",
		"location": "mountain_pass",
		"access_requirement": "",
		"items": [
			"potion",
			"hi_potion",
			"antidote",
			"echo_herb",
			"phoenix_down",
			"bubble_flask",
			"haste_tonic",
			"iron_shield_pill",
			"tent"
		],
		"equipment": []
	},

	"catacomb_merchant": {
		"name": "Bones & Bargains",
		"shop_keeper_npc": "skeleton_merchant",
		"flavor_text": "\"Ah, a living customer. How... refreshing. The eye drops are half-off. You'll need them down here. Trust me.\"",
		"location": "catacomb_entrance",
		"access_requirement": "",
		"items": [
			"eye_drops",
			"echo_herb",
			"soft",
			"phoenix_down"
		],
		"equipment": [],
		"price_modifiers": {
			"phoenix_down": 1.5
		},
		"notes": "Skeleton merchant NPC with dark humor dialogue. Phoenix Down is overpriced (1.5x base price). He finds this extremely funny."
	},

	"floating_island_shop": {
		"name": "Above the Clouds Emporium",
		"shop_keeper_npc": "island_shopkeeper",
		"flavor_text": "\"Not many make it up here. Fewer make it back down. No refunds, obviously.\"",
		"location": "floating_island",
		"access_requirement": "",
		"items": [
			"hi_potion",
			"mega_potion",
			"hi_ether",
			"remedy",
			"phoenix_down",
			"thunder_gem",
			"earth_crystal",
			"holy_water",
			"bubble_flask",
			"haste_tonic"
		],
		"equipment": [
			"crystal_wand",
			"wind_bow",
			"spirit_armor",
			"enchanted_robe"
		]
	},

	"final_dungeon_vendor": {
		"name": "The Last Merchant",
		"shop_keeper_npc": "mysterious_vendor",
		"flavor_text": "\"You've come this far. You might as well be prepared for what's ahead. I accept gold. I don't know why.\"",
		"location": "final_dungeon",
		"access_requirement": "",
		"items": [
			"elixir",
			"mega_phoenix",
			"void_essence",
			"mega_potion",
			"hi_ether",
			"remedy",
			"haste_tonic",
			"iron_shield_pill"
		],
		"equipment": [
			"void_blade",
			"ultima_staff",
			"sacred_armor"
		],
		"price_modifiers": {
			"elixir": 2.0,
			"mega_phoenix": 2.0,
			"void_essence": 3.0,
			"void_blade": 2.0,
			"ultima_staff": 2.0,
			"sacred_armor": 2.0
		},
		"notes": "Mysterious vendor in the final dungeon. Rare and endgame items are heavily marked up. Elixir and Mega Phoenix are sold here despite normally not being sold in shops — this is the one exception."
	},
}

static func get_shop(shop_id: String) -> Dictionary:
	return SHOPS.get(shop_id, {})

static func get_shop_items(shop_id: String) -> Array:
	var shop: Dictionary = SHOPS.get(shop_id, {})
	return shop.get("items", [])

static func get_shop_equipment(shop_id: String) -> Array:
	var shop: Dictionary = SHOPS.get(shop_id, {})
	return shop.get("equipment", [])

static func get_all_shops() -> Dictionary:
	return SHOPS

static func get_shops_in_location(location_id: String) -> Array:
	var result: Array = []
	for shop_id in SHOPS:
		if SHOPS[shop_id].get("location", "") == location_id:
			result.append(shop_id)
	return result

static func get_accessible_shops(player_key_items: Array) -> Array:
	var result: Array = []
	for shop_id in SHOPS:
		var req: String = SHOPS[shop_id].get("access_requirement", "")
		if req == "" or req in player_key_items:
			result.append(shop_id)
	return result

static func get_item_price(shop_id: String, item_id: String, base_price: int) -> int:
	var shop: Dictionary = SHOPS.get(shop_id, {})
	var modifiers: Dictionary = shop.get("price_modifiers", {})
	if modifiers.has(item_id):
		return int(base_price * modifiers[item_id])
	return base_price

static func has_shop(shop_id: String) -> bool:
	return SHOPS.has(shop_id)
