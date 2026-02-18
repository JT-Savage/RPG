extends Node
## BattleManager - ATB battle system, damage calculation, status effects, turn order

signal battle_started(enemy_formation: Array)
signal battle_ended(result: String)  # "victory" / "defeat" / "fled"
signal character_acted(char_id: String, action: Dictionary)
signal enemy_acted(enemy_index: int, action: Dictionary)
signal damage_dealt(target: Dictionary, damage: int, descriptor: String, element: String)
signal status_applied(target: Dictionary, status: String)
signal status_removed(target: Dictionary, status: String)
signal character_ko(char_id: String)
signal enemy_ko(enemy_index: int)
signal turn_ready(actor: Dictionary)  # {type: "character"/"enemy", id: String/int}

# Battle state
var in_battle := false
var current_enemies: Array = []
var battle_result := ""
var atb_active := true
var battle_background := "dungeon"

# ATB gauges: char_id/enemy_index -> float (0-100)
var atb_gauges: Dictionary = {}
var turn_queue: Array = []  # actors whose gauge hit 100, in order

# Active party snapshots for battle
var active_combatants: Array = []  # list of char_ids in battle

# Track accumulated battle EXP/Gil
var pending_exp := 0
var pending_gil := 0

# ===== ELEMENTS =====
enum Element { NONE, FIRE, WATER, EARTH, DARKNESS, LIGHT, THUNDER, PSYCHIC }

# ===== DAMAGE DESCRIPTORS =====
enum DamageType { PHYSICAL, MAGICAL, PSYCHIC }

# ===== STATUS EFFECTS =====
const STATUS_EFFECTS := {
	"poison": {"duration": -1, "dot_pct": 0.05, "ends_on_battle": true},
	"sleep": {"duration": -1, "ends_on_hit": true, "ends_on_battle": true},
	"paralysis": {"duration": -1, "ends_on_battle": true},
	"blind": {"acc_modifier": 0.4, "ends_on_battle": true},
	"silence": {"blocks_magic": true, "ends_on_battle": true},
	"slow": {"speed_modifier": 0.5, "ends_on_battle": true},
	"haste": {"speed_modifier": 1.75, "ends_on_battle": true},
	"berserk": {"atk_modifier": 1.5, "def_modifier": 0.75, "ai_controlled": true, "ends_on_battle": true},
	"confuse": {"ai_controlled": true, "can_hit_allies": true, "ends_on_battle": true},
	"burn": {"dot_flat": 15, "removed_by": "water", "ends_on_battle": true, "spread_chance": 0.0},
	"bubble": {"blocks_magic": true, "blocks_attack": true, "pops_on_hit": true, "ends_on_battle": true},
}

# ===== ELEMENTAL CHART =====
# multiplier[attack_element][defender_weakness/resist]
const ELEMENT_MULTIPLIERS := {
	"fire":      {"weakness": {"water": 0.5, "fire": 0.0}, "strong": {"fire": 2.0, "earth": 1.5}},
	"water":     {"weakness": {"fire": 0.5}, "strong": {"water": 2.0, "earth": 2.0}},
	"earth":     {"weakness": {"water": 0.5, "thunder": 0.5}, "strong": {"earth": 0.0}},
	"darkness":  {"strong": {"light": 2.0}, "weakness": {"darkness": 0.5}},
	"light":     {"strong": {"darkness": 2.0, "undead": 2.0}, "weakness": {"light": 0.5}},
	"thunder":   {"strong": {"water": 1.5}},
	"psychic":   {},  # Unresistable
}

func start_battle(enemy_formation: Array, background: String = "dungeon") -> void:
	in_battle = true
	battle_background = background
	current_enemies = []
	pending_exp = 0
	pending_gil = 0
	battle_result = ""

	# Copy enemies for battle
	for enemy_data in enemy_formation:
		var enemy := enemy_data.duplicate(true)
		enemy["current_hp"] = enemy["max_hp"]
		enemy["current_mp"] = enemy.get("max_mp", 0)
		enemy["status_effects"] = []
		enemy["atb_gauge"] = 0.0
		current_enemies.append(enemy)

	# Set up active combatants
	active_combatants = GameManager.active_party.duplicate()

	# Initialize ATB gauges
	atb_gauges.clear()
	turn_queue.clear()
	for char_id in active_combatants:
		atb_gauges[char_id] = randf() * 20.0  # Random start 0-20
	for i in range(current_enemies.size()):
		atb_gauges["enemy_%d" % i] = randf() * 10.0

	FlagManager.set_flag("fei_dead_in_battle", false)
	atb_active = true

	battle_started.emit(enemy_formation)
	AudioManager.play_music("battle")

