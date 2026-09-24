import math
import time
import py_files.utils as utils

#//* ===== Zombie variables =====
wav_tmp = 0
temps_animation = 0
last_spawn = time.time()
zombies_to_spawn = 0
last_zombie_spawn = time.time()
wave_size = 1
difficulty_level_wave = 0
nb_zombies = 0
zombies = []

def zombie_create():
    global zombies
    global wave_size
    global wav_tmp
    global zombies_to_spawn
    global last_zombie_spawn
    global difficulty_level_wave
    global nb_zombies
    # new wave
    utils.spawn_delay = max(0.02, 0.2 / (wave_size ** 0.7))
    if len(zombies) == 0 and zombies_to_spawn == 0:
        zombies_to_spawn = wave_size
        print(f"[DEBUG] Nouvelle vague : {wave_size} zombies")
        wav_tmp += 1
        if wave_size < 50 and wav_tmp >= 4:
            wav_tmp = 0
            difficulty_level_wave += 1
            wave_size = int(round(math.exp(difficulty_level_wave), 0)) 
            print(f"[DEBUG] Taille prochaine vague : {wave_size}")