import os
import pygame

skin1 = pygame.transform.scale_by(pygame.image.load(os.path.join('player', 'img1.png')), (0.125))
skin2 = pygame.transform.scale_by(pygame.image.load(os.path.join('player', 'img2.png')), (0.125))

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