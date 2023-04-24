import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def R(x, y, radius):
    r = math.sqrt(x ** 2 + y ** 2)
    if int(r) != int(radius):
        return RED
    return GREEN


def cur_radius(x, y):
    return math.sqrt(x ** 2 + y ** 2)


def drawLineBetween(screen, index, start, end, width, color):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(progress * start[0] + aprogress * end[0])
        y = int(progress * start[1] + aprogress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)


def too_close(center_x, center_y, pos_x, pos_y):
    if abs(center_x - pos_x) <= 25 and abs(center_y - pos_y) <= 25:
        return False
    return True


def percent(n, color):
    font = pygame.font.SysFont("Arial", 20, True)
    text = font.render(f'{n}', False, color)
    return text


def compare(radius, current):
    return (current * 100) / radius


def main():
    pygame.init()
    clock = pygame.time.Clock()

    points = []

    WIDTH = 1000
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    ok = False
    c_x, c_y = WIDTH / 2, HEIGHT / 2
    radius = 0
    color = []
    error_message = ""
    percentage = "XX."
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill(BLACK)
                points = []
                ok = True

                x, y = pygame.mouse.get_pos()
                x = abs(x - c_x)
                y = abs(y - c_y)
                radius = math.sqrt(x ** 2 + y ** 2)
                color.append(GREEN)
                error_message = ""
            if ok:
                if event.type == pygame.MOUSEMOTION:
                    position = event.pos
                    points = points + [position]
                    position = position[-256:]

                    color.append(R(position[0], position[1], radius))

                    ok = too_close(c_x, c_y, position[0], position[1])
                    # percentage = (percentage + compare(radius, cur_radius(position[0], position[1]))) // len(points)
                    if ok == False:
                        error_message = "too close"

            if event.type == pygame.MOUSEBUTTONUP:
                ok = False

        pygame.draw.circle(screen, WHITE, (c_x, c_y), 12)
        screen.blit(percent(percentage, WHITE), (c_x - 40, c_y - 10))
        screen.blit(percent(error_message, WHITE), (c_x - 40, c_y + 20))
        i = 0
        while i < len(points) - 1:
            drawLineBetween(screen, i, points[i], points[i + 1], 3, color[i])
            i += 1
        pygame.display.flip()
        clock.tick(60)


main()