func _process(delta: float) -> void:
	if not in_battle:
		return
	if not atb_active:
		return
	if GameManager.is_paused:
		return

	# ATB pause in menus
	if GameManager.atb_paused_in_menu and _is_menu_open():
		return

	# Fill ATB gauges
	for char_id in active_combatants:
		var char_state := PartyManager.get_character(char_id)
		if char_state.is_empty():
			continue
		if _is_ko(char_id):
			continue

		var speed_mod := _get_speed_modifier(char_id)
		var speed := char_state["stats"]["speed"] * speed_mod
		atb_gauges[char_id] = min(atb_gauges.get(char_id, 0.0) + speed * delta * 10.0, 100.0)

		if atb_gauges[char_id] >= 100.0 and not _in_turn_queue(char_id):
			turn_queue.append({"type": "character", "id": char_id})
			turn_ready.emit({"type": "character", "id": char_id})

	# Fill enemy ATB
	for i in range(current_enemies.size()):
		var enemy := current_enemies[i]
		if enemy["current_hp"] <= 0:
			continue
		var key := "enemy_%d" % i
		var speed_mod := _get_speed_modifier_enemy(i)
		var speed := enemy.get("speed", 10) * speed_mod
		atb_gauges[key] = min(atb_gauges.get(key, 0.0) + speed * delta * 10.0, 100.0)

		if atb_gauges[key] >= 100.0 and not _in_turn_queue(key):
			turn_queue.append({"type": "enemy", "id": i})
			turn_ready.emit({"type": "enemy", "id": i})

	# Process turn queue
	if not turn_queue.is_empty() and not _any_actor_animating():
		var actor := turn_queue[0]
		if actor["type"] == "enemy":
			_process_enemy_turn(actor["id"])

func _is_menu_open() -> bool:
	return false  # Set by UI when menu is open

func _in_turn_queue(key: Variant) -> bool:
	for actor in turn_queue:
		if actor["id"] == key:
			return true
	return false

func _any_actor_animating() -> bool:
	return false  # Set by animation system

# ===== PLAYER ACTION =====

func execute_player_action(char_id: String, action: Dictionary) -> void:
	if not char_id in active_combatants:
		return

	# Reset ATB gauge
	atb_gauges[char_id] = 0.0
	turn_queue = turn_queue.filter(func(a): return not (a["type"] == "character" and a["id"] == char_id))

	var action_type: String = action.get("type", "attack")
	match action_type:
		"attack":
			_execute_attack(char_id, action)
		"spell":
			_execute_spell(char_id, action)
		"item":
			_execute_item(char_id, action)
		"defend":
			_execute_defend(char_id)
		"flee":
			_attempt_flee()
		"swap":
			_execute_swap(char_id, action)

	character_acted.emit(char_id, action)
	_check_battle_end()

	# Baby Dragon counter (Javin)
	if char_id == "javin" and action_type in ["attack"]:
		_advance_baby_dragon_counter()

func _advance_baby_dragon_counter() -> void:
	var javin := PartyManager.get_character("javin")
	if javin.is_empty() or not GameManager.has_key_item("baby_dragon"):
		return
	javin["baby_dragon_counter"] += 1
	if javin["baby_dragon_counter"] >= 4:
		javin["baby_dragon_counter"] = 0
		# Fire Level 2 attack on random enemy
		var target_idx := _get_random_living_enemy()
		if target_idx >= 0:
			_deal_damage_to_enemy(target_idx, "fire", DamageType.MAGICAL, 2, "Baby Dragon")

# ===== ATTACK =====

func _execute_attack(char_id: String, action: Dictionary) -> void:
	var char_state := PartyManager.get_character(char_id)
	if char_state.is_empty():
		return

	var target := action.get("target", {})
	var target_type: String = target.get("type", "enemy")
	var target_id = target.get("id", 0)

	if target_type == "enemy":
		var damage := _calc_physical_damage(char_id, target_id)
		_deal_damage_to_enemy(target_id, "none", DamageType.PHYSICAL, damage, char_id)
		AudioManager.play_sfx("battle_hit_physical")

		# Iris learns attack if it's a wildlife enemy
		if FlagManager.is_flag("iris_recruited") and current_enemies[target_id].get("is_wildlife", false):
			if "iris" in active_combatants:
				PartyManager.learn_wildlife_attack({"name": action.get("attack_name",""), "damage": damage})

		# Check bubble pop
		_check_bubble_pop(target_id)

