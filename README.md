# CareerQuest 🎮

A pixel-art RPG career simulation game for Hackiethon.  
Walk around a town, enter buildings, and role-play as a Doctor, Psychologist, Hotel Front Desk agent, or Real Estate Salesperson.

---

## Setup

### Requirements
- Python 3.10+
- pygame
- numpy

### Install dependencies

**Windows (PowerShell)**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pygame numpy
python main.py
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pygame numpy
python3 main.py
```

---

## How to Play

| Key | Action |
|-----|--------|
| `W A S D` or Arrow Keys | Move your character |
| `E` or `Enter` | Enter a building (when nearby) |
| `ESC` | Exit a building / go back |
| Click | Select dialogue choices, buttons |

### Game Flow

1. **Intro Screen** – Choose Boy/Girl and enter your character's name.
2. **World Map** – Walk around and approach one of three buildings:
   - 🏥 **The Clinic** – Choose to be a Doctor or Psychologist
   - 🛋 **The Hotel** – Play as Hotel Front Desk staff
   - 🏡 **The Avenue** – Choose one of three houses to sell (Real Estate)
3. **Career Scene** – Have a 7-turn conversation with your client/patient/guest.
   - Click one of three response options each turn.
   - Better responses earn more points.
4. **Result Screen** – See your rating, feedback, and coins earned.
   - ⭐ Outstanding → 500 coins
   - 👍 Solid Work  → 250 coins
   - 📈 Keep Practising → 100 coins
5. Return to the map and try another career!

---

## File Structure

```
careerquest/
├── main.py          # Entry point — game loop
├── constants.py     # All magic numbers & config
├── assets.py        # NumPy-generated pixel art sprites
├── player.py        # Movable character (NumPy velocity normalisation)
├── world_map.py     # Top-down tile map (NumPy grid)
├── scenes.py        # All scenes: Intro, World, Career, Result
├── game.py          # State machine — wires everything together
├── dialogue.py      # All hardcoded conversation scripts + scoring
└── ui.py            # Reusable UI: buttons, panels, typewriter, input
```

---

## Tech Notes

- **NumPy** is used for:
  - Velocity normalisation (diagonal movement fix)
  - Tile grid generation
  - Procedural pixel-art sprite generation via `surfarray`
  - Star-field generation (random positions & brightness)
- **PyGame** handles rendering, events, and the game loop.
- **No AI API calls** — all dialogue is hardcoded in `dialogue.py`.
