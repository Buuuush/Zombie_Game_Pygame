import pygame
import time
import random

#//* ===== Screen variables =====
WIDTH = 400
HEIGHT = 600

burn_damage = 10
FLAMETHROWER_TTL = 3 # time to live for fire bullets
radius_explosion = 75
slow_time = 2
burning_bullets = False
piercing_bullets = False
ice_bullets = False
slow_factor = 1
xsprite = WIDTH / 2

burnt_time = 3
spawn_delay = 0

# //* ===== Game variables =====
dt = 0 # delta time (fps)
clock = pygame.time.Clock()
fps = 60
font = pygame.font.Font(None, 36)
score_text = font.render("Score: 0", True, "white")
pause = False
running = True