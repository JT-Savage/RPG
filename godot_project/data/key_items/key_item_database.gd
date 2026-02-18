class_name KeyItemDatabase

const KEY_ITEMS: Dictionary = {
	"baby_dragon_egg": {
		"name": "Baby Dragon Egg",
		"description": "A warm, pulsing egg. Something moves inside.",
		"obtained_from": "tutorial_warren_chest",
		"lore": "Hatches into the Baby Dragon party member after the tutorial sequence.",
		"sellable": false,
		"droppable": false
	},
	"holy_symbol": {
		"name": "Holy Symbol",
		"description": "A sacred medallion radiating faint warmth. Yipp would recognize this.",
		"obtained_from": "variable_dungeon_yipp_path",
		"lore": "Placement determined by which of three possible dungeons Yipp's spawn is seeded to. Required to recruit Yipp.",
		"sellable": false,
		"droppable": false
	},
	"wine_glass": {
		"name": "Wine Glass",
		"description": "An elegant crystal glass, inexplicably unbroken. Yipp will know what to do with it.",
		"obtained_from": "variable_dungeon_yipp_path",
		"lore": "Placed in the alternate dungeon from the holy_symbol, determined by Yipp's spawn seed. Required to recruit Yipp.",
		"sellable": false,
		"droppable": false
	},
	"orisia_invitation": {
		"name": "Orisia's Invitation",
		"description": "A hand-written letter sealed with a silver crescent. It smells faintly of the sea.",
		"obtained_from": "orisia_island",
		"lore": "Given directly by Orisia. Story item that advances her recruitment questline.",
		"sellable": false,
		"droppable": false
	},
	"empire_seal": {
		"name": "Empire Seal",
		"description": "The Emperor's personal signet. Doors that were closed to you are now very much open.",
		"obtained_from": "emperor_confrontation_cutscene",
		"lore": "Taken from the Emperor during the story confrontation. Grants access to all Imperial restricted areas and the black market.",
		"sellable": false,
		"droppable": false
	},
	"catacomb_key": {
		"name": "Catacomb Key",
		"description": "A heavy iron key crusted with old grave-moss. It fits the locked door deeper in.",
		"obtained_from": "catacomb_entrance",
		"lore": "Found in the catacomb_entrance area. Opens the locked door leading to catacomb_depths.",
		"sellable": false,
		"droppable": false
	},
	"dreamwalker_crystal": {
		"name": "Dreamwalker's Crystal",
		"description": "A cloudy gemstone that pulses with slow, dreaming light. It holds someone's focus.",
		"obtained_from": "dreamwalker_boss_drop",
		"lore": "The Dreamwalker's personal focus item. Dropped only if the Dreamwalker is defeated rather than recruited. May have alternate uses.",
		"sellable": false,
		"droppable": false
	},
	"swamp_root": {
		"name": "Swamp Root",
		"description": "A gnarled root reeking of the deep marsh. The druidess is looking for this.",
		"obtained_from": "swamp_village",
		"lore": "An ingredient required for the Druidess's sidequest. Found in the swamp_village area.",
		"sellable": false,
		"droppable": false
	},
	"mountain_herb": {
		"name": "Mountain Herb",
		"description": "A sprig of pale herb clinging to the cold rocks. The healer in the swamp will want this.",
		"obtained_from": "mountain_pass",
		"lore": "Found in mountain_pass. An ingredient requested by the healer NPC in swamp_village.",
		"sellable": false,
		"droppable": false
	},
	"vampire_coffin_key": {
		"name": "Vampire's Coffin Key",
		"description": "An ornate silver key etched with bats and roses. It opens something very old.",
		"obtained_from": "floating_island_chest",
		"lore": "Found in a chest on the floating_island. Opens the Vampire's sealed coffin and unlocks the dungeon leading to the Vampire boss/recruit.",
		"sellable": false,
		"droppable": false
	},
	"jerod_detonator": {
		"name": "Jerod's Detonator",
		"description": "A battered brass trigger mechanism. Jerod built it. You do not want to press it.",
		"obtained_from": "story_event_jerod",
		"lore": "Story item belonging to Jerod. Automatically used during the scripted cutscene. Cannot be manually activated.",
		"sellable": false,
		"droppable": false,
		"auto_use": true
	},
	"flood_amulet": {
		"name": "Flood's Amulet",
		"description": "A simple carved amulet that belonged to Hannah. The stone is still warm.",
		"obtained_from": "flood_death_event",
		"lore": "Hannah's personal amulet. Becomes a permanent plot item after Flood's death cutscene. A reminder of what was lost.",
		"sellable": false,
		"droppable": false,
		"permanent": true
	},
	"ng_plus_crown": {
		"name": "Crown of the Twice-Born",
		"description": "A crown awarded to those who have conquered all and begun again. Proof of mastery.",
		"obtained_from": "ng_plus_completion_reward",
		"lore": "Awarded upon completing a New Game Plus run. Displayed in the inventory as proof of completion.",
		"sellable": false,
		"droppable": false
	},
	"class_crystal_warrior": {
		"name": "Warrior's Class Crystal",
		"description": "A shard of hardened resolve, resonating with Michael's potential.",
		"obtained_from": "orisia_sidequest_completion",
		"lore": "Unlocks the Warrior class evolution for Michael. Obtained by completing Orisia's sidequest.",
		"sellable": false,
		"droppable": false,
		"unlocks_class": "warrior",
		"character": "michael"
	},
	"class_crystal_saint": {
		"name": "Saint's Class Crystal",
		"description": "A luminous fragment humming with holy light, attuned to Hannah's spirit.",
		"obtained_from": "hannah_class_quest",
		"lore": "Unlocks the Saint class evolution for Hannah.",
		"sellable": false,
		"droppable": false,
		"unlocks_class": "saint",
		"character": "hannah"
	},
	"class_crystal_druid": {
		"name": "Druid's Class Crystal",
		"description": "A rough stone threaded with living roots, resonating with the Druidess.",
		"obtained_from": "druidess_class_quest",
		"lore": "Unlocks the Druid class evolution for the Druidess.",
		"sellable": false,
		"droppable": false,
		"unlocks_class": "druid",
		"character": "druidess"
	},
	"class_crystal_vampire_lord": {
		"name": "Vampire Lord's Class Crystal",
		"description": "A dark shard pulsing with ancient blood-power.",
		"obtained_from": "vampire_class_quest",
		"lore": "Unlocks the Vampire Lord class evolution for the Vampire.",
		"sellable": false,
		"droppable": false,
		"unlocks_class": "vampire_lord",
		"character": "vampire"
	},
	"class_crystal_shapeshifter": {
		"name": "Shapeshifter's Class Crystal",
		"description": "A mercurial gem that shifts color when you look away. It belongs to Iris.",
		"obtained_from": "iris_class_quest",
		"lore": "Unlocks the Shapeshifter class evolution for Iris.",
		"sellable": false,
		"droppable": false,
		"unlocks_class": "shapeshifter",
		"character": "iris"
	},
	"class_crystal_paladin": {
		"name": "Paladin's Class Crystal",
		"description": "A crystal carved into a shield motif, emanating calm strength attuned to Kella.",
		"obtained_from": "kella_class_quest",
		"lore": "Unlocks the Paladin class evolution for Kella.",
		"sellable": false,
		"droppable": false,
		"unlocks_class": "paladin",
		"character": "kella"
	},
	"class_crystal_dreamweaver": {
		"name": "Dreamweaver's Class Crystal",
		"description": "A translucent shard that seems to contain a moving landscape within.",
		"obtained_from": "dreamwalker_class_quest",
		"lore": "Unlocks the Dreamweaver class evolution for the Dreamwalker.",
		"sellable": false,
		"droppable": false,
		"unlocks_class": "dreamweaver",
		"character": "dreamwalker"
	},
	"ultimate_weapon_kella": {
		"name": "Kella's Oath-Shield",
		"description": "A legendary tower shield said to have never once broken. It never will.",
		"obtained_from": "orisia_sidequest_completion",
		"lore": "Kella's ultimate weapon. Awarded for completing the Orisia sidequest.",
		"sellable": false,
		"droppable": false,
		"character": "kella",
		"equipment_id": "oath_shield_kella"
	},
	"ultimate_weapon_michael": {
		"name": "Michael's Resolute Blade",
		"description": "A sword that has seen a hundred battles and remembers every one.",
		"obtained_from": "michael_ultimate_quest",
		"lore": "Michael's ultimate weapon.",
		"sellable": false,
		"droppable": false,
		"character": "michael",
		"equipment_id": "resolute_blade_michael"
	},
	"ultimate_weapon_hannah": {
		"name": "Hannah's Tidecaller Staff",
		"description": "A staff carved from driftwood, still wet from the sea that gave her power.",
		"obtained_from": "hannah_ultimate_quest",
		"lore": "Hannah's ultimate weapon.",
		"sellable": false,
		"droppable": false,
		"character": "hannah",
		"equipment_id": "tidecaller_staff_hannah"
	},
	"ultimate_weapon_fei": {
		"name": "Fei's Twin Fang Blades",
		"description": "Two blades that move like a single thought. They were waiting for her.",
		"obtained_from": "fei_ultimate_quest",
		"lore": "Fei's ultimate weapon.",
		"sellable": false,
		"droppable": false,
		"character": "fei",
		"equipment_id": "twin_fang_fei"
	},
	"panda_plushie": {
		"name": "Panda Plushie",
		"description": "A battered stuffed panda with one button eye. Iris will not go anywhere without it.",
		"obtained_from": "army_camp_chest",
		"lore": "Iris's Shapeshifter totem. Found in the army_camp chest. Required for Iris's Shapeshifter class abilities to function at full power.",
		"sellable": false,
		"droppable": false,
		"character": "iris"
	},
	"baby_dragon_name_tag": {
		"name": "Baby Dragon's Name Tag",
		"description": "A small carved tag with a name on it. The Baby Dragon wears it proudly.",
		"obtained_from": "kobold_village",
		"lore": "A personalized name tag for the Baby Dragon, given to the player during a story event in kobold_village. The name is set by the player.",
		"sellable": false,
		"droppable": false,
		"player_named": true,
		"character": "baby_dragon"
	},
}

static func get_key_item(item_id: String) -> Dictionary:
	return KEY_ITEMS.get(item_id, {})

static func get_all_key_items() -> Dictionary:
	return KEY_ITEMS

static func has_key_item(item_id: String) -> bool:
	return KEY_ITEMS.has(item_id)

static func get_key_items_for_character(character_id: String) -> Array:
	var result: Array = []
	for item_id in KEY_ITEMS:
		if KEY_ITEMS[item_id].get("character", "") == character_id:
			result.append(item_id)
	return result

static func get_class_crystals() -> Array:
	var result: Array = []
	for item_id in KEY_ITEMS:
		if item_id.begins_with("class_crystal_"):
			result.append(item_id)
	return result

static func get_ultimate_weapons() -> Array:
	var result: Array = []
	for item_id in KEY_ITEMS:
		if item_id.begins_with("ultimate_weapon_"):
			result.append(item_id)
	return result
