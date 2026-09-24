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

import pygame
import time
import random

#//* ===== Screen variables =====
pygame.init()
screen = pygame.display.set_mode((400, 600))
WIDTH = screen.get_width()
HEIGHT = screen.get_height()

#//* ===== File import =====
import py_files.utils as utils

WIDTH = utils.WIDTH
HEIGHT = utils.HEIGHT
#//* ===== Variables =====

import py_files.save as save
import py_files.player as player
import py_files.zombies as zombies_data
import py_files.assets as assets


#//* Run functions
zombies_data.zombie_create()
save.d()

def restart():
    zombies_data.zombies = []
    player.bullet = []
    player.gun = []
    assets.explosions = []
    player.score = 0
    utils.xsprite = WIDTH / 2
    player.current_weapon = 0
    player.current_damage = 10
    player.delay_bullet = 0.125
    zombies_data.nb_zombies = 0
    zombies_data.wave_size = 1
    zombies_data.wav_tmp = 0
    zombies_data.difficulty_level_wave = 0
    zombies_data.zombies_to_spawn = 0
    zombies_data.last_zombie_spawn = time.time()
    player.next_gun_spawn = time.time() + random.randint(5, 15)
    utils.ice_bullets = False
    utils.burning_bullets = False
    utils.piercing_bullets = False

