from ursina import *
import time
import random

def start_game():
    # Hide title screen and show game elements
    title_text.enabled = False
    start_game_button.enabled = False
    player.enabled = True
    score_board.enabled = True
    road.enabled = True
    median_r.enabled = True
    median_l.enabled = True
    for enemy in enemies:
        enemy.enabled = True
    application.resume()

def restart_game():
    global speed
    # Reset player and game state
    player.position = (0, 3, -2000)
    player.rotation = Vec3(0, 0, 0)
    score_board.text = '0'
    game_over_text.enabled = False
    restart_button.enabled = False
    quit_button.enabled = False
    speed = 200
    # Re-enable all game elements
    player.enabled = True
    road.enabled = True
    median_r.enabled = True
    median_l.enabled = True
    for enemy in enemies:
        enemy.enabled = True
    application.resume()

def quit_game():
    application.quit()

def game_over():
    application.pause()
    game_over_text.enabled = True
    restart_button.enabled = True
    quit_button.enabled = True

# Initialize Ursina game
game = Ursina()

# Title Screen
title_text = Text(text='The Super Ball', scale=5, origin=(0, 0), color=color.white)
start_game_button = Button(text='Start Game', color=color.azure, scale=(0.2, 0.1), position=(0, -0.2))
start_game_button.on_click = start_game

# Game Elements
player = Entity(model='sphere', color=color.red, position=(0, 3, -1000), scale=(5, 5, 5), collider='box', enabled=False)
camera.z = -15
camera.add_script(SmoothFollow(target=player, offset=(0, 5, -30)))
road = Entity(model='plane', scale=(50, 10, 1000000), color=color.black, enabled=False)
rows = [-15, -10, -5, 0, 5, 10, 15]
median_r = Entity(model='cube', collider='box', position=(25, 2, 0), scale=(5, 10, 1000000), color=color.white, enabled=False)
median_l = Entity(model='cube', collider='box', position=(-25, 2, 0), scale=(5, 10, 1000000), color=color.white, enabled=False)
score_board = Text(text='0', scale=5, x=-0.85, y=0.45, enabled=False)
speed = 200

game_over_text = Text(text='Game Over', scale=5, origin=(0, 0), color=color.red, enabled=False)
restart_button = Button(text='Restart', color=color.azure, scale=(0.2, 0.1), position=(0, -0.1), enabled=False)
quit_button = Button(text='Quit', color=color.azure, scale=(0.2, 0.1), position=(0, -0.3), enabled=False)

restart_button.on_click = restart_game
quit_button.on_click = quit_game

# Create enemies
enemies = []
for i in range(0, 100000, 100):
    enemy = Entity(model='cube', collider='box', position=(random.choice(rows), 6, i), color=color.random_color(), scale=(10, 10, 10), enabled=False)
    enemies.append(enemy)

def update():
    global speed
    player.z += time.dt * speed
    player.rotation_x += time.dt * 50
    score_val = player.z + 600
    score = int(score_val)

    if held_keys['d']:
        player.x += time.dt * 25
        player.rotation_z += time.dt * 100
    if held_keys['a']:
        player.x -= time.dt * 25
        player.rotation_z -= time.dt * 100
    if held_keys['w']:
        player.z += time.dt * 1000
        player.rotation_x += time.dt * 600

    if player.intersects().hit or median_r.intersects().hit or median_l.intersects().hit:
        game_over()

    score_board.text = str(score)

window.fullscreen = True
sky = Sky()
game.run()