# ===== DAMAGE CALCULATION =====

func _calc_physical_damage(attacker_id: String, target_enemy_idx: int) -> int:
	var char_state := PartyManager.get_character(attacker_id)
	var enemy := current_enemies[target_enemy_idx]
	var attack := char_state["stats"]["attack"]

	# Equipment bonus
	attack += _get_equipment_attack_bonus(attacker_id)

	var defense := enemy.get("defense", 0)
	var raw := max(1, attack - defense)
	var variance := raw * randf_range(0.85, 1.15)

	# Critical hit check
	var crit_chance := 0.05 + _get_crit_bonus(attacker_id)
	var is_crit := randf() < crit_chance
	if is_crit:
		variance *= 2.0

	# Berserk attack boost
	if _has_status(attacker_id, "berserk"):
		variance *= 1.5

	return max(1, int(variance))

func _calc_magical_damage(char_id: String, spell_data: Dictionary, target_enemy_idx: int) -> int:
	var char_state := PartyManager.get_character(char_id)
	var enemy := current_enemies[target_enemy_idx]

	var magic_power := char_state["stats"]["magic_power"]
	magic_power += _get_equipment_magic_bonus(char_id)

	var spell_resistance := enemy.get("spell_resistance", 0)
	var base_power: int = spell_data.get("base_power", 10)
	var raw := max(1, (magic_power + base_power) - spell_resistance)
	var variance := raw * randf_range(0.9, 1.1)

	# Elemental multiplier
	var element: String = spell_data.get("element", "none")
	variance *= _get_elemental_multiplier(element, enemy)

	# Double cast
	if spell_data.get("double_cast", false):
		variance *= 2.0

	# Hannah Magus multi-target reduces per-target damage
	if spell_data.get("multi_target", false):
		variance *= 0.7

	return max(1, int(variance))

func _calc_psychic_damage(char_id: String, spell_data: Dictionary) -> int:
	var char_state := PartyManager.get_character(char_id)
	var base_power: int = spell_data.get("base_power", 8)
	var magic_power := char_state["stats"]["magic_power"]

	# Psychic: slightly weaker base, unresistable
	var raw := int((magic_power * 0.85 + base_power) * randf_range(0.9, 1.1))

	# High crit chance for psychic
	var crit_chance := 0.15 + _get_crit_bonus(char_id)
	if randf() < crit_chance:
		raw = int(raw * 2.5)

	# Dreamwalker mastery bonus
	var char_state2 := PartyManager.get_character(char_id)
	if "dreamwalker_mastery" in char_state2.get("abilities", []):
		raw = int(raw * 1.25)

	return max(1, raw)

func _deal_damage_to_enemy(enemy_idx: int, element: String, damage_type: int, amount: int, source: String) -> void:
	if enemy_idx < 0 or enemy_idx >= current_enemies.size():
		return
	var enemy := current_enemies[enemy_idx]
	if enemy["current_hp"] <= 0:
		return

	enemy["current_hp"] = max(0, enemy["current_hp"] - amount)
	damage_dealt.emit({"type": "enemy", "index": enemy_idx}, amount, _damage_type_name(damage_type), element)

	# Burn spread (Arsonist Crankpot)
	if element == "fire" and FlagManager.is_flag("crankpot_recruited"):
		var crankpot := PartyManager.get_character("crankpot")
		if not crankpot.is_empty() and crankpot["current_class"] == "arsonist":
			_apply_status_enemy(enemy_idx, "burn", {"spread_chance": 0.15})

	if enemy["current_hp"] <= 0:
		_on_enemy_ko(enemy_idx)

