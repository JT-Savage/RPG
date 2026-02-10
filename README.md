# There Will Be Kobolds

A 30+ hour dark fantasy JRPG for iOS using Pythonista's `scene` module, inspired by Final Fantasy 1-6.

## Overview

Based on the book "There Will Be Kobolds," this is a complete RPG featuring:

- **12 Recruitable Characters** (7 required, 5 optional)
- **Class Evolution System** via Orisia sidequests with key items
- **Active Time Battle** or Turn-Based combat
- **4 Different Endings** (Best, Good, Normal, Bad)
- **New Game+** with commentary and max-level starts
- **30+ Hour Campaign** with dark fantasy story and gallows humor

## Technical Specifications

- **Engine**: Pythonista `scene` module (iOS)
- **Resolution**: 256x224 pixels (logical, scaled to device)
- **Orientation**: Landscape only
- **Controls**: Touch-only, two-handed gameplay
- **Tile Size**: 16x16 pixels (maps), 16x24 pixels (characters)
- **Art Style**: 16-bit Final Fantasy (FF4-FF6 era)

## Characters

### Required Characters
1. **Javin** - Claw Noble → Dreamwalker (Psychic damage specialist)
2. **Frostbite** - Gunner (Shotgun specialist, gets Ultimate Shotgun)
3. **Fei** - Warrior → Weapon Master (Tank/DPS with dual-wielding)
4. **Michael** - Cleric → Paladin (Healer/Tank hybrid)
5. **Flood** - Ice Mage (Dies permanently in story)
6. **Hannah** - Witch → Magus (Elemental magic specialist)
7. **Warghoul** - Undead Warrior → Deathknight (Summons skeletons)

### Optional Characters
8. **Cookie** - Druid → Druidess (Control spells)
9. **Iris** - Nature Bound Druid → Shapeshifter (Panda form, goes berserk when Fei dies)
10. **Fritzzit** - Goblin Sniper (Gets Ultimate Sniper Rifle, instant-kill crits)
11. **Crankpot** - Goblin Firemage → Arsonist (Burn status with 15% spread)
12. **Yipp** - Ratling Necromancer → Saint/Vampire (Alignment choice affects ending)

## Key Features

### Magic System
- **MP-Based Casting**: MP cost = spell level (1-9)
- **Purchasable Spells**: Buy spells from magic shops
- **Class Restrictions**: Only certain classes can learn specific magic types
- **Psychic Damage**: Dreamwalker's spells cannot be resisted

### Key Item System
- **Cannot be sold/destroyed** once obtained
- **Required for character evolution** sidequests with Orisia
- **Cutscene triggers** (Cookie's Crown, Iris's Panda Fur)
- **Tutorial introduction** with Baby Dragon (optional in tutorial)

### Combat System
- **ATB or Turn-Based** (performance-dependent)
- **Active Party**: 3 characters in battle
- **Mid-Battle Swapping**: Switch with reserves
- **Status Effects**: Poison, Burn, Sleep, Paralysis, Silence, Berserk, etc.
- **Burn Mechanic**: 15% chance to spread to adjacent enemies

### Character Evolution
- **Orisia Sidequests**: Meet Orisia before desert to unlock evolutions
- **Key Item Requirements**: Each character needs specific key items
- **Level Cap Increase**: 75 → 99 upon evolution (except Flood, always 99)
- **Deadline**: Recruitment/evolution cutoff when entering desert

### Story Highlights
- **Flood's Permanent Death**: Dramatic cutscene after 2nd dragon boss
- **Iris's Berserk**: Goes berserk (uncontrollable) when Fei dies in battle
- **Yipp's Alignment**: Choose Saint (Good/Best ending) or Vampire (Bad ending only)
- **Fungal Enemies Removed**: After Jerod boss, fungal wildlife disappears permanently
- **Infected Kobolds Dominate**: 70% spawn rate after Imperial Warren escape

### Ending Paths

