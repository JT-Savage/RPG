## equipment_database.gd
## Static equipment data for "There Will Be Kobolds"
## Contains all weapons, armor, shields, and accessories.
class_name EquipmentDatabase


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

## Returns a Dictionary with full stats for the given equipment id.
## Returns an empty Dictionary if the id is not found.
static func get_equipment(id: String) -> Dictionary:
	var db := _build_equipment_db()
	if db.has(id):
		return db[id]
	push_warning("EquipmentDatabase: unknown equipment id '%s'" % id)
	return {}


## Returns an Array of equipment id Strings that the given class can equip.
## class_name_param should match the "classes" lists in the database.
static func get_equipment_for_class(class_name_param: String) -> Array:
	var db  := _build_equipment_db()
	var out : Array = []
	for id in db:
		var entry : Dictionary = db[id]
		if entry.has("classes") and class_name_param in entry["classes"]:
			out.append(id)
	return out


# ---------------------------------------------------------------------------
# Equipment database builder
# ---------------------------------------------------------------------------

static func _build_equipment_db() -> Dictionary:
	return {

		# ===================================================================
		# WEAPONS
		# ===================================================================

		# -------------------------------------------------------------------
		# Daggers  — usable by Javin
		# -------------------------------------------------------------------

		"iron_dagger": {
			"id": "iron_dagger",
			"name": "Iron Dagger",
			"slot": "weapon",
			"weapon_type": "dagger",
			"classes": ["javin"],
			"atk": 15,
			"description": "A simple iron dagger. Reliable if unspectacular.",
		},

		"silver_dagger": {
			"id": "silver_dagger",
			"name": "Silver Dagger",
			"slot": "weapon",
			"weapon_type": "dagger",
			"classes": ["javin"],
			"atk": 25,
			"element": "light",
			"description": "A silver-bladed dagger imbued with faint holy light.",
		},

		"shadow_blade": {
			"id": "shadow_blade",
			"name": "Shadow Blade",
			"slot": "weapon",
			"weapon_type": "dagger",
			"classes": ["javin"],
			"atk": 40,
			"element": "darkness",
			"description": "A blade that drinks in shadow, striking from blind spots.",
		},

		"void_shard": {
			"id": "void_shard",
			"name": "Void Shard",
			"slot": "weapon",
			"weapon_type": "dagger",
			"classes": ["javin"],
			"atk": 60,
			"element": "darkness",
			"best_in_slot_region": "desert",
			"description": "A crystallised fragment of void energy. Javin's best-in-slot dagger in the desert region.",
		},

		# -------------------------------------------------------------------
		# Shotguns  — usable by Frostbite
		# -------------------------------------------------------------------

		"standard_shotgun": {
			"id": "standard_shotgun",
			"name": "Standard Shotgun",
			"slot": "weapon",
			"weapon_type": "shotgun",
			"classes": ["frostbite"],
			"atk": 30,
			"description": "A dependable scatter-shot firearm.",
		},

		"enhanced_shotgun": {
			"id": "enhanced_shotgun",
			"name": "Enhanced Shotgun",
			"slot": "weapon",
			"weapon_type": "shotgun",
			"classes": ["frostbite"],
			"atk": 50,
			"description": "A modified shotgun with improved spread and stopping power.",
		},

		"ultimate_shotgun": {
			"id": "ultimate_shotgun",
			"name": "Ultimate Shotgun",
			"slot": "weapon",
			"weapon_type": "shotgun",
			"classes": ["frostbite"],
			"atk": 80,
			"double_attack": true,
			"level_cap_increase": true,
			"is_key_reward": true,
			"description": "Frostbite's definitive armament. Fires twice per attack and raises her level cap. A KEY story reward.",
		},

		# -------------------------------------------------------------------
		# Sniper Rifles  — usable by Fritzzit
		# -------------------------------------------------------------------

		"standard_sniper": {
			"id": "standard_sniper",
			"name": "Standard Sniper Rifle",
			"slot": "weapon",
			"weapon_type": "sniper_rifle",
			"classes": ["fritzzit"],
			"atk": 28,
			"crit_bonus": 10,
			"description": "A reliable long-range rifle. +10% critical hit chance.",
		},

		"enhanced_sniper": {
			"id": "enhanced_sniper",
			"name": "Enhanced Sniper Rifle",
			"slot": "weapon",
			"weapon_type": "sniper_rifle",
			"classes": ["fritzzit"],
			"atk": 48,
			"crit_bonus": 15,
			"description": "A precision-tuned sniper rifle. +15% critical hit chance.",
		},

		"ultimate_sniper_rifle": {
			"id": "ultimate_sniper_rifle",
			"name": "Ultimate Sniper Rifle",
			"slot": "weapon",
			"weapon_type": "sniper_rifle",
			"classes": ["fritzzit"],
			"atk": 75,
			"crit_bonus": 25,
			"instakill_on_crit_nonboss": true,
			"is_key_reward": true,
			"description": "Fritzzit's masterwork. +25% crit; critical hits instantly kill non-boss enemies. A KEY story reward.",
		},

		# -------------------------------------------------------------------
		# Swords  — usable by Fei, Michael, Warghoul
		# -------------------------------------------------------------------

		"iron_sword": {
			"id": "iron_sword",
			"name": "Iron Sword",
			"slot": "weapon",
			"weapon_type": "sword",
			"classes": ["fei", "michael", "warghoul"],
			"atk": 22,
			"description": "A sturdy iron sword suited to warriors of all stripes.",
		},

		"flame_sword": {
			"id": "flame_sword",
			"name": "Flame Sword",
			"slot": "weapon",
			"weapon_type": "sword",
			"classes": ["fei", "michael", "warghoul"],
			"atk": 35,
			"element": "fire",
			"description": "A blade wreathed in fire. Deals fire elemental damage.",
		},

		"holy_blade": {
			"id": "holy_blade",
			"name": "Holy Blade",
			"slot": "weapon",
			"weapon_type": "sword",
			"classes": ["fei", "michael", "warghoul"],
			"atk": 55,
			"element": "light",
			"bonus_vs_undead": true,
			"description": "A blade blessed with sacred light. Extra effective against undead.",
		},

		"void_reaper": {
			"id": "void_reaper",
			"name": "Void Reaper",
			"slot": "weapon",
			"weapon_type": "sword",
			"classes": ["fei", "michael", "warghoul"],
			"atk": 70,
			"element": "darkness",
			"description": "A greatsword torn from the void itself. Strikes with pure darkness.",
		},

		# -------------------------------------------------------------------
		# Axes  — usable by Fei, Warghoul
		# -------------------------------------------------------------------

		"battle_axe": {
			"id": "battle_axe",
			"name": "Battle Axe",
			"slot": "weapon",
			"weapon_type": "axe",
			"classes": ["fei", "warghoul"],
			"atk": 28,
			"description": "A heavy single-bladed axe favoured by brute-force fighters.",
		},

		"war_axe": {
			"id": "war_axe",
			"name": "War Axe",
			"slot": "weapon",
			"weapon_type": "axe",
			"classes": ["fei", "warghoul"],
			"atk": 45,
			"description": "A massive double-headed war axe capable of cleaving armour.",
		},

		# -------------------------------------------------------------------
		# Staves  — usable by Flood, Hannah, Michael, Cookie, Yipp, Crankpot
		# -------------------------------------------------------------------

		"oak_staff": {
			"id": "oak_staff",
			"name": "Oak Staff",
			"slot": "weapon",
			"weapon_type": "staff",
			"classes": ["flood", "hannah", "michael", "cookie", "yipp", "crankpot"],
			"atk": 10,
			"mag": 15,
			"description": "A gnarled oak staff that channels basic magical energies.",
		},

		"crystal_staff": {
			"id": "crystal_staff",
			"name": "Crystal Staff",
			"slot": "weapon",
			"weapon_type": "staff",
			"classes": ["flood", "hannah", "michael", "cookie", "yipp", "crankpot"],
			"atk": 15,
			"mag": 28,
			"description": "A staff capped with a resonant crystal, amplifying spell power.",
		},

		"arcane_staff": {
			"id": "arcane_staff",
			"name": "Arcane Staff",
			"slot": "weapon",
			"weapon_type": "staff",
			"classes": ["flood", "hannah", "michael", "cookie", "yipp", "crankpot"],
			"atk": 20,
			"mag": 45,
			"description": "A staff humming with condensed arcane energy.",
		},

		"void_staff": {
			"id": "void_staff",
			"name": "Void Staff",
			"slot": "weapon",
			"weapon_type": "staff",
			"classes": ["flood", "hannah", "michael", "cookie", "yipp", "crankpot"],
			"atk": 25,
			"mag": 60,
			"best_in_slot_region": "desert",
			"description": "A staff threaded with void energy. Best-in-slot staff in the desert region.",
		},

		# -------------------------------------------------------------------
		# Wands  — usable by Cookie, Crankpot, Yipp
		# -------------------------------------------------------------------

		"flame_wand": {
			"id": "flame_wand",
			"name": "Flame Wand",
			"slot": "weapon",
			"weapon_type": "wand",
			"classes": ["cookie", "crankpot", "yipp"],
			"mag": 20,
			"fire_bonus": 15,
			"description": "A wand attuned to fire. +15% fire spell potency.",
		},

		"thunder_wand": {
			"id": "thunder_wand",
			"name": "Thunder Wand",
			"slot": "weapon",
			"weapon_type": "wand",
			"classes": ["cookie", "crankpot", "yipp"],
			"mag": 20,
			"thunder_bonus": 15,
			"description": "A wand attuned to lightning. +15% thunder spell potency.",
		},

		"nature_wand": {
			"id": "nature_wand",
			"name": "Nature Wand",
			"slot": "weapon",
			"weapon_type": "wand",
			"classes": ["cookie", "crankpot", "yipp"],
			"mag": 22,
			"earth_bonus": 15,
			"description": "A wand grown from living wood. +15% earth spell potency.",
		},

		# -------------------------------------------------------------------
		# Maces  — usable by Michael
		# -------------------------------------------------------------------

		"iron_mace": {
			"id": "iron_mace",
			"name": "Iron Mace",
			"slot": "weapon",
			"weapon_type": "mace",
			"classes": ["michael"],
			"atk": 20,
			"mag": 10,
			"description": "A blunt iron mace that still channels modest holy energy.",
		},

		"blessed_mace": {
			"id": "blessed_mace",
			"name": "Blessed Mace",
			"slot": "weapon",
			"weapon_type": "mace",
			"classes": ["michael"],
			"atk": 30,
			"mag": 20,
			"holy_bonus": 10,
			"description": "A mace consecrated by a priest. +10% holy spell potency.",
		},

		# ===================================================================
		# ARMOR
		# ===================================================================

		# -------------------------------------------------------------------
		# Light Armor
		# -------------------------------------------------------------------

		"leather_armor": {
			"id": "leather_armor",
			"name": "Leather Armor",
			"slot": "body",
			"armor_type": "light",
			"def": 10,
			"description": "Basic tanned leather armour. Light and easy to move in.",
		},

		"studded_leather": {
			"id": "studded_leather",
			"name": "Studded Leather",
			"slot": "body",
			"armor_type": "light",
			"def": 18,
			"description": "Leather reinforced with iron studs for improved protection.",
		},

		"shadow_cloak": {
			"id": "shadow_cloak",
			"name": "Shadow Cloak",
			"slot": "body",
			"armor_type": "light",
			"def": 25,
			"evasion_bonus": 5,
			"description": "A cloak woven from shadow-silk. +5% evasion.",
		},

		# -------------------------------------------------------------------
		# Medium Armor
		# -------------------------------------------------------------------

		"chainmail": {
			"id": "chainmail",
			"name": "Chainmail",
			"slot": "body",
			"armor_type": "medium",
			"def": 20,
			"description": "Interlocking rings of iron offering solid all-round protection.",
		},

		"reinforced_chain": {
			"id": "reinforced_chain",
			"name": "Reinforced Chain",
			"slot": "body",
			"armor_type": "medium",
			"def": 30,
			"description": "Chainmail with additional plate reinforcement at vital points.",
		},

		"desert_mail": {
			"id": "desert_mail",
			"name": "Desert Mail",
			"slot": "body",
			"armor_type": "medium",
			"def": 40,
			"best_in_slot_region": "desert",
			"description": "Sand-tempered chainmail that breathes in arid heat. Best-in-slot medium armour in the desert region.",
		},

		# -------------------------------------------------------------------
		# Heavy Armor
		# -------------------------------------------------------------------

		"plate_armor": {
			"id": "plate_armor",
			"name": "Plate Armor",
			"slot": "body",
			"armor_type": "heavy",
			"def": 35,
			"description": "Full-plate steel armour that turns aside most blows.",
		},

		"knight_plate": {
			"id": "knight_plate",
			"name": "Knight Plate",
			"slot": "body",
			"armor_type": "heavy",
			"def": 50,
			"description": "Master-forged knight's plate. Near-impenetrable by conventional weapons.",
		},

		# -------------------------------------------------------------------
		# Robes
		# -------------------------------------------------------------------

		"mage_robe": {
			"id": "mage_robe",
			"name": "Mage Robe",
			"slot": "body",
			"armor_type": "robe",
			"def": 5,
			"sp_res": 20,
			"description": "A lightweight robe that channels magical resistance.",
		},

		"arcane_robe": {
			"id": "arcane_robe",
			"name": "Arcane Robe",
			"slot": "body",
			"armor_type": "robe",
			"def": 8,
			"sp_res": 35,
			"mag": 10,
			"description": "Robe embroidered with arcane sigils. Boosts both spell resistance and magic power.",
		},

		"void_robe": {
			"id": "void_robe",
			"name": "Void Robe",
			"slot": "body",
			"armor_type": "robe",
			"def": 12,
			"sp_res": 50,
			"mag": 20,
			"best_in_slot_region": "desert",
			"description": "A robe threaded with void energy. Best-in-slot robe in the desert region.",
		},

		# ===================================================================
		# SHIELDS
		# ===================================================================

		"wooden_shield": {
			"id": "wooden_shield",
			"name": "Wooden Shield",
			"slot": "offhand",
			"equipment_type": "shield",
			"def": 8,
			"description": "A basic wooden buckler. Better than nothing.",
		},

		"iron_shield": {
			"id": "iron_shield",
			"name": "Iron Shield",
			"slot": "offhand",
			"equipment_type": "shield",
			"def": 15,
			"description": "A solid iron shield that deflects physical blows.",
		},

		"tower_shield": {
			"id": "tower_shield",
			"name": "Tower Shield",
			"slot": "offhand",
			"equipment_type": "shield",
			"def": 25,
			"enables_taunt": true,
			"description": "A full-body shield. Unlocks the Taunt ability, drawing enemy attention.",
		},

		# ===================================================================
		# ACCESSORIES
		# ===================================================================

		"fire_ring": {
			"id": "fire_ring",
			"name": "Fire Ring",
			"slot": "accessory",
			"fire_resistance": 30,
			"description": "A ring set with a fire opal. +30% fire resistance.",
		},

		"thunder_ring": {
			"id": "thunder_ring",
			"name": "Thunder Ring",
			"slot": "accessory",
			"thunder_resistance": 30,
			"description": "A ring set with a static gem. +30% thunder resistance.",
		},

		"anti_poison": {
			"id": "anti_poison",
			"name": "Antidote Charm",
			"slot": "accessory",
			"poison_immune": true,
			"description": "A charm soaked in antitoxin. Grants immunity to poison.",
		},

		"speed_boots": {
			"id": "speed_boots",
			"name": "Speed Boots",
			"slot": "accessory",
			"speed": 5,
			"description": "Enchanted boots that quicken the wearer's step. +5 Speed.",
		},

		"crit_pendant": {
			"id": "crit_pendant",
			"name": "Crit Pendant",
			"slot": "accessory",
			"crit_bonus": 10,
			"description": "A pendant that sharpens focus in battle. +10% critical hit chance.",
		},

		"mana_crystal": {
			"id": "mana_crystal",
			"name": "Mana Crystal",
			"slot": "accessory",
			"mp_percent_bonus": 20,
			"description": "A resonant crystal that expands magical reserves. +20% max MP.",
		},

		"dragon_scale_amulet": {
			"id": "dragon_scale_amulet",
			"name": "Dragon Scale Amulet",
			"slot": "accessory",
			"all_element_resistance": 15,
			"description": "An amulet fashioned from a true dragon's scale. +15% resistance to all elements.",
		},

		# ===================================================================
		# KEY EQUIPMENT  (story-flagged)
		# ===================================================================

		"baby_dragon": {
			"id": "baby_dragon",
			"name": "Baby Dragon",
			"slot": "special",
			"is_key_item": true,
			"classes": ["javin"],
			"restriction": "javin_only",
			"passive_effect": "fire_lv2_every_4_attacks",
			"description": "A tiny dragon companion that rides with Javin. Breathes fire every 4 attacks (Fire Lv2). Javin-exclusive special slot.",
		},

		"sentimental_traveler_pouch": {
			"id": "sentimental_traveler_pouch",
			"name": "Sentimental Traveler's Pouch",
			"slot": "accessory",
			"is_key_item": true,
			"is_story_item": true,
			"classes": ["michael"],
			"restriction": "michael_only",
			"hp": 30,
			"mp": 15,
			"description": "A worn pouch Michael has carried since his journey began. +30 HP, +15 MP. Michael-exclusive story accessory.",
		},

		# ===================================================================
		# SHOP-REFERENCED EQUIPMENT  (added to satisfy shop_database.gd)
		# ===================================================================

		# -------------------------------------------------------------------
		# Weapons — Bows  (early-mid game ranged, usable by Fritzzit)
		# -------------------------------------------------------------------

		"short_bow": {
			"id": "short_bow",
			"name": "Short Bow",
			"slot": "weapon",
			"weapon_type": "bow",
			"classes": ["fritzzit"],
			"atk": 18,
			"crit_bonus": 5,
			"description": "A compact wooden bow suited to quick, accurate shots. +5% critical hit chance.",
		},

		# -------------------------------------------------------------------
		# Weapons — Staves  (early-mid game magic, shared caster pool)
		# -------------------------------------------------------------------

		"wooden_staff": {
			"id": "wooden_staff",
			"name": "Wooden Staff",
			"slot": "weapon",
			"weapon_type": "staff",
			"classes": ["flood", "hannah", "michael", "cookie", "yipp", "crankpot"],
			"atk": 8,
			"mag": 10,
			"description": "A plain wooden staff. A reliable first choice for any budding caster.",
		},

		"silver_staff": {
			"id": "silver_staff",
			"name": "Silver Staff",
			"slot": "weapon",
			"weapon_type": "staff",
			"classes": ["flood", "hannah", "michael", "cookie", "yipp", "crankpot"],
			"atk": 18,
			"mag": 35,
			"element": "light",
			"description": "A staff capped with polished silver. Channels light-aligned magic with ease.",
		},

		# -------------------------------------------------------------------
		# Weapons — Swords  (mid game, shared sword users)
		# -------------------------------------------------------------------

		"steel_sword": {
			"id": "steel_sword",
			"name": "Steel Sword",
			"slot": "weapon",
			"weapon_type": "sword",
			"classes": ["fei", "michael", "warghoul"],
			"atk": 38,
			"description": "A well-balanced steel blade. A solid mid-game upgrade for any sword user.",
		},

		# -------------------------------------------------------------------
		# Weapons — Wands  (late game, floating island)
		# -------------------------------------------------------------------

		"crystal_wand": {
			"id": "crystal_wand",
			"name": "Crystal Wand",
			"slot": "weapon",
			"weapon_type": "wand",
			"classes": ["cookie", "crankpot", "yipp"],
			"mag": 50,
			"best_in_slot_region": "floating_island",
			"description": "A wand carved from a single resonant crystal. Dramatically amplifies spell output. Best-in-slot wand on the floating island.",
		},

		# -------------------------------------------------------------------
		# Weapons — Bows  (late game, floating island)
		# -------------------------------------------------------------------

		"wind_bow": {
			"id": "wind_bow",
			"name": "Wind Bow",
			"slot": "weapon",
			"weapon_type": "bow",
			"classes": ["fritzzit"],
			"atk": 65,
			"crit_bonus": 20,
			"element": "wind",
			"best_in_slot_region": "floating_island",
			"description": "A bow strung with condensed gale-force wind. Deals wind elemental damage. Best-in-slot bow on the floating island.",
		},

		# -------------------------------------------------------------------
		# Weapons — Final dungeon tier
		# -------------------------------------------------------------------

		"void_blade": {
			"id": "void_blade",
			"name": "Void Blade",
			"slot": "weapon",
			"weapon_type": "sword",
			"classes": ["fei", "michael", "warghoul"],
			"atk": 90,
			"element": "darkness",
			"description": "A sword forged from compressed void energy. The pinnacle of dark-aligned blades.",
		},

		"ultima_staff": {
			"id": "ultima_staff",
			"name": "Ultima Staff",
			"slot": "weapon",
			"weapon_type": "staff",
			"classes": ["flood", "hannah", "michael", "cookie", "yipp", "crankpot"],
			"atk": 35,
			"mag": 80,
			"description": "A staff radiating raw magical force. The mightiest staff available in the final dungeon.",
		},

		# -------------------------------------------------------------------
		# Armor — Medium  (early-mid game)
		# -------------------------------------------------------------------

		"chain_mail": {
			"id": "chain_mail",
			"name": "Chain Mail",
			"slot": "body",
			"armor_type": "medium",
			"def": 25,
			"description": "A coat of closely woven iron rings. Offers reliable protection without excessive weight.",
		},

		# -------------------------------------------------------------------
		# Armor — Robes / Light  (mid game, mage-oriented)
		# -------------------------------------------------------------------

		"mage_coat": {
			"id": "mage_coat",
			"name": "Mage Coat",
			"slot": "body",
			"armor_type": "robe",
			"def": 12,
			"sp_res": 28,
			"mag": 8,
			"classes": ["flood", "hannah", "michael", "cookie", "yipp", "crankpot"],
			"description": "A long coat lined with spell-dampening thread. Balances modest physical protection with useful magical resistance.",
		},

		# -------------------------------------------------------------------
		# Armor — Medium  (late game, floating island)
		# -------------------------------------------------------------------

		"spirit_armor": {
			"id": "spirit_armor",
			"name": "Spirit Armor",
			"slot": "body",
			"armor_type": "medium",
			"def": 45,
			"sp_res": 15,
			"best_in_slot_region": "floating_island",
			"description": "Armor imbued with ethereal energy. Provides strong physical and moderate magical defence. Best-in-slot medium armour on the floating island.",
		},

		# -------------------------------------------------------------------
		# Armor — Robe  (late game, floating island)
		# -------------------------------------------------------------------

		"enchanted_robe": {
			"id": "enchanted_robe",
			"name": "Enchanted Robe",
			"slot": "body",
			"armor_type": "robe",
			"def": 18,
			"sp_res": 55,
			"mag": 25,
			"best_in_slot_region": "floating_island",
			"classes": ["flood", "hannah", "michael", "cookie", "yipp", "crankpot"],
			"description": "A robe woven with active enchantments that deflect hostile spells. Best-in-slot robe on the floating island.",
		},

		# -------------------------------------------------------------------
		# Armor — Heavy  (final dungeon tier)
		# -------------------------------------------------------------------

		"sacred_armor": {
			"id": "sacred_armor",
			"name": "Sacred Armor",
			"slot": "body",
			"armor_type": "heavy",
			"def": 65,
			"sp_res": 20,
			"element_resistance_all": 10,
			"description": "Armor blessed by ancient rites. Grants outstanding physical defence and blanket elemental resistance.",
		},

	}