"""The number of zombies will increase over time,
and the player can move left and right to shoot them.
The player has a score that increases by 1 for each zombie killed.
The game ends when a zombie reaches the bottom of the screen."""


"""
Functionnalities

Easy
1. Add highscore in crypted file  DONE
2. Combo score (fast kill some zombies = score *2 *3 etc) DONE
3. Differents zombies have differents stats
4. Set guns more realistics 

Medium
1. Add some special zombies : runner (low hp but fast speed), tank (low speed, high hp, explosion on death), healer (heal nearby zombies)

Hard
1. progressive level : more zombies, more hp, faster
2. visual effects (shake screen when explosion, white bang when shoot, blood particles, rpg smoke, etc)
3. More guns
4. upgrade every x points (100 etc)
"""

import pickle
import pygame
import time
import os
import random
import math
from neocitizen import NeocitiesApi
import urllib.request
from pathlib import Path
import shutil

# pygame setup
pygame.init()

#//* ===== Screen variables =====
screen = pygame.display.set_mode((400, 600))
WIDTH = screen.get_width()
HEIGHT = screen.get_height()


# //* ===== Game variables =====
dt = 0 # delta time (fps)
xsprite = WIDTH / 2
clock = pygame.time.Clock()
fps = 60
font = pygame.font.Font(None, 36)
score_text = font.render("Score: 0", True, "white")
pause = False
running = True
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

#//* ===== Player variables =====
ybullet = 0
xbullet = 0
delay_bullet = 0.125
time_from_last_bullet = time.time()
img_player = 1
score = 0
current_weapon = 0
current_damage = 10
radius_explosion = 75
slow_time = 2
gun = []
next_gun_spawn = time.time() + random.randint(5, 15)
Highscore = []
last_kill = time.time()
burn_damage = 10
FLAMETHROWER_TTL = 3 # time to live for fire bullets


#//* ===== Zombie variables =====
wav_tmp = 0
temps_animation = 0
last_spawn = time.time()
zombies_to_spawn = 0
last_zombie_spawn = time.time()
wave_size = 1
difficulty_level_wave = 0
nb_zombies = 0
burnt_time = 3
spawn_delay = 0

zombies_img = [
    pygame.transform.scale_by(pygame.image.load(os.path.join('zombie', 'zombie1_1.png')), (0.25)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('zombie', 'zombie1_2.png')), (0.25)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('zombie', 'zombie2_1.png')), (0.25)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('zombie', 'zombie2_2.png')), (0.25)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('zombie', 'zombie3_1.png')), (0.25)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('zombie', 'zombie3_2.png')), (0.25)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('zombie', 'zombie4_1.png')), (0.25)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('zombie', 'zombie4_2.png')), (0.25)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('zombie', 'zombie5_1.png')), (0.25)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('zombie', 'zombie5_2.png')), (0.25)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('zombie', 'zombie6_1.png')), (0.25)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('zombie', 'zombie6_2.png')), (0.25))
]
zombies = []

#//* Player images
skin1 = pygame.transform.scale_by(pygame.image.load(os.path.join('player', 'img1.png')), (0.125))
skin2 = pygame.transform.scale_by(pygame.image.load(os.path.join('player', 'img2.png')), (0.125))
bullet = []
bulletimages_small = [
    pygame.transform.scale_by(pygame.image.load(os.path.join('bullet', 'bullet1.png')), (0.065)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('bullet', 'bullet2.png')), (0.065)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('bullet', 'bullet3.png')), (0.065)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('bullet', 'bullet4.png')), (0.065))
]
bulletimages_medium = [
    pygame.transform.scale_by(pygame.image.load(os.path.join('bullet', 'bullet1.png')), (0.1)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('bullet', 'bullet2.png')), (0.1)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('bullet', 'bullet3.png')), (0.1)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('bullet', 'bullet4.png')), (0.1))
]
bulletimages_large = [
    pygame.transform.scale_by(pygame.image.load(os.path.join('bullet', 'bullet1.png')), (0.2)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('bullet', 'bullet2.png')), (0.2)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('bullet', 'bullet3.png')), (0.2)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('bullet', 'bullet4.png')), (0.2))
]
"""
bas1    |  bas2    |  bas3      |  bas4
milieu1 |  milieu2 |  milieu3   |  milieu4
haut1b |  haut2    |  haut3     |  haut4
"""
bulletimages_plasma = []