func _deal_damage_to_character(char_id: String, amount: int, damage_type: int, element: String = "none") -> void:
	var char_state := PartyManager.get_character(char_id)
	if char_state.is_empty() or char_state["hp"] <= 0:
		return

	# Check bubble (pops on hit)
	if _has_status(char_id, "bubble"):
		_remove_status(char_id, "bubble")
		damage_dealt.emit({"type": "character", "id": char_id}, 0, "bubble_pop", element)
		return

	# Physical damage reduced by armor
	var final_damage := amount
	if damage_type == DamageType.PHYSICAL:
		var armor := char_state["stats"]["defense"] + _get_equipment_defense_bonus(char_id)
		final_damage = max(1, amount - armor)

	# Magical damage reduced by spell resistance
	elif damage_type == DamageType.MAGICAL:
		var resistance := char_state["stats"]["spell_resistance"] + _get_equipment_resistance_bonus(char_id)
		final_damage = max(1, amount - resistance)

	# Psychic: no reduction

	# Michael auto-taunt redirect
	if damage_type == DamageType.PHYSICAL and char_id != "michael":
		if _michael_auto_taunt_active():
			_deal_damage_to_character("michael", amount, damage_type, element)
			return

	char_state["hp"] = max(0, char_state["hp"] - final_damage)
	damage_dealt.emit({"type": "character", "id": char_id}, final_damage, _damage_type_name(damage_type), element)

	if char_state["hp"] <= 0:
		_on_character_ko(char_id)

func _michael_auto_taunt_active() -> bool:
	if not "michael" in active_combatants:
		return false
	var michael := PartyManager.get_character("michael")
	if michael.is_empty() or michael["hp"] <= 0:
		return false
	if michael["current_class"] != "paladin":
		return false
	if michael["equipment"]["shield"] == "":
		return false
	return true

# ===== SPELLS =====

func _execute_spell(char_id: String, action: Dictionary) -> void:
	var spell_id: String = action.get("spell_id", "")
	var spell_data := _get_spell_data(spell_id)
	if spell_data.is_empty():
		return

	var char_state := PartyManager.get_character(char_id)
	var mp_cost: int = spell_data.get("mp_cost", 1)

	# Hannah Magus multi-target costs +3 MP flat
	if action.get("multi_target", false):
		mp_cost += 3

	# Flood/Hannah double cast
	if action.get("double_cast", false):
		mp_cost *= 2
		spell_data["double_cast"] = true

	if char_state["mp"] < mp_cost:
		return  # Not enough MP

	char_state["mp"] -= mp_cost

	var targets: Array = action.get("targets", [])
	var element: String = spell_data.get("element", "none")
	var damage_type := DamageType.MAGICAL

	# Psychic spells (Dreamwalker)
	if element == "psychic":
		damage_type = DamageType.PSYCHIC

	for target in targets:
		if target["type"] == "enemy":
			var dmg := 0
			if damage_type == DamageType.PSYCHIC:
				dmg = _calc_psychic_damage(char_id, spell_data)
			else:
				dmg = _calc_magical_damage(char_id, spell_data, target["index"])
			_deal_damage_to_enemy(target["index"], element, damage_type, dmg, char_id)

			# Water removes Burn
			if element == "water":
				_remove_status_enemy(target["index"], "burn")

		elif target["type"] == "character":
			if spell_data.get("is_heal", false):
				_heal_character(target["id"], spell_data, char_id)
			else:
				var dmg := 0
				if damage_type == DamageType.PSYCHIC:
					dmg = _calc_psychic_damage(char_id, spell_data)
				else:
					dmg = _calc_magical_damage(char_id, spell_data, -1)
				_deal_damage_to_character(target["id"], dmg, damage_type, element)

	AudioManager.play_sfx("spell_" + element)

func _heal_character(char_id: String, spell_data: Dictionary, caster_id: String) -> void:
	var char_state := PartyManager.get_character(char_id)
	if char_state.is_empty() or char_state["hp"] <= 0:
		return

	var caster_state := PartyManager.get_character(caster_id)
	var heal_power := caster_state["stats"]["magic_power"]
	var base_heal: int = spell_data.get("base_power", 30)

	# Michael Paladin healing bonus
	var heal_bonus := 1.0
	if "healing_power_plus_10" in caster_state.get("abilities", []):
		heal_bonus += 0.10
	if "healing_power_plus_20" in caster_state.get("abilities", []):
		heal_bonus += 0.20

	var amount := int((heal_power * 0.5 + base_heal) * heal_bonus * randf_range(0.9, 1.1))

	# Double cast
	if spell_data.get("double_cast", false):
		amount *= 2

	char_state["hp"] = min(char_state["max_hp"], char_state["hp"] + amount)
	damage_dealt.emit({"type": "character", "id": char_id}, -amount, "heal", "none")

	# Esuna clears status effects
	if spell_data.get("is_esuna", false):
		_clear_all_statuses(char_id)

	# Raise - revive KO'd character
	if spell_data.get("is_raise", false) and char_state["hp"] == 0:
		char_state["hp"] = int(char_state["max_hp"] * 0.3)
		if FlagManager.is_flag("fei_dead_in_battle") and char_id == "fei":
			FlagManager.set_flag("fei_dead_in_battle", false)

