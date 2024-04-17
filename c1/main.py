import pygame
import sys
from cube import Cube
import numpy as np


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = np.array([SCREEN_WIDTH, SCREEN_HEIGHT])
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FOCAL_LIMITS = 20.0, 500.0
FOCAL_STEP = 0.3
TRANSLATION_STEP = 0.05
ROTATION_STEP = np.radians(0.1)

pygame.init()
pygame.display.set_caption("Camera")
screen = pygame.display.set_mode(tuple(SCREEN_SIZE))

cubes = [
    Cube.read("cubes/1"),
    Cube.read("cubes/2"),
    Cube.read("cubes/3"),
    Cube.read("cubes/4"),
]

focal = 200
node_color = (255, 255, 255)
node_size = 3
edge_color = node_color
EDGE_WIDTH = 2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        for cube in cubes:
            cube.translate(0, TRANSLATION_STEP, 0)
    if keys[pygame.K_DOWN]:
        for cube in cubes:
            cube.translate(0, -TRANSLATION_STEP, 0)
    if keys[pygame.K_LEFT]:
        for cube in cubes:
            cube.translate(TRANSLATION_STEP, 0, 0)
    if keys[pygame.K_RIGHT]:
        for cube in cubes:
            cube.translate(-TRANSLATION_STEP, 0, 0)
    if keys[pygame.K_SPACE]:
        for cube in cubes:
            cube.translate(0, 0, TRANSLATION_STEP)
    if keys[pygame.K_LSHIFT]:
        for cube in cubes:
            cube.translate(0, 0, -TRANSLATION_STEP)

    if keys[pygame.K_q]:
        for cube in cubes:
            cube.rotate(ROTATION_STEP, "x")
    if keys[pygame.K_w]:
        for cube in cubes:
            cube.rotate(-ROTATION_STEP, "x")
    if keys[pygame.K_a]:
        for cube in cubes:
            cube.rotate(ROTATION_STEP, "y")
    if keys[pygame.K_s]:
        for cube in cubes:
            cube.rotate(-ROTATION_STEP, "y")
    if keys[pygame.K_z]:
        for cube in cubes:
            cube.rotate(ROTATION_STEP, "z")
    if keys[pygame.K_x]:
        for cube in cubes:
            cube.rotate(-ROTATION_STEP, "z")

    if keys[pygame.K_PAGEUP]:
        focal += FOCAL_STEP
    if keys[pygame.K_PAGEDOWN]:
        focal -= FOCAL_STEP

    screen.fill(BLACK)

    for cube in cubes:
        edges = cube.get_2d_edges(focal)

        for edge in edges:
            start = edge[:2] + SCREEN_SIZE / 2
            end = edge[2:] + SCREEN_SIZE / 2

            pygame.draw.line(screen, WHITE, start, end, EDGE_WIDTH)

    pygame.display.flip()

pygame.quit()
sys.exit()