for i in range(1, 5):
    bulletimages_plasma.append({
        "top": pygame.transform.scale_by(pygame.image.load(f"guns/plasma/Haut_{i}.png").convert_alpha(), (0.2)),
        "middle": pygame.transform.scale_by(pygame.image.load(f"guns/plasma/Milieu_{i}.png").convert_alpha(), (0.2)),
        "bottom": pygame.transform.scale_by(pygame.image.load(f"guns/plasma/Bas_{i}.png").convert_alpha(), (0.2))
    })

bulletimages = bulletimages_small



#//* Functions
#//* File editing
#! file  content :
#! <1st score>; <2nd>; <3rd>; <4th> etc> 
#! max 10 scores
def get_highscore():
    try:
        with open("highscore.zombie", "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return {"score": []}

def set_highscore(highscore, score):
    highscore["score"].append(int(score))
    highscore["score"] = sorted(highscore["score"], reverse=True)[:100]

    with open("highscore.zombie", "wb") as f:
        pickle.dump(highscore, f)

def u():
    data = get_highscore()
    a = NeocitiesApi(api_key=data['a'])

    shutil.copy("highscore.zombie", "highscore.txt")

    try:
        a.upload_files({Path("highscore.txt"): "highscore.txt"})
    finally:
        if os.path.exists("highscore.txt"):
            os.remove("highscore.txt")

def d():
    urllib.request.urlretrieve("https://bushbientotmodo.neocities.org/highscore.txt", "highscore.zombie")

def shoot():
    global time_from_last_bullet
    global delay_bullet
    global current_damage
    global current_weapon
    global xsprite
    global bullet
    global sprite

    if time.time() - time_from_last_bullet > delay_bullet:
        time_from_last_bullet = time.time()
        if current_weapon == 5:
            bullet.append({
                "frame": 0,
                "x": xsprite,
                "y": HEIGHT - sprite.get_height(),
                "anim_time": 0,
                "damage": current_damage,
                "weapon": current_weapon,
                "hit_zombies": [],
                "ttl": FLAMETHROWER_TTL
            })
        else:
            bullet.append({
                "frame": 0,
                "x": xsprite,
                "y": HEIGHT - sprite.get_height(),
                "anim_time": 0,
                "damage": current_damage,
                "weapon": current_weapon,
                "hit_zombies": []
            })

def zombie_create():
    global zombies
    global wave_size
    global wav_tmp
    global zombies_to_spawn
    global last_zombie_spawn
    global difficulty_level_wave
    global nb_zombies
    global spawn_delay
    # new wave
    spawn_delay = max(0.02, 0.2 / (wave_size ** 0.7))
    if len(zombies) == 0 and zombies_to_spawn == 0:
        zombies_to_spawn = wave_size
        print(f"[DEBUG] Nouvelle vague : {wave_size} zombies")
        wav_tmp += 1
        if wave_size < 50 and wav_tmp >= 4:
            wav_tmp = 0
            difficulty_level_wave += 1
            wave_size = int(round(math.exp(difficulty_level_wave), 0)) 
            print(f"[DEBUG] Taille prochaine vague : {wave_size}")

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

# Progressive spawn
def split_frames(surface):
    frames = []
    start_x = None
    for x in range(surface.get_width()):
        transparent_column = True
        for y in range(surface.get_height()):
            if surface.get_at((x, y)).a != 0:
                transparent_column = False
                break

        if not transparent_column and start_x is None:
            start_x = x
        elif transparent_column and start_x is not None:
            width = x - start_x
            frame = surface.subsurface(
                pygame.Rect(
                    start_x,
                    0,
                    width,
                    surface.get_height()
                )
            )
            frames.append(frame.copy())
            start_x = None
    # last frame
    if start_x is not None:
        frame = surface.subsurface(
            pygame.Rect(
                start_x,
                0,
                surface.get_width() - start_x,
                surface.get_height()
            )
        )
        frames.append(frame.copy())
    return frames


#//* Run functions
zombie_create()
d()

#//* Gun images
# explosion of the rpg, when the bullet collides with a zombie, the explosion is animated and then disappears
explosion = split_frames(pygame.transform.scale_by(pygame.image.load(os.path.join('guns', 'explosion.png')), (1)).convert_alpha())
explosions = []

flame = split_frames(pygame.transform.scale_by(pygame.image.load(os.path.join('guns', 'flame.png')), (1)).convert_alpha())
flames = []

m16_frames = split_frames(pygame.transform.scale_by(pygame.image.load(os.path.join('guns', 'M16_anim.png')), (0.2)).convert_alpha())
m249_frames = split_frames(pygame.transform.scale_by(pygame.image.load(os.path.join('guns', 'M249_anim.png')), (0.2)).convert_alpha())
rpg_frames = split_frames(pygame.transform.scale_by(pygame.image.load(os.path.join('guns', 'RPG_anim.png')), (0.2)).convert_alpha())
plasma_frames = split_frames(pygame.transform.scale_by(pygame.image.load(os.path.join('guns', 'Plasma_anim.png')), (0.2)).convert_alpha())
ak_frames = split_frames(pygame.transform.scale_by(pygame.image.load(os.path.join('guns', 'AK-47_anim.png')), (0.2)).convert_alpha())
flamethrower_frames = split_frames(pygame.transform.scale_by(pygame.image.load(os.path.join('guns', 'flame_thrower_anim.png')), (0.2)).convert_alpha())
freeze_gun_frames = split_frames(pygame.transform.scale_by(pygame.image.load(os.path.join('guns', 'freeze_gun_anim.png')), (0.2)).convert_alpha())
grenade_launcher_frames = split_frames(pygame.transform.scale_by(pygame.image.load(os.path.join('guns', 'grenade_launcher_anim.png')), (0.2)).convert_alpha())
sniper_frames = split_frames(pygame.transform.scale_by(pygame.image.load(os.path.join('guns', 'sniper_anim.png')), (0.2)).convert_alpha())

gun_anim = [
    m16_frames,
    m249_frames,
    rpg_frames,
    plasma_frames,
    ak_frames,
    flamethrower_frames,
    freeze_gun_frames,
    grenade_launcher_frames,
    sniper_frames
]


while running:

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt: float = clock.tick(fps) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause = not pause
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                shoot()
    if pause:
        text = font.render("PAUSE", True, "white")
        screen.blit(text, (
            WIDTH // 2 - text.get_width() // 2,
            HEIGHT // 2
        ))

        pygame.display.flip()
        clock.tick(fps)
        continue

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(color="gray")  #! Change gray if you want to change the bg
    
    # Add a wall at x = WIDTH - WIDTH // 5 from up to (bottom - height player)
    pygame.draw.rect(screen, "black", (WIDTH - WIDTH // 5 - 10, 0, 5, HEIGHT - skin1.get_height()))

    if img_player < 10:
        sprite = skin1
    elif 20 > img_player > 10:
        sprite = skin2

    # spawn zombies at the top of the screen and they have the same time btw switching images
    if time.time() - last_spawn > 0.3:
        last_spawn = time.time()
        zombie_create()

    if zombies_to_spawn > 0:
        if len(zombies) < 50:
            if time.time() - last_zombie_spawn >= spawn_delay:
                last_zombie_spawn = time.time()
                r_type = random.randint(0, 5)
                x = random.randint(
                    0,
                    WIDTH - zombies_img[r_type * 2].get_width() - WIDTH // 5
                )
                if nb_zombies % 50 == 0 and nb_zombies != 0:
                    zombies.append({
                        "frame": 0,
                        "x": x,
                        "y": 0,
                        "anim_time": 0,
                        "type": r_type,
                        "width": zombies_img[r_type * 2].get_width() * 2,
                        "height": zombies_img[r_type * 2].get_height() * 2,
                        "hp": 300,
                        "boss": True,
                        "burn_time": 0,
                        "slow_time": 0,
                        "zombie_role": "boss"
                    })
                else:
                    match r_type:
                        case 2:
                            zombies.append({
                                "frame": 0,
                                "x": x,
                                "y": 0,
                                "anim_time": 0,
                                "type": r_type,
                                "width": zombies_img[r_type * 2].get_width(),
                                "height": zombies_img[r_type * 2].get_height(),
                                "hp": 150,
                                "boss": False,
                                "burn_time": 0,
                                "slow_time": 0,
                                "zombie_role": "hp"
                            })
                        case _:
                            zombies.append({
                                "frame": 0,
                                "x": x,
                                "y": 0,
                                "anim_time": 0,
                                "type": r_type,
                                "width": zombies_img[r_type * 2].get_width(),
                                "height": zombies_img[r_type * 2].get_height(),
                                "hp": 100,
                                "boss": False,
                                "burn_time": 0,
                                "slow_time": 0,
                                "zombie_role": "basic"                                
                            })
                nb_zombies += 1
                zombies_to_spawn -= 1

    if zombies:
        
        for z in zombies[:]:
            speed = 50
            if z["boss"]:
                speed = 25
            if z["slow_time"] > 0:
                speed *= 0.5
                z["slow_time"] -= dt

            if z["zombie_role"] == "hp":
                z["y"] += speed * dt * 2/3
            else:
                z["y"] += speed * dt

            if z["burn_time"] > 0:
                z["hp"] -= burn_damage * dt
                z["burn_time"] -= dt
                if z["hp"] <= 0:
                    check_bonus()
                    if z["boss"]:
                        score += 25 * bonus[0]
                    else:
                        score += 1 * bonus[0]
                    zombies.remove(z)

            # if zombies go bottom or touch the player, end of the game            
            if z["y"] + z["height"] >= HEIGHT or (z["y"] + z["height"] > HEIGHT - sprite.get_height() and z["x"] < xsprite + sprite.get_width() and z["x"] + z["width"] > xsprite):

                Highscore = get_highscore()
                set_highscore(Highscore, score)
                lines = [
                    "GAME OVER",
                    "",
                    f"Your score: {score:.1f}",
                    "",
                    f"Best scores :",
                ]
                scores = Highscore["score"]
                for i in range(min(3, len(scores))):
                    lines.append(f"{i+1} - {scores[i]}")
                lines.extend([
                "",
                "Press R to restart or Q to leave"
                ])

                for i, line in enumerate(lines):
                    text = font.render(line, True, "white")
                    screen.blit(
                        text,
                        (
                            WIDTH // 2 - text.get_width() // 2,
                            HEIGHT // 3 - 20 + i * 30
                        )
                    )
                
                pygame.display.flip()
                score = 0
                bulletimages = bulletimages_small
                current_weapon = 0
                # if R pressed, restart the game
                # else running = False
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            break
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                # restart the game
                                zombies = []
                                bullet = []
                                gun = []
                                explosions = []
                                score = 0
                                xsprite = WIDTH / 2
                                current_weapon = 0
                                current_damage = 10
                                delay_bullet = 0.125
                                nb_zombies = 0
                                wave_size = 1
                                wav_tmp = 0
                                difficulty_level_wave = 0
                                zombies_to_spawn = 0
                                last_zombie_spawn = time.time()
                                next_gun_spawn = time.time() + random.randint(5, 15)
                                ice_bullets = False
                                burning_bullets = False
                                piercing_bullets = False
                                break

                            if event.key == pygame.K_q:
                                running = False
                                break
                    else:
                        continue
                    break

            z["anim_time"] += dt
            if z["anim_time"] >= 0.1:
                z["frame"] = 1 - z["frame"]
                z["anim_time"] = 0

    # //*Right to the wall, btw random time, a gun can spawn and the player has to shoot it to get it
    # The frames of the gun animation are in the same image, so we have to split it : each time there is on or more transparents
    # pixels, we have to split the image and get the frames, then we can animate it
    if gun:
        for g in gun[:]:
            g["anim_time"] += dt
            if g["anim_time"] >= 0.1:
                g["frame"] += 1
                if g["frame"] >= len(gun_anim[g["type"]]):
                    g["frame"] = 0
                g["anim_time"] = 0

    if time.time() >= next_gun_spawn:
        r_type = random.randint(0, len(gun_anim) - 1)
        gun.append({
            "frame": 0,
            "x": WIDTH - gun_anim[r_type][0].get_width() - 10,
            "y": 0,
            "anim_time": 0,
            "type": r_type,
            "width": gun_anim[r_type][0].get_width(),
            "height": gun_anim[r_type][0].get_height(),
        })
        next_gun_spawn = time.time() + random.randint(5, 15)


    keys = pygame.key.get_pressed()
    if keys[pygame.K_q] or keys[pygame.K_LEFT]:
        if xsprite <= 0:
            pass
        else:
            xsprite -= 300 * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if xsprite >= WIDTH - sprite.get_width():
            pass
        else:
            xsprite += 300 * dt

    if keys[pygame.K_SPACE]:
        shoot()


    for b in bullet[:]:
        if b["weapon"] == 3:
            b["y"] -= 750 * dt
        else:
            b["y"] -= 500 * dt
        b["anim_time"] += dt
        if b["weapon"] == 3:
            if b["anim_time"] >= 0.08:
                b["frame"] += 1
                b["anim_time"] = 0
            if b["frame"] >= 4:
                b["frame"] = 0
        elif b["weapon"] == 8:
            if b["anim_time"] >= 0.1:
                b["frame"] += 1
                b["anim_time"] = 0
            if b["frame"] >= len(bulletimages):
                b["frame"] = 0
        elif b["weapon"] == 5:
            if b["anim_time"] >= 0.05:
                b["frame"] += 1
                b["anim_time"] = 0
            if b["frame"] >= len(flame):
                b["frame"] = 0
        else:
            if b["anim_time"] >= 0.1:
                b["frame"] += 1
                b["anim_time"] = 0
            if b["frame"] >= len(bulletimages):
                b["frame"] = 0
        if b["y"] < 0:
            bullet.remove(b)

    if explosions:
        for exp in explosions[:]:
            exp["anim_time"] += dt
            if exp["anim_time"] >= 0.05:
                exp["frame"] += 1
                exp["anim_time"] = 0
            if exp["frame"] >= len(explosion):
                explosions.remove(exp)
    if flames:
        for fl in flames[:]:
            fl["anim_time"] += dt
            if fl["anim_time"] >= 0.05:
                fl["frame"] += 1
                fl["anim_time"] = 0
            if fl["frame"] >= len(flame):
                flames.remove(fl)
    if gun:
        for g in gun[:]:
            g["y"] += 100 * dt
            if g["y"] > HEIGHT:
                gun.remove(g)

    screen.blit(sprite, (xsprite, HEIGHT - sprite.get_height()))
    for b in bullet:
        if b["weapon"] == 3:
            frame = bulletimages_plasma[b["frame"]]
            screen.blit(frame["top"],(b["x"], b["y"]))
            screen.blit(frame["middle"],(b["x"], b["y"] + frame["top"].get_height()))
            screen.blit(frame["bottom"],(b["x"],b["y"] + frame["top"].get_height() + frame["middle"].get_height()))
        elif b["weapon"] == 5:
            screen.blit(flame[b["frame"] % len(flame)],(b["x"], b["y"]))
        else:
            screen.blit(  bulletimages[b["frame"]],(b["x"], b["y"]))

    for z in zombies:
        img = zombies_img[z["type"] * 2 + z["frame"]]

        if z["boss"]:
            img = pygame.transform.scale_by(img, 2)

        if z["burn_time"] > 0:

            # Red flashes when burning
            if z["burn_time"] > 0 and int(time.time() * 10) % 2 == 0:
                img = img.copy()

                img.fill(
                    (255, 0, 0),
                    special_flags=pygame.BLEND_RGB_ADD
                )

        screen.blit(img, (z["x"], z["y"]))

        pygame.draw.rect(
            screen,
            "red",
            (z["x"], z["y"] + z["height"] + 5, z["width"], 5)
        )
        
        match z["zombie_role"]:
            case "hp": 
                max_hp = 150
            case "boss":
                max_hp = 300

            case _:
                max_hp = 100
            
        pygame.draw.rect(
            screen,
            "green",
            (z["x"], z["y"] + z["height"] + 5, z["width"] * z["hp"] / max_hp, 5))


    for g in gun:
        screen.blit(gun_anim[g["type"]][g["frame"]],(g["x"], g["y"]))
    for exp in explosions:
        screen.blit(explosion[exp["frame"]], (exp["x"], exp["y"]))

    # despawn zombies when bullet collides with them
    if bullet and zombies:
        for b in bullet[:]:
            for z in zombies[:]:
                if b["weapon"] == 3:
                    frame = bulletimages_plasma[b["frame"]]

                    width = frame["middle"].get_width()

                    height = (
                        frame["top"].get_height()
                        + frame["middle"].get_height()
                        + frame["bottom"].get_height()
                    )

                elif b["weapon"] == 5:
                    width = flame[b["frame"]].get_width()
                    height = flame[b["frame"]].get_height()

                else:
                    width = bulletimages[b["frame"]].get_width()
                    height = bulletimages[b["frame"]].get_height()


                bullet_rect = pygame.Rect(b["x"],b["y"],width,height)
                zombie_rect = pygame.Rect(z["x"], z["y"], z["width"], z["height"])
                if bullet_rect.colliderect(zombie_rect):
                    try:
                        if b["weapon"] == 8:
                            if z in b["hit_zombies"]:
                                continue
                            b["hit_zombies"].append(z)
                        z["hp"] -= b["damage"]
                        if b["weapon"] == 6:
                            z["slow_time"] = slow_time
                        if b["weapon"] == 5:
                            if b["ttl"] > 0:
                                z["burn_time"] = burnt_time
                                b["ttl"] -= 1
                            else:
                                bullet.remove(b)
                                continue
                        
                        if b["weapon"] == 2 or b["weapon"] == 7:
                            explosion_x = z["x"]
                            explosion_y = z["y"]
                            explosions.append({
                                "x": explosion_x,
                                "y": explosion_y,
                                "frame": 0,
                                "anim_time": 0
                            })
                            for z2 in zombies[:]:
                                dx = z2["x"] - explosion_x
                                dy = z2["y"] - explosion_y
                                distance = (dx * dx + dy * dy) ** 0.5
                                if distance <= radius_explosion:
                                    z2["hp"] -= b["damage"]
                                    if z2["hp"] <= 0:
                                        check_bonus()
                                        if z2["boss"]:
                                            score += 25 * bonus[0]
                                        else:
                                            score += 1 * bonus[0]
                                        if z2 in zombies:
                                            zombies.remove(z2)
                            if b in bullet:
                                bullet.remove(b)
                            continue

                        if z["hp"] <= 0:
                            check_bonus()
                            if z["boss"]:
                                score += 25 * bonus[0]
                            else:
                                score += 1 * bonus[0]
                            zombies.remove(z)
                            continue 
                        if b["weapon"] != 8 and b["weapon"] != 5:
                            bullet.remove(b)

                    except ValueError:
                        pass
    # if gun collides with player, the player get the gun and it despawn
    if gun:
        for g in gun[:]:
            gun_rect = pygame.Rect(g["x"], g["y"], g["width"], g["height"])
            if gun_rect.colliderect(pygame.Rect(xsprite, HEIGHT - sprite.get_height(), sprite.get_width(), sprite.get_height())):
                gun.remove(g)
                for b in bullet[:]:
                    if b in bullet:
                        bullet.remove(b)
                if g["type"] == 0:
                    current_damage = 25
                    delay_bullet = 0.18   # M16
                    bulletimages = bulletimages_small
                    current_weapon = 0
                elif g["type"] == 1:
                    current_damage = 12
                    delay_bullet = 0.08    # M249
                    bulletimages = bulletimages_small
                    current_weapon = 1
                elif g["type"] == 2:
                    current_damage = 100
                    delay_bullet = 1.5     # RPG
                    bulletimages = bulletimages_large
                    current_weapon = 2
                    radius_explosion = 120
                elif g["type"] == 3:
                    current_damage = 40
                    delay_bullet = 0.35    # Plasma
                    current_weapon = 3
                elif g["type"] == 4:
                    current_damage = 35
                    delay_bullet = 0.12     # AK-47
                    bulletimages = bulletimages_small
                    current_weapon = 4
                elif g["type"] == 5:
                    current_damage = 0.5
                    delay_bullet = 0.05     # Flamethrower
                    bulletimages = bulletimages_large
                    current_weapon = 5
                    burning_bullets = True
                    burn_damage = 10
                    burnt_time = 3
                    piercing_bullets = True
                elif g["type"] == 6:
                    current_damage = 20
                    delay_bullet = 0.12     # Freeze gun
                    bulletimages = bulletimages_medium
                    current_weapon = 6
                    ice_bullets = True
                    slow_factor = 0.5
                    slow_time = 2
                elif g["type"] == 7:
                    current_damage = 70
                    delay_bullet = 0.7     # Grenade launcher
                    bulletimages = bulletimages_large
                    current_weapon = 7
                    radius_explosion = 90
                elif g["type"] == 8:
                    current_damage = 300
                    delay_bullet = 1.2     # Sniper
                    bulletimages = bulletimages_medium
                    current_weapon = 8
                    piercing_bullets = True
                print(f"[DEBUG] Le joueur a ramassé une arme (type = {g['type']})")


    for fl in flames:
        screen.blit(
            flame[fl["frame"]],
            (fl["x"], fl["y"])
        )


    # display score (zombie = 1 pt)
    if score:
        score_text = font.render(f"Score: {score:.1f}           Bonus : x{bonus[0]}", True, "white") if bonus[0] >1 else font.render(f"Score: {score:.1f}", True, "white")
    screen.blit(score_text, (10, 10))

    # flip() the display to put your work on screen
    pygame.display.flip()

    if img_player < 20:
        img_player += 50 * dt
    else:    
        img_player = 1

pygame.quit()

# future API to upload the best scores online.
u()