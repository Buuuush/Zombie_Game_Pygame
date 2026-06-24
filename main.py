"""The number of zombies will increase over time,
and the player can move left and right to shoot them.
The player has a score that increases by 1 for each zombie killed.
The game ends when a zombie reaches the bottom of the screen."""

import pygame
import time
import os
import random
import math

print("[DEBUG] Initialisation de Pygame et configuration initiale")
# pygame setup
pygame.init()
screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()
running = True
dt = 0
ybullet = 0
xbullet = 0
img_player = 1
fps = 60
temps_animation = 0
time_from_last_bullet = time.time()
last_spawn = time.time()
zombies_to_spawn = 0
last_zombie_spawn = time.time()
WIDTH = screen.get_width()
HEIGHT = screen.get_height()
xsprite = WIDTH / 2
score = 0
go = True
delay_bullet = 0.125
font = pygame.font.Font(None, 36)
wave_size = 1
score_text = font.render("Score: 0", True, "white")
wav_tmp = 0
e = 0
current_weapon = 5
pause = False
current_damage = 10
nb_zombies = 0
radius_explosion = 75
slow_time = 2
burnt_time = 3
burn_damage = 15

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
def zombie_create():
    global zombies
    global wave_size
    global wav_tmp
    global zombies_to_spawn
    global last_zombie_spawn
    global e
    global nb_zombies

    # Nouvelle vague        
    spawn_delay = max(0.002, 0.2 / (wave_size ** 0.7))
    if len(zombies) == 0 and zombies_to_spawn == 0:
        zombies_to_spawn = wave_size
        print(f"[DEBUG] Nouvelle vague : {wave_size} zombies")
        wav_tmp += 1
        if wave_size < 50 and wav_tmp >= 4:
            wav_tmp = 0
            e += 1
            wave_size = int(round(math.exp(e), 0)) 
            print(f"[DEBUG] Taille prochaine vague : {wave_size}")

    # Spawn progressif

zombie_create()

skin1 = pygame.transform.scale_by(pygame.image.load(os.path.join('player', 'img1.png')), (0.125))
skin2 = pygame.transform.scale_by(pygame.image.load(os.path.join('player', 'img2.png')), (0.125))
# multiple bullets
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

# Bullet of plasma are in the folder guns/plasma:
"""
bas1    |  bas2    |  bas3      |  bas4
milieu1 |  milieu2 |  milieu3   |  milieu4
haut1b |  haut2    |  haut3     |  haut4"""


bulletimages_plasma = []

for i in range(1, 5):
    bulletimages_plasma.append({
        "top": pygame.transform.scale_by(pygame.image.load(f"guns/plasma/Haut_{i}.png").convert_alpha(), (0.2)),
        "middle": pygame.transform.scale_by(pygame.image.load(f"guns/plasma/Milieu_{i}.png").convert_alpha(), (0.2)),
        "bottom": pygame.transform.scale_by(pygame.image.load(f"guns/plasma/Bas_{i}.png").convert_alpha(), (0.2))
    })


bulletimages = bulletimages_small

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
    # dernière frame
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


# explosion of the rpg, when the bullet collides with a zombie, the explosion is animated and then disappears
explosion = split_frames(pygame.transform.scale_by(pygame.image.load(os.path.join('guns', 'explosion.png')), (1)).convert_alpha())
explosions = []

flame = split_frames(pygame.transform.scale_by(pygame.image.load(os.path.join('guns', 'flame.png')), (1)).convert_alpha())
flames = []

gun = []

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

next_gun_spawn = time.time() + random.randint(5, 15)


print("[DEBUG] Entrée dans la boucle de jeu principale")

while running:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause = not pause

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
    screen.fill(color="fuchsia")
    
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
        if len(zombies) < 20:
            if time.time() - last_zombie_spawn >= 0.2:
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
                        "slow_time": 0
                    })
                else:
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
                        "slow_time": 0
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

            z["y"] += speed * dt

            if z["burn_time"] > 0:
                z["hp"] -= 15 * dt
                z["burn_time"] -= dt
                if z["hp"] <= 0:
                    if z["boss"]:
                        score += 25
                    else:
                        score += 1
                    zombies.remove(z)
            # if zombies go bottom or touch the player, end of the game

            if z["y"] > HEIGHT or (z["y"] + z["height"] > HEIGHT - sprite.get_height() and z["x"] < xsprite + sprite.get_width() and z["x"] + z["width"] > xsprite):


                lines = [
                    "GAME OVER",
                    "",
                    f"Score: {score}",
                    "",
                    "Press R to restart"
                ]

                for i, line in enumerate(lines):
                    text = font.render(line, True, "white")
                    screen.blit(
                        text,
                        (
                            WIDTH // 2 - text.get_width() // 2,
                            HEIGHT // 2 - 80 + i * 40
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
                                e = 0
                                zombies_to_spawn = 0
                                last_zombie_spawn = time.time()
                                next_gun_spawn = time.time() + random.randint(5, 15)
                                break
                    else:
                        continue
                    break

            z["anim_time"] += dt
            if z["anim_time"] >= 0.1:
                z["frame"] = 1 - z["frame"]
                z["anim_time"] = 0

    # Right to the wall, btw random time, a gun can spawn and the player has to shoot it to get it
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
                    "hit_zombies": []
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

            # clignotement rouge
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
        if z["boss"]:
            max_hp = 300
        else:
            max_hp = 100

        pygame.draw.rect(screen,"green",(z["x"], z["y"] + z["height"] + 5, z["width"] * z["hp"] / max_hp, 5))


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
                            z["burn_time"] = burnt_time
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
                                        if z2["boss"]:
                                            score += 25
                                        else:
                                            score += 1
                                        if z2 in zombies:
                                            zombies.remove(z2)
                            if b in bullet:
                                bullet.remove(b)
                            continue

                        if z["hp"] <= 0:
                            if z["boss"]:
                                score += 25
                            else:
                                score += 1
                            zombies.remove(z)
                            continue 
                        if b["weapon"] != 8:
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
                    delay_bullet = 0.02     # Flamethrower
                    bulletimages = bulletimages_large
                    current_weapon = 5
                    burning_bullets = True
                    burn_damage = 15
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
        score_text = font.render(f"Score: {score}", True, "white")
    screen.blit(score_text, (10, 10))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt: float = clock.tick(fps) / 1000
    if img_player < 20:
        img_player += 50 * dt
    else:
        img_player = 1

print("[DEBUG] Arrêt de Pygame et fermeture du programme")
pygame.quit()