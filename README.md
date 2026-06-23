# 🧟 Zombie Survival

A small arcade zombie shooter made with **Python** and **Pygame**.

Survive endless waves of zombies, collect weapons, improve your firepower and try to achieve the highest score possible before the horde reaches you.

---

## 🎮 Features

- 🧟 Progressive zombie waves
- 📈 Exponential difficulty scaling
- 🔫 Multiple weapon pickups
- 💥 RPG with area damage explosions
- ❤️ Zombie health system
- 🎯 Score tracking
- ⏸ Pause menu (`ESC`)
- 🎞 Animated player, zombies, weapons and explosions
- ⚡ Different fire rates and damage values depending on the weapon

---

## 🛠 Weapons

| Weapon | Damage | Fire Rate |
|----------|----------|----------|
| M16 | 10 | Medium |
| M249 | 5 | Very Fast |
| RPG | 75 | Slow |
| Plasma Gun | 5 | Extremely Fast |

Weapons spawn randomly during gameplay.

Collect them by touching the weapon pickup.

---

## 🎯 Controls (AZERTY) --> QWERTY = A & D

| Key | Action |
|------|------|
| `Q` | Move Left |
| `D` | Move Right |
| `SPACE` | Shoot |
| `ESC` | Pause / Resume |

---

## 🧟 Enemy System

Zombies:

- Spawn in waves
- Have health points
- Become increasingly numerous
- End the game if they:
  - Reach the bottom of the screen
  - Touch the player

Wave progression uses an exponential growth system ^^ :

```python
wave_size = int(round(math.exp(e), 0))
```

---

## 🖼 Assets

The project uses custom sprites for:

- Player
- Zombies
- Weapons
- Bullets
- Explosions

Assets are loaded from the following folders:

```text
player/
zombie/
bullet/
guns/
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/zombie-survival.git
cd zombie-survival
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install pygame
```

Run the game:

```bash
python main.py
```

---

## 📋 Future Ideas

- Boss zombies
- More weapons
- Sound effects
- Music