# ===== ITEMS =====

func _execute_item(char_id: String, action: Dictionary) -> void:
	var item_id: String = action.get("item_id", "")
	var target_id: String = action.get("target_id", char_id)

	if not GameManager.remove_item(item_id, 1):
		return

	# Load item data to handle effects generically
	var ItemDB = load("res://data/items/item_database.gd")
	var item_data: Dictionary = {}
	if ItemDB:
		item_data = ItemDB.get_item(item_id)

	# Use item_data effect field for generic handling, with specific overrides
	var effect: String = item_data.get("effect", "")
	var value: int = item_data.get("value", 0)

	match item_id:
		# Healing items
		"potion":
			_heal_simple(target_id, 100)
			AudioManager.play_sfx("spell_heal")
		"hi_potion":
			_heal_simple(target_id, 500)
			AudioManager.play_sfx("spell_heal")
		"mega_potion":
			_heal_simple(target_id, 2000)
			AudioManager.play_sfx("spell_heal")
		"elixir":
			_heal_simple(target_id, 99999)
			_restore_mp(target_id, 99999)
			AudioManager.play_sfx("spell_heal")
		# MP restore
		"ether":
			_restore_mp(target_id, 50)
			AudioManager.play_sfx("spell_heal")
		"hi_ether":
			_restore_mp(target_id, 200)
			AudioManager.play_sfx("spell_heal")
		# Revive
		"phoenix_down":
			_revive_character(target_id, 0.25)
			AudioManager.play_sfx("level_up")
		"mega_phoenix":
			# Revive all KO'd party members
			for cid in PartyManager.get_active_party():
				var cs := PartyManager.get_character(cid)
				if not cs.is_empty() and cs.get("hp", 1) <= 0:
					_revive_character(cid, 0.5)
			AudioManager.play_sfx("level_up")
		# Status cures
		"antidote":
			_remove_status(target_id, "poison")
		"eye_drops":
			_remove_status(target_id, "blind")
		"echo_herb", "echo_screen":
			_remove_status(target_id, "silence")
		"soft":
			_remove_status(target_id, "paralysis")
		"dream_powder":
			_remove_status(target_id, "sleep")
		"smelling_salts":
			_remove_status(target_id, "confuse")
		"remedy":
			for s in ["poison", "blind", "silence", "paralysis", "sleep", "confuse"]:
				_remove_status(target_id, s)
		"holy_water":
			_remove_status(target_id, "burn")
			_deal_damage_to_enemy(0, "water", DamageType.MAGICAL, 75, "holy_water")
		# Battle items (deal damage to enemies)
		"fire_bomb":
			_deal_damage_to_enemy(0, "fire", DamageType.MAGICAL, 200, "fire_bomb")
			AudioManager.play_sfx("spell_fire")
		"thunder_gem":
			for i in range(current_enemies.size()):
				_deal_damage_to_enemy(i, "thunder", DamageType.MAGICAL, 300, "thunder_gem")
			AudioManager.play_sfx("spell_thunder")
		"earth_crystal":
			for i in range(current_enemies.size()):
				_deal_damage_to_enemy(i, "earth", DamageType.MAGICAL, 300, "earth_crystal")
			AudioManager.play_sfx("spell_earth")
		"darkness_shard":
			_deal_damage_to_enemy(0, "dark", DamageType.MAGICAL, 150, "darkness_shard")
		"void_essence":
			for i in range(current_enemies.size()):
				_deal_damage_to_enemy(i, "void", DamageType.PSYCHIC, 9999, "void_essence")
		# Buff items
		"bubble_flask":
			_apply_status(target_id, "bubble")
		"haste_tonic":
			_apply_status(target_id, "haste")
		"iron_shield_pill":
			var cs := PartyManager.get_character(target_id)
			if not cs.is_empty():
				cs["iron_shield"] = true
		"tent":
			# Tent can only be used at save points, not in battle
			GameManager.add_item(item_id, 1)  # Return it
		_:
			# Generic fallback using item_data effect
			match effect:
				"heal_hp":
					_heal_simple(target_id, value)
				"heal_mp":
					_restore_mp(target_id, value)
				"revive":
					_revive_character(target_id, float(value) / 100.0)
				"damage_fire":
					_deal_damage_to_enemy(0, "fire", DamageType.MAGICAL, value, item_id)
				_:
					push_warning("BattleManager._execute_item: Unknown item '%s'" % item_id)

