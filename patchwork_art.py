import pygame
import random
import asyncio

pygame.init()

rows, cols = 20, 10
square_size = 30

width = cols * square_size
height = rows * square_size

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Patchwork Art')


def get_random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


grid_colors = [[get_random_color() for _ in range(cols)] for _ in range(rows)]


async def main_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for row in range(rows):
            for col in range(cols):
                color = grid_colors[row][col]
                rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
                pygame.draw.rect(screen, color, rect)

        pygame.display.flip()

        await asyncio.sleep(0)

await main_loop()