import time
import random
import py_files.utils as utils
#//* ===== Player variables =====
ybullet = 0
xbullet = 0
delay_bullet = 0.125
time_from_last_bullet = time.time()
img_player = 1
score = 0
current_weapon = 0
current_damage = 10
gun = []
next_gun_spawn = time.time() + random.randint(5, 15)
Highscore = []
last_kill = time.time()

bullet = []
zombies_before_bonus = [
    5,
    8,
    12,
    16,
    21,
    27,
    34,
    42,
    51,
    61,
    72,
    84,
    97,
    111,
    126
]
bonus = [1,zombies_before_bonus[0]]

# //* ===== Game variables =====


def shoot(sprite_height):
    global time_from_last_bullet
    global delay_bullet
    global current_damage
    global current_weapon
    global bullet

    if time.time() - time_from_last_bullet > delay_bullet:
        time_from_last_bullet = time.time()
        bullet_x = utils.xsprite
        if current_weapon == 5:
            bullet.append({
                "frame": 0,
                "x": bullet_x,
                "y": utils.HEIGHT - sprite_height,
                "anim_time": 0,
                "damage": current_damage,
                "weapon": current_weapon,
                "hit_zombies": [],
                "ttl": utils.FLAMETHROWER_TTL
            })
        else:
            bullet.append({
                "frame": 0,
                "x": bullet_x,
                "y": utils.HEIGHT - sprite_height,
                "anim_time": 0,
                "damage": current_damage,
                "weapon": current_weapon,
                "hit_zombies": []
            })

def check_bonus():
    global bonus
    global last_kill
    global zombies_before_bonus

    current_kill = time.time()
    if current_kill - last_kill <= 2:
        if bonus[1] == 0:
            bonus[0] += 0.5

            index = int(bonus[0] *2 -1)
            if index >= len(zombies_before_bonus):
                index = len(zombies_before_bonus)-1
            
            bonus[1] = zombies_before_bonus[index]
        else:
            bonus[1] -= 1
    else:
        bonus = [1,zombies_before_bonus[0]]
    last_kill = current_kill