**Best Ending** (Post-credits secret ending):
- Yipp recruited AND became Saint
- Cure found (Kella saved)
- Complete Slaver Island (defeat Captain Donald)

**Good Ending**:
- Cure found (Kella saved)
- Yipp is Saint OR not recruited
- Credits roll

**Normal Ending**:
- Cure found but not all characters recruited
- Yipp is Saint OR not recruited

**Bad Ending**:
- Cure NOT found
- Kella becomes double-infected boss
- Fight through capitol city to secret boss battle

### New Game+
- **Start at max available level** for each character
- **Harder enemies** with scaled stats
- **Character commentary** references previous playthrough
- **Story variations** based on past choices
- **Try opposite Yipp alignment** or different endings

## Project Structure

```
RPG/
├── main.py                 # Entry point
├── scenes/                 # Game scenes
│   └── title_screen.py
├── data/                   # Game data
│   ├── characters.py       # 12 characters, stats, abilities
│   ├── spells.py           # Magic system
│   ├── key_items.py        # Key items and sidequests
│   ├── items.py            # Consumables
│   ├── equipment.py        # Weapons, armor, accessories
│   └── enemies.py          # Enemies and bosses
├── utils/                  # Game systems (to be built)
│   ├── save_system.py
│   ├── battle_engine.py
│   ├── recruitment_system.py
│   └── ending_system.py
└── assets/                 # Graphics and audio
    ├── sprites/
    ├── tiles/
    └── ui/
```

## Current Status

**Completed**:
- Project structure
- Character class system (all 12 characters with stats, growth, abilities)
- Magic system (all spells, purchasable, MP-based)
- Key item system (with cutscene triggers)
- Items and equipment data
- Enemy and boss data (FF6-style progression)
- Title screen (basic)

**In Progress**:
- Save/load system
- Combat engine
- Map/world rendering
- Recruitment system

**To Do**:
- Battle engine (ATB/Turn-based)
- Level-up system (abilities every 10 levels)
- Orisia sidequest system
- Story events and cutscenes
- Dungeon system
- Ending system
- New Game+
- UI/UX polish
- Tutorial system

## Development Notes

### Critical Implementation Details

**Yipp Pre-Orisia Restriction**:
- Yipp can ONLY spawn in dungeons accessible BEFORE meeting Orisia
- His key items (Holy Symbol, Empty Wine Glass) also ONLY spawn pre-Orisia
- Code must check `orisia_met` flag

**Flood's Death**:
- After 2nd dragon boss cutscene, Flood is permanently removed
- Cannot be resurrected by any means
- Equipment drops to inventory
- Hannah screams (FF6 Terra Esper scream recreation)

**Iris's Berserk**:
- Triggers when Fei dies (0 HP) while Iris in party
- Player loses control until Fei is raised
- Shapeshifter: Auto-panda, attacks Fei's killer
- Nature Bound: Random abilities each turn

**Recruitment Deadline**:
- Once player says YES to Orisia's "ready?" question
- All un-recruited optional characters → zombies in final battle

**Fritzzit & Crankpot Pairing**:
- Found together at Imperial City inn (post-kobolds, pre-Orisia)
- BOTH join together OR neither joins
- Cannot recruit individually

## Lore

**Setting**: Dark fantasy world with gunpowder technology (no tech beyond Roman/Three Kingdoms era except gunpowder)

**Main Threat**: Necromantic plague turning kobolds into undead

**Protagonist**: Javin, Queen Kella's Claw (special operative)

**Tone**: Dark fantasy with gallows humor (Terry Pratchett's Discworld style)

**Technology**: High fantasy + guns, grenades, cannons

## Credits

Game design and implementation: Claude Code
Based on: "There Will Be Kobolds" (book)
Inspired by: Final Fantasy 1-6 (Square Enix)
Engine: Pythonista (omz:software)

---

**Version**: 0.1.0 (Pre-Alpha)
**Target Platform**: iOS (Pythonista)
**Development Status**: Early Development