func _heal_simple(char_id: String, amount: int) -> void:
	var char_state := PartyManager.get_character(char_id)
	if char_state.is_empty():
		return
	char_state["hp"] = min(char_state["max_hp"], char_state["hp"] + amount)

func _restore_mp(char_id: String, amount: int) -> void:
	var char_state := PartyManager.get_character(char_id)
	if char_state.is_empty():
		return
	char_state["mp"] = min(char_state["max_mp"], char_state["mp"] + amount)

func _revive_character(char_id: String, hp_pct: float) -> void:
	var char_state := PartyManager.get_character(char_id)
	if char_state.is_empty():
		return
	if char_state["hp"] > 0:
		return  # Already alive
	char_state["hp"] = int(char_state["max_hp"] * hp_pct)
	if char_id == "fei" and FlagManager.is_flag("fei_dead_in_battle"):
		FlagManager.set_flag("fei_dead_in_battle", false)

func _execute_defend(char_id: String) -> void:
	# Add temp defend buff
	var char_state := PartyManager.get_character(char_id)
	if not char_state.is_empty():
		char_state.get_or_add("defending", false)
		char_state["defending"] = true

func _attempt_flee() -> void:
	if randf() < 0.75:
		battle_result = "fled"
		_end_battle()

func _execute_swap(char_id: String, action: Dictionary) -> void:
	var bench_id: String = action.get("bench_id", "")
	if GameManager.swap_party_member(bench_id, char_id):
		active_combatants.erase(char_id)
		active_combatants.append(bench_id)
		atb_gauges[bench_id] = 0.0

# ===== ENEMY AI =====

func _process_enemy_turn(enemy_idx: int) -> void:
	var key := "enemy_%d" % enemy_idx
	atb_gauges[key] = 0.0
	turn_queue = turn_queue.filter(func(a): return not (a["type"] == "enemy" and a["id"] == enemy_idx))

	var enemy := current_enemies[enemy_idx]
	if enemy["current_hp"] <= 0:
		return

	# Simple AI: choose action from enemy's action list
	var actions: Array = enemy.get("actions", [{"type": "attack", "weight": 100}])
	var action := _weighted_random_action(actions)

	match action.get("type", "attack"):
		"attack":
			_enemy_attack(enemy_idx)
		"spell":
			_enemy_spell(enemy_idx, action)
		"ability":
			_enemy_ability(enemy_idx, action)

	enemy_acted.emit(enemy_idx, action)
	_check_battle_end()

func _enemy_attack(enemy_idx: int) -> void:
	var enemy := current_enemies[enemy_idx]
	var target_id := _get_enemy_attack_target()
	if target_id == "":
		return

	var attack := enemy.get("attack", 20)
	var char_state := PartyManager.get_character(target_id)
	var defense := char_state["stats"]["defense"] + _get_equipment_defense_bonus(target_id)
	var damage := max(1, int((attack - defense) * randf_range(0.85, 1.15)))

	_deal_damage_to_character(target_id, damage, DamageType.PHYSICAL)
	AudioManager.play_sfx("battle_hit_physical")

func _enemy_spell(enemy_idx: int, action: Dictionary) -> void:
	var enemy := current_enemies[enemy_idx]
	var target_id := _get_enemy_attack_target()
	if target_id == "":
		return

	var spell_power: int = action.get("power", 30)
	var element: String = action.get("element", "none")
	var char_state := PartyManager.get_character(target_id)
	var resistance := char_state["stats"]["spell_resistance"] + _get_equipment_resistance_bonus(target_id)
	var damage := max(1, int((spell_power - resistance) * randf_range(0.9, 1.1)))
	_deal_damage_to_character(target_id, damage, DamageType.MAGICAL, element)
	AudioManager.play_sfx("spell_" + element)

