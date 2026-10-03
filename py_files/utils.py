import pygame

#//* ===== Screen variables =====
WIDTH = 400
HEIGHT = 600

burn_damage = 10
FLAMETHROWER_TTL = 5 # time to live for fire bullets (nb of ennemis before end bullet)
radius_explosion = 75
slow_time = 2
burning_bullets = False
piercing_bullets = False
ice_bullets = False
slow_factor = 1
xsprite = WIDTH / 2
ammo = 0
reload_time = 0
current_reload = False
reload_start_time = 0

burnt_time = 3
spawn_delay = 0

# //* ===== Game variables =====
dt = 0 # delta time (fps)
clock = pygame.time.Clock()
fps = 0
font = pygame.font.Font(None, 36)
score_text = font.render("Score: 0", True, "white")
ammo_text = font.render("Ammo: 0", True, "white")
weapon_text = font.render("Basic gun", True, "white")
pause = False
running = True

def get_color_hp(hp, max):
    if hp > (max/3)*2:
        return "green"
    elif hp > max/3:
        return "orange"
    else:
        return "red"

def get_color_reload(reload_progress):
    if reload_progress >2/3:
        return "green"
    elif reload_progress > 1/3:
        return "orange"
    else:
        return "red"