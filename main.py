"""The number of zombies will increase over time,
and the player can move left and right to shoot them.
The player has a score that increases by 1 for each zombie killed.
The game ends when a zombie reaches the bottom of the screen."""


import pygame
import time
import os
import random

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
f = 60
temps_animation = 0
time_from_last_bullet = time.time()
last_spawn = time.time()
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
    global last_spawn
    global wave_size
    global wav_tmp
    y = 0
    for i in range(wave_size):
        r_type = random.randint(0, 5)
        x = random.randint(0,WIDTH - zombies_img[r_type * 2].get_width() - WIDTH // 5)

        zombies.append({
            "frame": 0,
            "x": x,
            "y": 0,
            "anim_time": 0,
            "type": r_type,
            "width": zombies_img[r_type * 2].get_width(),
            "height": zombies_img[r_type * 2].get_height(),
        })
    y += 1
    wav_tmp += 0.125
    print(f"[DEBUG] Création de {wave_size} zombies (wave_size = {wave_size})")
    if wave_size < 15:
        if wav_tmp == 1:
            print(f"[DEBUG] Augmentation de la taille de la vague (wave_size = {wave_size})")
            wave_size += 1
            wav_tmp = 0
zombie_create()


skin1 = pygame.transform.scale_by(pygame.image.load(os.path.join('player', 'img1.png')), (0.125))
skin2 = pygame.transform.scale_by(pygame.image.load(os.path.join('player', 'img2.png')), (0.125))
# multiple bullets
bullet = [] 
bulletimages = [
    pygame.transform.scale_by(pygame.image.load(os.path.join('bullet', 'bullet1.png')), (0.125)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('bullet', 'bullet2.png')), (0.125)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('bullet', 'bullet3.png')), (0.125)),
    pygame.transform.scale_by(pygame.image.load(os.path.join('bullet', 'bullet4.png')), (0.125))
]



print("[DEBUG] Entrée dans la boucle de jeu principale")
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("[DEBUG] Événement de fermeture détecté (pygame.QUIT)")
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    
    # Add a wall at x = WIDTH - WIDTH // 5 from up to (bottom - height player)
    pygame.draw.rect(screen, "black", (WIDTH - WIDTH // 5 - 10, 0, 5, HEIGHT - skin1.get_height()))

    if img_player < 10:
        sprite = skin1
    elif 20 > img_player > 10:
        sprite = skin2

    # spawn zombies at the top of the screen and they have the same time btw switching images
    e = score
    if time.time() - last_spawn > 0.3:
        last_spawn = time.time()
        zombie_create()

    if zombies:
        for z in zombies[:]:
            z["y"] += 50 * dt

            if z["y"] > HEIGHT:
                running = False

            z["anim_time"] += dt
            if z["anim_time"] >= 0.1:
                z["frame"] = 1 - z["frame"]
                z["anim_time"] = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        if xsprite <= 0:
            pass
        else:
            xsprite -= 300 * dt
    if keys[pygame.K_l]:
        if f == 60:
            f = 10
        else:
            f = 60
        print(f"[DEBUG] Changement de la cible FPS (f = {f})")
    if keys[pygame.K_d]:
        if xsprite >= WIDTH - sprite.get_width():
            pass
        else:
            xsprite += 300 * dt
    if keys[pygame.K_SPACE]:
        if time.time() - time_from_last_bullet > delay_bullet:
            time_from_last_bullet = time.time()
            bullet.append({
                "frame": 0,
                "x": xsprite,
                "y": HEIGHT - sprite.get_height(),
                "anim_time": 0,
            })
    if bullet:
        for b in bullet[:]:
            b["y"] -= 500 * dt
            b["anim_time"] += dt
            if b["anim_time"] >= 0.1:
                b["frame"] += 1
                b["anim_time"] = 0
            if b["frame"] >= len(bulletimages):
                b["frame"] = 0
            if b["y"] < 0:
                bullet.remove(b)

    screen.blit(sprite, (xsprite, HEIGHT - sprite.get_height()))
    if bullet:
        for b in bullet:
            screen.blit(bulletimages[b["frame"]], (b["x"], b["y"]))
    if zombies:
        for z in zombies:
            screen.blit(zombies_img[z["type"]*2 + z["frame"]], (z["x"], z["y"]))

    # despawn zombies when bullet collides with them
    if bullet and zombies:
        for b in bullet[:]:
            for z in zombies[:]:
                bullet_rect = pygame.Rect(b["x"], b["y"], bulletimages[b["frame"]].get_width(), bulletimages[b["frame"]].get_height())
                zombie_rect = pygame.Rect(z["x"], z["y"], zombies_img[z["type"]*2 + z["frame"]].get_width(), zombies_img[z["type"]*2 + z["frame"]].get_height())
                if bullet_rect.colliderect(zombie_rect):
                    try:
                        zombies.remove(z)
                        bullet.remove(b)
                        score += 1
                    except ValueError:
                        pass


    # display score (zombie = 1 pt)

    if e != score:
        score_text = font.render(f"Score: {score}", True, "white")
    screen.blit(score_text, (10, 10))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt: float = clock.tick(f) / 1000
    if img_player < 20:
        img_player += 50 * dt
    else:
        img_player = 1

print("[DEBUG] Arrêt de Pygame et fermeture du programme")
pygame.quit()