func _enemy_ability(enemy_idx: int, action: Dictionary) -> void:
	var ability: String = action.get("ability_id", "")
	var target_id := _get_enemy_attack_target()
	# Apply status effect
	if ability.ends_with("_inflict"):
		var status_name := ability.replace("_inflict", "")
		_apply_status(target_id, status_name, {})

func _get_enemy_attack_target() -> String:
	# Check Fei Taunt or Michael auto-taunt
	if "fei" in active_combatants:
		var fei := PartyManager.get_character("fei")
		if not fei.is_empty() and fei["hp"] > 0 and fei.get("taunting", false):
			return "fei"

	if _michael_auto_taunt_active():
		return "michael"

	# Confuse check
	for char_id in active_combatants:
		var char_state := PartyManager.get_character(char_id)
		if char_state.is_empty() or char_state["hp"] <= 0:
			continue
		return char_id

	return ""

func _get_random_living_enemy() -> int:
	var alive := []
	for i in range(current_enemies.size()):
		if current_enemies[i]["current_hp"] > 0:
			alive.append(i)
	if alive.is_empty():
		return -1
	return alive[randi() % alive.size()]

func _weighted_random_action(actions: Array) -> Dictionary:
	var total_weight := 0
	for a in actions:
		total_weight += a.get("weight", 100)
	var roll := randi() % total_weight
	var cumulative := 0
	for a in actions:
		cumulative += a.get("weight", 100)
		if roll < cumulative:
			return a
	return actions[0]

# ===== STATUS EFFECTS =====

func _apply_status(char_id: String, status: String, params: Dictionary = {}) -> void:
	var char_state := PartyManager.get_character(char_id)
	if char_state.is_empty():
		return
	if not status in char_state["status_effects"]:
		char_state["status_effects"].append(status)
		status_applied.emit({"type": "character", "id": char_id}, status)

func _apply_status_enemy(enemy_idx: int, status: String, params: Dictionary = {}) -> void:
	var enemy := current_enemies[enemy_idx]
	if not status in enemy["status_effects"]:
		enemy["status_effects"].append(status)
		# Burn spread
		if status == "burn" and params.get("spread_chance", 0.0) > 0:
			enemy["burn_spread_chance"] = params["spread_chance"]
		status_applied.emit({"type": "enemy", "index": enemy_idx}, status)

func _remove_status(char_id: String, status: String) -> void:
	var char_state := PartyManager.get_character(char_id)
	if char_state.is_empty():
		return
	char_state["status_effects"].erase(status)
	status_removed.emit({"type": "character", "id": char_id}, status)

func _remove_status_enemy(enemy_idx: int, status: String) -> void:
	if enemy_idx < 0 or enemy_idx >= current_enemies.size():
		return
	var enemy := current_enemies[enemy_idx]
	enemy["status_effects"].erase(status)

func _has_status(char_id: String, status: String) -> bool:
	var char_state := PartyManager.get_character(char_id)
	if char_state.is_empty():
		return false
	return status in char_state["status_effects"]

func _clear_all_statuses(char_id: String) -> void:
	var char_state := PartyManager.get_character(char_id)
	if not char_state.is_empty():
		char_state["status_effects"].clear()

func _check_bubble_pop(enemy_idx: int) -> void:
	var enemy := current_enemies[enemy_idx]
	if "bubble" in enemy["status_effects"]:
		_remove_status_enemy(enemy_idx, "bubble")

# ===== KO HANDLERS =====

func _on_character_ko(char_id: String) -> void:
	character_ko.emit(char_id)
	AudioManager.play_sfx("battle_miss")

	# Fei death triggers Iris berserk
	if char_id == "fei" and "iris" in active_combatants:
		FlagManager.set_flag("fei_dead_in_battle", true)
		var iris := PartyManager.get_character("iris")
		if not iris.is_empty():
			if iris["current_class"] == "shapeshifter":
				_activate_iris_berserk_shapeshifter()
			else:
				_activate_iris_berserk_druid()

	_check_battle_end()

func _activate_iris_berserk_shapeshifter() -> void:
	# Player loses control of Iris, she targets Fei's killer each turn
	var iris := PartyManager.get_character("iris")
	iris["berserk_mode"] = true
	iris["berserk_target"] = "last_ko_cause"
	if "panda_form" in iris.get("abilities", []):
		iris["panda_form_active"] = true
	AudioManager.play_sfx("iris_berserk_roar")

