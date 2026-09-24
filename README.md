# Zombie Game

## Gameplay

Zombie Survival is based on a simple concept: survive for as long as possible against endless waves of zombies.

The player can move horizontally across the bottom of the screen and eliminate incoming enemies before they reach the player's position or the bottom of the map. As the game progresses, waves become larger and more difficult, requiring efficient weapon management and quick reactions.

Random weapon drops provide temporary upgrades and introduce different playstyles throughout each run.

## Enemy Types

The game currently includes several zombie variants with different characteristics.

### Basic Zombie

The standard enemy with balanced movement speed and health.

### Heavy Zombie

A slower zombie with increased health, requiring more damage to eliminate.

### Boss Zombie

Bosses appear periodically throughout the game.

Characteristics:

- Increased health pool
- Larger size
- Reduced movement speed
- Higher score reward

## Scoring System

Each zombie eliminated grants points.

- Standard zombies reward 1 point
- Boss zombies reward 25 points

The game also includes a combo multiplier system. Consecutive kills performed within a short time window gradually increase the score multiplier, rewarding aggressive and accurate gameplay.


## Wave Progression

Enemy waves grow over time using an exponential progression model.

```python
wave_size = int(round(math.exp(level), 0))
```

As the wave number increases:

- More zombies spawn
- Spawn intervals become shorter
- Higher enemy density increases difficulty


## Weapon Effects

Several weapons provide special gameplay mechanics beyond direct damage.

- **RPG**: explosive area damage
- **Grenade Launcher**: explosive area damage
- **Flamethrower**: burn damage over time
- **Freeze Gun**: slows enemies
- **Sniper Rifle**: piercing projectiles
- **Plasma Gun**: high projectile speed

These effects encourage players to adapt their strategy depending on the current situation.


## High Score System

The game features a persistent high score system.

Features:

- Local score saving
- Top 100 scores stored
- Binary save file (`highscore.zombie`)
- Online leaderboard synchronization using Neocities

Scores are automatically loaded when the game starts and updated when a run ends.


## Technical Features

The project was developed to explore several game programming concepts using Pygame.

Implemented systems include:

- Sprite animation
- Delta-time movement
- Collision detection
- Procedural wave generation
- Combo and multiplier system
- Weapon pickup system
- Status effects (burn and slow)
- Animated explosions
- Local and online score persistence


## Project Structure

```text
player/
├── Player sprites

zombie/
├── Zombie sprites and animations

bullet/
├── Projectile sprites

guns/
├── Weapon assets
├── Weapon animations
├── Explosion effects
└── Flamethrower effects

main.py
├── Main game logic

highscore.zombie
├── Saved leaderboard data
```


## Requirements

- Python 3.11 or newer
- Pygame

Optional:

- pygame-ce
- neocitizen

Install dependencies:

```bash
pip install pygame neocitizen
```


## Future Improvements

Planned features include:

- [ ] Sound effects
- [ ] Background music
- [ ] Additional zombie classes (runner, tank, healer)
- [ ] Upgrade and progression system
- [ ] Additional weapons
- [ ] Improved visual effects
- [ ] Better game balancing
- [ ] More boss mechanics

## Author

I'm **Buuuush**, a French dev student and I created this game during my internship because I was bored :D

More updates are coming ! (I added my highscore, feel free to beat it) ^^