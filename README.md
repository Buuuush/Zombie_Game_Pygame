# Zombie Game

## Gameplay

Zombie Survival is based on simple concept: survive as long as possible against endless waves of zombies.

Player can move horizontally across bottom of screen and eliminate incoming enemies before they reach player position or bottom of map. As game progresses, waves become larger and more difficult, requiring efficient weapon management and quick reactions.

Random weapon drops provide temporary upgrades and introduce different playstyles throughout each run.

```python
wave_size = int(round(math.exp(level), 0))
```

## Enemy Types

Game currently includes several zombie variants with different characteristics.

### Basic Zombie

Standard enemy with balanced movement speed and health.

### Heavy Zombie

Slower zombie with increased health, requiring more damage to eliminate.

### Boss Zombie

Bosses appear periodically throughout game.

Characteristics:

- Increased health pool
- Larger size
- Reduced movement speed
- Higher score reward

## Scoring System

Each zombie eliminated grants points.

- Standard zombies reward 1 point
- Boss zombies reward 25 points

Game also includes combo multiplier system. Consecutive kills performed within short time window gradually increase score multiplier, rewarding aggressive and accurate gameplay.

## Wave Progression

Enemy waves grow over time using exponential progression model.

As wave number increases:

- More zombies spawn
- Spawn intervals become shorter
- Higher enemy density increases difficulty

## Weapons

Game features 9 weapons with unique characteristics:

1. **M16** - Standard assault rifle, balanced stats
2. **M249** - Light machine gun, high fire rate, lower damage
3. **RPG** - Explosive area damage, slow fire rate
4. **Plasma Gun** - High projectile speed, unique plasma bullet animation
5. **AK-47** - Assault rifle, moderate stats
6. **Flamethrower** - Burn damage over time, piercing projectiles
7. **Freeze Gun** - Slows enemies on hit
8. **Grenade Launcher** - Explosive area damage
9. **Sniper Rifle** - Piercing projectiles, very high damage, slow fire rate

Weapons drop randomly from right wall and must be shot to collect.

## Status Effects

- **Burn**: Damage over time applied by Flamethrower and RPG explosions
- **Slow**: Movement speed reduction applied by Freeze Gun

## High Score System

Game features persistent high score system.

Features:

- Local score saving using binary pickle format (`highscore.zombie`)
- Top 100 scores stored
- Online leaderboard synchronization using Neocities

Scores are automatically loaded when game starts and updated when run ends.

## Technical Features

Project developed to explore several game programming concepts using Pygame.

Implemented systems include:

- Sprite animation with frame-based timing
- Delta-time movement for framerate independence
- Collision detection using pygame.Rect
- Procedural wave generation with exponential difficulty scaling
- Combo and multiplier system with time-based decay
- Weapon pickup system with random drops
- Status effects (burn and slow)
- Animated explosions and particle effects
- Local and online score persistence

## Project Structure

```text
player/
├── Player sprites (img1.png, img2.png)

zombie/
├── Zombie sprites and animations (6 types, 2 frames each)

bullet/
├── Projectile sprites (bullet1.png - bullet4.png)

guns/
├── Weapon animation frames
├── Explosion effects (explosion.png)
├── Flamethrower effects (flame.png)
└── Plasma gun frames (Haut, Milieu, Bas)

main.py
├── Main game loop and logic

py_files/
├── assets.py      - Image loading and frame splitting
├── player.py      - Player logic, shooting, combo system
├── zombies.py     - Zombie spawning and wave management
├── utils.py       - Shared constants and helper functions
├── save.py        - High score persistence and Neocities sync

highscore.zombie
├── Saved leaderboard data (pickle format)

config/
├── config.json    - Weapon configuration data
```

## Requirements

- Python 3.11 or newer
- Pygame (or pygame-ce)

Install virtualenv:

Linux:

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv

.venv/Scripts/activate
```

Optional:

- neocitizen (for online leaderboard)

Install dependencies:

```bash
pip install pygame neocitizen
```

> Note: Make sure virtualenv is activated before installing.

## Future Improvements

Planned features include:

- [x] More maintenable code (don't look at the old code ^^)
- [ ] Sound effects
- [ ] Background music
- [ ] Additional zombie classes (runner, tank, healer)
- [ ] Upgrade and progression system
- [ ] Additional weapons
- [ ] Improved visual effects (screen shake, blood particles, smoke)
- [ ] Better game balancing
- [ ] More boss mechanics

## Author

I'm **Buuuush**, French dev student and I created this game during my internship because I was bored :D

More updates are coming! (I added my highscore, feel free to beat it) ^^