func _activate_iris_berserk_druid() -> void:
	var iris := PartyManager.get_character("iris")
	iris["berserk_mode"] = true
	iris["random_action_mode"] = true

func _on_enemy_ko(enemy_idx: int) -> void:
	var enemy := current_enemies[enemy_idx]
	pending_exp += enemy.get("exp_reward", 10)
	pending_gil += enemy.get("gil_reward", 5)
	enemy_ko.emit(enemy_idx)
	_check_battle_end()

# ===== BATTLE END =====

func _check_battle_end() -> void:
	var all_enemies_dead := true
	for enemy in current_enemies:
		if enemy["current_hp"] > 0:
			all_enemies_dead = false
			break

	var all_party_dead := true
	for char_id in active_combatants:
		var char_state := PartyManager.get_character(char_id)
		if not char_state.is_empty() and char_state["hp"] > 0:
			all_party_dead = false
			break

	if all_enemies_dead:
		battle_result = "victory"
		_end_battle()
	elif all_party_dead:
		battle_result = "defeat"
		_end_battle()

func _end_battle() -> void:
	in_battle = false
	atb_active = false
	turn_queue.clear()

	# Clear battle-only status effects
	for char_id in active_combatants:
		var char_state := PartyManager.get_character(char_id)
		if char_state.is_empty():
			continue
		char_state["status_effects"].clear()
		char_state["defending"] = false
		if char_id == "iris":
			char_state["berserk_mode"] = false
			char_state["panda_form_active"] = false

	if battle_result == "victory":
		# Award EXP and Gil
		_award_exp_and_gil()
		AudioManager.play_music("victory")

	elif battle_result == "defeat":
		AudioManager.play_music("game_over")

	FlagManager.set_flag("fei_dead_in_battle", false)
	battle_ended.emit(battle_result)

func _award_exp_and_gil() -> void:
	GameManager.earn_gil(pending_gil)
	var party := GameManager.get_active_characters()
	var exp_per_char := pending_exp / max(1, party.size())
	for char_id in party:
		PartyManager.add_exp(char_id, exp_per_char)

func _is_ko(char_id: String) -> bool:
	var char_state := PartyManager.get_character(char_id)
	if char_state.is_empty():
		return true
	return char_state["hp"] <= 0

# ===== HELPERS =====

func _get_spell_data(spell_id: String) -> Dictionary:
	# Load from SpellDatabase resource
	return SpellDatabase.get_spell(spell_id)

func _get_equipment_attack_bonus(char_id: String) -> int:
	return 0  # Expanded by equipment system

func _get_equipment_defense_bonus(char_id: String) -> int:
	return 0

func _get_equipment_magic_bonus(char_id: String) -> int:
	return 0

func _get_equipment_resistance_bonus(char_id: String) -> int:
	return 0

func _get_crit_bonus(char_id: String) -> float:
	var char_state := PartyManager.get_character(char_id)
	if char_state.is_empty():
		return 0.0
	var bonus := 0.0
	if "crit_plus_10" in char_state.get("abilities", []):
		bonus += 0.10
	return bonus

func _get_speed_modifier(char_id: String) -> float:
	var mod := 1.0
	if _has_status(char_id, "slow"):
		mod *= 0.5
	if _has_status(char_id, "haste"):
		mod *= 1.75
	return mod

func _get_speed_modifier_enemy(enemy_idx: int) -> float:
	var enemy := current_enemies[enemy_idx]
	var mod := 1.0
	if "slow" in enemy.get("status_effects", []):
		mod *= 0.5
	if "haste" in enemy.get("status_effects", []):
		mod *= 1.75
	return mod

func _get_elemental_multiplier(element: String, enemy: Dictionary) -> float:
	var weaknesses: Array = enemy.get("elemental_weaknesses", [])
	var resistances: Array = enemy.get("elemental_resistances", [])
	var immunities: Array = enemy.get("elemental_immunities", [])

	if element in immunities:
		return 0.0
	if element in weaknesses:
		return 2.0
	if element in resistances:
		return 0.5
	return 1.0

func _damage_type_name(damage_type: int) -> String:
	match damage_type:
		DamageType.PHYSICAL: return "physical"
		DamageType.MAGICAL: return "magical"
		DamageType.PSYCHIC: return "psychic"
	return "none"

func is_in_battle() -> bool:
	return in_battle