while utils.running:
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt: float = utils.clock.tick(utils.fps) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            utils.running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                utils.pause = not utils.pause
    if utils.pause:
        text = utils.font.render("PAUSE", True, "white")
        screen.blit(text, (
            WIDTH // 2 - text.get_width() // 2,
            HEIGHT // 2
        ))

        pygame.display.flip()
        utils.clock.tick(utils.fps)
        continue

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(color="gray")  #! Change gray if you want to change the bg
    
    # Add a wall at x = WIDTH - WIDTH // 5 from up to (bottom - height player)
    pygame.draw.rect(screen, "black", (WIDTH - WIDTH // 5 - 10, 0, 5, HEIGHT - assets.skin1.get_height()))

    if player.img_player < 10:
        sprite = assets.skin1
    elif 20 > player.img_player > 10:
        sprite = assets.skin2

    # spawn zombies at the top of the screen and they have the same time btw switching images
    if time.time() - zombies_data.last_spawn > 0.3:
        zombies_data.last_spawn = time.time()
        zombies_data.zombie_create()

    if zombies_data.zombies_to_spawn > 0:
        if len(zombies_data.zombies) < 50:
            if time.time() - zombies_data.last_zombie_spawn >= utils.spawn_delay:
                zombies_data.last_zombie_spawn = time.time()
                r_type = random.randint(0, 5)
                x = random.randint(
                    0,
                    WIDTH - assets.zombies_img[r_type * 2].get_width() - WIDTH // 5
                )
                if zombies_data.nb_zombies % 50 == 0 and zombies_data.nb_zombies != 0:
                    zombies_data.zombies.append({
                        "frame": 0,
                        "x": x,
                        "y": 0,
                        "anim_time": 0,
                        "type": r_type,
                        "width": assets.zombies_img[r_type * 2].get_width() * 2,
                        "height": assets.zombies_img[r_type * 2].get_height() * 2,
                        "hp": 300,
                        "boss": True,
                        "burn_time": 0,
                        "slow_time": 0,
                        "zombie_role": "boss"
                    })
                else:
                    match r_type:
                        case 2:
                            zombies_data.zombies.append({
                                "frame": 0,
                                "x": x,
                                "y": 0,
                                "anim_time": 0,
                                "type": r_type,
                                "width": assets.zombies_img[r_type * 2].get_width(),
                                "height": assets.zombies_img[r_type * 2].get_height(),
                                "hp": 150,
                                "boss": False,
                                "burn_time": 0,
                                "slow_time": 0,
                                "zombie_role": "hp"
                            })
                        case _:
                            zombies_data.zombies.append({
                                "frame": 0,
                                "x": x,
                                "y": 0,
                                "anim_time": 0,
                                "type": r_type,
                                "width": assets.zombies_img[r_type * 2].get_width(),
                                "height": assets.zombies_img[r_type * 2].get_height(),
                                "hp": 100,
                                "boss": False,
                                "burn_time": 0,
                                "slow_time": 0,
                                "zombie_role": "basic"                                
                            })
                zombies_data.nb_zombies += 1
                zombies_data.zombies_to_spawn -= 1

    if zombies_data.zombies:
        
        for z in zombies_data.zombies[:]:
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
                z["hp"] -= utils.burn_damage * dt
                z["burn_time"] -= dt
                if z["hp"] <= 0:
                    player.check_bonus()
                    if z["boss"]:
                        player.score += 25 * player.bonus[0]
                    else:
                        player.score += 1 * player.bonus[0]
                    zombies_data.zombies.remove(z)

            # if zombies go bottom or touch the player, end of the game            
            if z["y"] + z["height"] >= HEIGHT or (z["y"] + z["height"] > HEIGHT - sprite.get_height() and z["x"] < utils.xsprite + sprite.get_width() and z["x"] + z["width"] > utils.xsprite):

                Highscore = save.get_highscore()
                save.set_highscore(Highscore, player.score)
                lines = [
                    "GAME OVER",
                    "",
                    f"Your score: {player.score:.1f}",
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
                    text = utils.font.render(line, True, "white")
                    screen.blit(
                        text,
                        (
                            WIDTH // 2 - text.get_width() // 2,
                            HEIGHT // 3 - 20 + i * 30
                        )
                    )
                
                pygame.display.flip()
                player.score = 0
                assets.bulletimages = assets.bulletimages_small
                player.current_weapon = 0
                # if R pressed, restart the game
                # else running = False
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            utils.running = False
                            break
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                # restart the game
                                restart()
                                break

                            if event.key == pygame.K_q:
                                utils.running = False
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
    if player.gun:
        for g in player.gun[:]:
            g["anim_time"] += dt
            if g["anim_time"] >= 0.1:
                g["frame"] += 1
                if g["frame"] >= len(assets.gun_anim[g["type"]]):
                    g["frame"] = 0
                g["anim_time"] = 0

    if time.time() >= player.next_gun_spawn:
        r_type = random.randint(0, len(assets.gun_anim) - 1)
        player.gun.append({
            "frame": 0,
            "x": WIDTH - assets.gun_anim[r_type][0].get_width() - 10,
            "y": 0,
            "anim_time": 0,
            "type": r_type,
            "width": assets.gun_anim[r_type][0].get_width(),
            "height": assets.gun_anim[r_type][0].get_height(),
        })
        player.next_gun_spawn = time.time() + random.randint(5, 15)


    keys = pygame.key.get_pressed()
    if keys[pygame.K_q] or keys[pygame.K_LEFT]:
        if utils.xsprite <= 0:
            pass
        else:
            utils.xsprite -= 300 * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if utils.xsprite >= WIDTH - sprite.get_width():
            pass
        else:
            utils.xsprite += 300 * dt

    if keys[pygame.K_SPACE]:
        player.shoot(sprite.get_height())

    for b in player.bullet[:]:
        if b["weapon"] == 3:
            b["y"] -= 750 * dt
        else:
            b["y"] -= 500 * dt
        b["anim_time"] += dt
        match b["weapon"]:
            case 3:
                if b["anim_time"] >= 0.08:
                    b["frame"] += 1
                    b["anim_time"] = 0
                if b["frame"] >= 4:
                    b["frame"] = 0
            case 8:
                if b["anim_time"] >= 0.1:
                    b["frame"] += 1
                    b["anim_time"] = 0
                if b["frame"] >= len(assets.bulletimages):
                    b["frame"] = 0
            case 5:
                if b["anim_time"] >= 0.05:
                    b["frame"] += 1
                    b["anim_time"] = 0
                if b["frame"] >= len(assets.flame):
                    b["frame"] = 0
            case _:
                if b["anim_time"] >= 0.1:
                    b["frame"] += 1
                    b["anim_time"] = 0
                if b["frame"] >= len(assets.bulletimages):
                    b["frame"] = 0
        if b["y"] < 0:
            player.bullet.remove(b)

    if assets.explosions:
        for exp in assets.explosions[:]:
            exp["anim_time"] += dt
            if exp["anim_time"] >= 0.05:
                exp["frame"] += 1
                exp["anim_time"] = 0
            if exp["frame"] >= len(assets.explosion):
                assets.explosions.remove(exp)
    if assets.flames:
        for fl in assets.flames[:]:
            fl["anim_time"] += dt
            if fl["anim_time"] >= 0.05:
                fl["frame"] += 1
                fl["anim_time"] = 0
            if fl["frame"] >= len(assets.flame):
                assets.flames.remove(fl)
    if player.gun:
        for g in player.gun[:]:
            g["y"] += 100 * dt
            if g["y"] > HEIGHT:
                player.gun.remove(g)

    screen.blit(sprite, (utils.xsprite, HEIGHT - sprite.get_height()))
    for b in player.bullet:
        if b["weapon"] == 3:
            frame = assets.bulletimages_plasma[b["frame"]]
            screen.blit(frame["top"],(b["x"], b["y"]))
            screen.blit(frame["middle"],(b["x"], b["y"] + frame["top"].get_height()))
            screen.blit(frame["bottom"],(b["x"],b["y"] + frame["top"].get_height() + frame["middle"].get_height()))
        elif b["weapon"] == 5:
            screen.blit(assets.flame[b["frame"] % len(assets.flame)],(b["x"], b["y"]))
        else:
            screen.blit(assets.bulletimages[b["frame"]],(b["x"], b["y"]))

    for z in zombies_data.zombies:
        img = assets.zombies_img[z["type"] * 2 + z["frame"]]

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


    for g in player.gun:
        screen.blit(assets.gun_anim[g["type"]][g["frame"]],(g["x"], g["y"]))
    for exp in assets.explosions:
        screen.blit(assets.explosion[exp["frame"]], (exp["x"], exp["y"]))

    # despawn zombies when bullet collides with them
    if player.bullet and zombies_data.zombies:
        for b in player.bullet[:]:
            for z in zombies_data.zombies[:]:
                if b["weapon"] == 3:
                    frame = assets.bulletimages_plasma[b["frame"]]

                    width = frame["middle"].get_width()

                    height = (
                        frame["top"].get_height()
                        + frame["middle"].get_height()
                        + frame["bottom"].get_height()
                    )

                elif b["weapon"] == 5:
                    width = assets.flame[b["frame"]].get_width()
                    height = assets.flame[b["frame"]].get_height()

                else:
                    width = assets.bulletimages[b["frame"]].get_width()
                    height = assets.bulletimages[b["frame"]].get_height()


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
                            z["slow_time"] = utils.slow_time
                        if b["weapon"] == 5:
                            if b["ttl"] > 0:
                                z["burn_time"] = utils.burnt_time
                                b["ttl"] -= 1
                            else:
                                player.bullet.remove(b)
                                continue
                        
                        if b["weapon"] == 2 or b["weapon"] == 7:
                            explosion_x = z["x"]
                            explosion_y = z["y"]
                            assets.explosions.append({
                                "x": explosion_x,
                                "y": explosion_y,
                                "frame": 0,
                                "anim_time": 0
                            })
                            for z2 in zombies_data.zombies[:]:
                                dx = z2["x"] - explosion_x
                                dy = z2["y"] - explosion_y
                                distance = (dx * dx + dy * dy) ** 0.5
                                if distance <= utils.radius_explosion:
                                    z2["hp"] -= b["damage"]
                                    if z2["hp"] <= 0:
                                        player.check_bonus()
                                        if z2["boss"]:
                                            player.score += 25 * player.bonus[0]
                                        else:
                                            player.score += 1 * player.bonus[0]
                                        if z2 in zombies_data.zombies:
                                            zombies_data.zombies.remove(z2)
                            if b in player.bullet:
                                player.bullet.remove(b)
                            continue

                        if z["hp"] <= 0:
                            player.check_bonus()
                            if z["boss"]:
                                player.score += 25 * player.bonus[0]
                            else:
                                player.score += 1 * player.bonus[0]
                            zombies_data.zombies.remove(z)
                            continue 
                        if b["weapon"] != 8 and b["weapon"] != 5:
                            player.bullet.remove(b)

                    except ValueError:
                        pass
    # if gun collides with player, the player get the gun and it despawn
    if player.gun:
        for g in player.gun[:]:
            player.gun_rect = pygame.Rect(g["x"], g["y"], g["width"], g["height"])
            if player.gun_rect.colliderect(pygame.Rect(utils.xsprite, HEIGHT - sprite.get_height(), sprite.get_width(), sprite.get_height())):
                player.gun.remove(g)
                for b in player.bullet[:]:
                    if b in player.bullet:
                        player.bullet.remove(b)
                match g["type"]:
                    case 0:
                        player.current_damage = 22
                        player.delay_bullet = 0.16   # M16
                        assets.bulletimages = assets.bulletimages_small
                        player.current_weapon = 0
                    case 1:
                        player.current_damage = 14
                        player.delay_bullet = 0.07    # M249
                        assets.bulletimages = assets.bulletimages_small
                        player.current_weapon = 1
                    case 2:
                        player.current_damage = 95
                        player.delay_bullet = 1.4     # RPG
                        assets.bulletimages = assets.bulletimages_large
                        player.current_weapon = 2
                        utils.radius_explosion = 120
                    case 3:
                        player.current_damage = 35
                        player.delay_bullet = 0.32    # Plasma
                        player.current_weapon = 3
                    case 4:
                        player.current_damage = 20
                        player.delay_bullet = 0.11     # AK-47
                        assets.bulletimages = assets.bulletimages_small
                        player.current_weapon = 4
                    case 5:
                        player.current_damage = 2
                        player.delay_bullet = 0.05     # Flamethrower
                        assets.bulletimages = assets.bulletimages_large
                        player.current_weapon = 5
                        utils.burning_bullets = True
                        utils.burn_damage = 10
                        utils.burnt_time = 3
                        utils.piercing_bullets = True
                    case 6:
                        player.current_damage = 16
                        player.delay_bullet = 0.1     # Freeze gun
                        assets.bulletimages = assets.bulletimages_medium
                        player.current_weapon = 6
                        utils.ice_bullets = True
                        utils.slow_factor = 0.5
                        utils.slow_time = 2
                    case 7:
                        player.current_damage = 65
                        player.delay_bullet = 0.65    # Grenade launcher
                        assets.bulletimages = assets.bulletimages_large
                        player.current_weapon = 7
                        utils.radius_explosion = 90
                    case 8:
                        player.current_damage = 300
                        player.delay_bullet = 1.2     # Sniper
                        assets.bulletimages = assets.bulletimages_medium
                        player.current_weapon = 8
                        utils.piercing_bullets = True
                print(f"[DEBUG] Le joueur a ramassé une arme (type = {g['type']})")

    for fl in assets.flames:
        screen.blit(
            assets.flame[fl["frame"]],
            (fl["x"], fl["y"])
        )

    # display score (zombie = 1 pt)
    if player.score:
        utils.score_text = utils.font.render(f"Score: {player.score:.1f}           Bonus : x{player.bonus[0]}", True, "white") if player.bonus[0] >1 else utils.font.render(f"Score: {player.score:.1f}", True, "white")
    screen.blit(utils.score_text, (10, 10))

    # flip() the display to put your work on screen
    pygame.display.flip()

    if player.img_player < 20:
        player.img_player += 50 * dt
    else:    
        player.img_player = 1

pygame.quit()

save.u()