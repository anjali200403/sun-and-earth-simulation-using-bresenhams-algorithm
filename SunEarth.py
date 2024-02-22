import pygame
import sys
import math
from numpy import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sun and Earth")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE=(0, 102, 204)
YELLOW=(255, 255, 102)
GREEN = (0,255,0)
ORANGE = (255,201,34)


def set_pixel(surface, x, y, color):
    surface.set_at((x, y), color)

def draw_bresenhams_circle(surface, cx, cy, radius, color):
    x = 0
    y = radius
    d = 3 - 2 * radius

    while y >= x:
        draw_circle_points(surface, cx, cy, x, y, color)
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6

def draw_circle_points(surface, cx, cy, x, y, color):
    if(color==BLUE):
        n=random.randint(1,8)
        arr=random.randint(1,8,size=n)
        if 1 in arr:
            set_pixel(surface, cx + x, cy + y, GREEN)
        else:
            set_pixel(surface, cx + x, cy + y, BLUE)

        if 2 in arr:
            set_pixel(surface, cx - x, cy + y, GREEN)
        else:
            set_pixel(surface, cx - x, cy + y,BLUE)

        if 3 in arr:
            set_pixel(surface, cx + x, cy - y, GREEN)
        else:
            set_pixel(surface, cx + x, cy - y, BLUE)

        if 4 in arr:
            set_pixel(surface, cx - x, cy - y, GREEN)
        else:
            set_pixel(surface, cx - x, cy - y, BLUE)

        if 5 in arr:
            set_pixel(surface, cx + y, cy + x, GREEN)
        else:
            set_pixel(surface, cx + y, cy + x, BLUE)

        if 6 in arr:
            set_pixel(surface, cx - y, cy + x, GREEN)
        else:
            set_pixel(surface, cx - y, cy + x, BLUE)

        if 7 in arr:
            set_pixel(surface, cx + y, cy - x, GREEN)
        else:
            set_pixel(surface, cx + y, cy - x, BLUE)

        if 8 in arr:
            set_pixel(surface, cx - y, cy - x, GREEN)
        else:
            set_pixel(surface, cx - y, cy - x, BLUE)         
       
    else:
        set_pixel(surface, cx + x, cy + y, color)
        set_pixel(surface, cx - x, cy + y, color)
        set_pixel(surface, cx + x, cy - y, ORANGE)
        set_pixel(surface, cx - x, cy - y, color)
        set_pixel(surface, cx + y, cy + x, ORANGE)
        set_pixel(surface, cx - y, cy + x, color)
        set_pixel(surface, cx + y, cy - x, ORANGE)
        set_pixel(surface, cx - y, cy - x, color)
        
def rotate_x(point, angle, center):
    x, y, z = point
    cx, cy, cz = center
    y -= cy
    z -= cz
    new_y = y * math.cos(angle) - z * math.sin(angle)
    new_z = y * math.sin(angle) + z * math.cos(angle)
    return (x, new_y + cy, new_z + cz)

def rotate_z(point, angle, center):
    x, y, z = point
    cx, cy, cz = center
    x -= cx
    y -= cy
    new_x = x * math.cos(angle) - y * math.sin(angle)
    new_y = x * math.sin(angle) + y * math.cos(angle)
    return (new_x + cx, new_y + cy-300, z)

def rotate_xz(point, angle, center):
    rotated_x = rotate_x(point, angle, center)
    return rotate_z(rotated_x, angle, center)


def main():
    cx, cy = width // 2+100, height  
    radius = 100  
    angle = 0
    a=1
    b=10
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        
        for phi in range(0, 360, 2):
            for theta in range(0, 360, 2):
                x = cx + int(radius * math.sin(math.radians(theta)) * math.cos(math.radians(phi)))
                y = cy + int(radius * math.sin(math.radians(theta)) * math.sin(math.radians(phi)))
                z = int(radius * math.cos(math.radians(theta)))
                rotated_point = rotate_xz((x, y, z), angle, (cx, cy, 0))
                draw_bresenhams_circle(screen, int(rotated_point[0]), int(rotated_point[1]), 2, YELLOW)

                next_phi = (phi + 5) % 360
                next_theta = (theta + 5) % 360
                next_x = cx + int(radius * math.sin(math.radians(next_theta)) * math.cos(math.radians(next_phi)))
                next_y = cy + int(radius * math.sin(math.radians(next_theta)) * math.sin(math.radians(next_phi)))
                next_z = int(radius * math.cos(math.radians(next_theta)))
                rotated_point = rotate_xz((next_x, next_y, next_z), angle, (cx, cy, 0))

        
        second_radius = 50  
        second_center = (cx + 200, cy)  
        
        for phi in range(0, 360, 5):
            for theta in range(0, 360, 5):
                x = second_center[0] + int(second_radius * math.sin(math.radians(theta)) * math.cos(math.radians(phi)))
                y = second_center[1] + int(second_radius * math.sin(math.radians(theta)) * math.sin(math.radians(phi)))
                z = int(second_radius * math.cos(math.radians(theta)))
                x = x+cx+ a * math.cos(math.radians(angle))-500
                y = y+cy+ b * math.sin(math.radians(angle))-500
                rotated_point = rotate_xz((x, y, z), angle, (cx, cy, 0))
                draw_bresenhams_circle(screen, int(rotated_point[0]), int(rotated_point[1]), 2, BLUE)
                
                next_phi = (phi + 5) % 360
                next_theta = (theta + 5) % 360
                next_x = second_center[0] + int(second_radius * math.sin(math.radians(next_theta)) * math.cos(math.radians(next_phi)))
                next_y = second_center[1] + int(second_radius * math.sin(math.radians(next_theta)) * math.sin(math.radians(next_phi)))
                next_z = int(second_radius * math.cos(math.radians(next_theta)))
                rotated_point = rotate_xz((next_x, next_y, next_z), angle, (cx, cy, 0))


        angle += math.radians(1)
        if angle >= 2 * math.pi:
            angle -= 2 * math.pi

        pygame.display.flip()

if __name__ == "__main__":
    main()
