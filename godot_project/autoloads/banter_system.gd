extends Node

## In-battle banter system for "There Will Be Kobolds".
## When certain character pairs are both in the active party, there is a 15%
## chance of banter lines appearing between turns. Data is loaded from the
## druid_dreamwalker_banter JSON file.  Multiple pairs can be registered in
## that file; the system picks one unseen pair per battle and one unseen line
## within that pair so conversations do not repeat.

signal banter_triggered(speaker: String, text: String)

const BANTER_PATH: String = "res://data/dialogues/druid_dreamwalker_banter.json"
const BANTER_CHANCE: float = 0.15

## Raw banter data keyed by pair identifier, e.g. "druid_dreamwalker".
## Each value is an Array of { "speaker": String, "text": String } dicts.
var _banter_data: Dictionary = {}

## Tracks which pair keys have already fired this battle to prevent repeats.
var _shown_this_battle: Array[String] = []

# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------

func _ready() -> void:
	_load_banter()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

## Call this at the start of every new battle so repeat-suppression resets.
func reset_for_battle() -> void:
	_shown_this_battle.clear()


## Call this between turns (e.g. from the ATB scheduler) with the current
## active party member names as strings.  If a registered pair is present and
## the random roll succeeds, one unseen banter line is emitted.
func try_trigger_banter(active_party: Array) -> void:
	if _banter_data.is_empty():
		return

	# Collect all eligible pair keys (both members present, not yet shown).
	var eligible: Array[String] = []
	for pair_key in _banter_data.keys():
		if pair_key in _shown_this_battle:
			continue
		if _check_pair(pair_key, active_party):
			eligible.append(pair_key)

	if eligible.is_empty():
		return

	# Random chance gate — checked once per call regardless of how many pairs
	# are eligible, so the probability stays predictable.
	if randf() > BANTER_CHANCE:
		return

	# Pick a random eligible pair and a random unseen line from it.
	var chosen_pair: String = eligible[randi() % eligible.size()]
	var lines: Array = _banter_data[chosen_pair]

	if lines.is_empty():
		return

	var chosen_line: Dictionary = lines[randi() % lines.size()]
	var speaker: String = chosen_line.get("speaker", "???")
	var text: String = chosen_line.get("text", "")

	# Suppress this pair for the rest of the battle.
	_shown_this_battle.append(chosen_pair)

	banter_triggered.emit(speaker, text)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

## Loads and parses the JSON file.  Expects the top-level key "banter" to
## hold a Dictionary whose keys are pair identifiers and whose values are
## Arrays of { "speaker", "text" } objects.
func _load_banter() -> void:
	if not FileAccess.file_exists(BANTER_PATH):
		push_warning("BanterSystem: banter file not found at %s" % BANTER_PATH)
		return

	var file := FileAccess.open(BANTER_PATH, FileAccess.READ)
	if file == null:
		push_error("BanterSystem: failed to open %s (error %d)" % [BANTER_PATH, FileAccess.get_open_error()])
		return

	var raw_text: String = file.get_as_text()
	file.close()

	var parsed = JSON.parse_string(raw_text)
	if parsed == null:
		push_error("BanterSystem: JSON parse error in %s" % BANTER_PATH)
		return

	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("BanterSystem: expected a JSON object at the root of %s" % BANTER_PATH)
		return

	if not parsed.has("banter"):
		push_error("BanterSystem: missing top-level 'banter' key in %s" % BANTER_PATH)
		return

	var banter_section = parsed["banter"]
	if typeof(banter_section) != TYPE_DICTIONARY:
		push_error("BanterSystem: 'banter' key must be a JSON object in %s" % BANTER_PATH)
		return

	# Validate and copy each pair entry.
	for pair_key in banter_section.keys():
		var lines = banter_section[pair_key]
		if typeof(lines) != TYPE_ARRAY:
			push_warning("BanterSystem: pair '%s' has non-array value; skipping." % pair_key)
			continue

		var validated_lines: Array[Dictionary] = []
		for i in lines.size():
			var entry = lines[i]
			if typeof(entry) != TYPE_DICTIONARY:
				push_warning("BanterSystem: pair '%s' entry %d is not an object; skipping." % [pair_key, i])
				continue
			if not entry.has("speaker") or not entry.has("text"):
				push_warning("BanterSystem: pair '%s' entry %d missing 'speaker' or 'text'; skipping." % [pair_key, i])
				continue
			validated_lines.append({ "speaker": str(entry["speaker"]), "text": str(entry["text"]) })

		if not validated_lines.is_empty():
			_banter_data[pair_key] = validated_lines

	print("BanterSystem: loaded %d pair(s) from %s" % [_banter_data.size(), BANTER_PATH])


## Returns true when both characters named in pair_key are present in
## active_party.  pair_key format is "char1_char2" (single underscore
## separator; character names must not contain underscores themselves).
## The lookup is case-insensitive so JSON authoring is forgiving.
func _check_pair(pair_key: String, active_party: Array) -> bool:
	# Build a lower-case set of active party member names for O(1) lookup.
	var party_lower: Dictionary = {}
	for member in active_party:
		party_lower[str(member).to_lower()] = true

	# Split on the first underscore only so names like "dreamwalker" survive.
	var sep_index: int = pair_key.find("_")
	if sep_index == -1:
		push_warning("BanterSystem: pair key '%s' has no underscore separator." % pair_key)
		return false

	var char1: String = pair_key.left(sep_index).to_lower()
	var char2: String = pair_key.substr(sep_index + 1).to_lower()

	return party_lower.has(char1) and party_lower.has(char2)
