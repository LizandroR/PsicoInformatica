import pygame
import sys
from math import sqrt

# Initialize Pygame
pygame.init()
infoObject = pygame.display.Info()
width, height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

# Color definitions
black = (0, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)  # Yellow color for the dots

white = (255, 255, 255)
central_cross_size = 20
central_cross_thickness = 5

# Convert real coordinates to pygame screen coordinates
window_center = (width // 2, height // 2)
window_scale = min(width, height) // 2



def coord(real):
    return int(round(real[0] * window_scale + window_center[0])), int(round(real[1] * window_scale + window_center[1]))

# Define the circles where the yellow dots will be placed
circle_scale = 0.3
circle_radius = 6
circles = [(0, 1), (sqrt(3) / 2, -0.5), (-sqrt(3) / 2, -0.5)]

# Function to draw a blue cross on a surface
cross_size = 40
cross_thickness = 8
def draw_cross(surface, x, y, size, thickness):
    pygame.draw.line(surface, blue, (x - size, y), (x + size, y), thickness)
    pygame.draw.line(surface, blue, (x, y - size), (x, y + size), thickness)

# Calculate the spacing based on the screen size
cross_spacing = min(width, height) // 8

# Create a surface for crosses that will fit the 7x7 matrix
crosses_surface = pygame.Surface((cross_spacing * 7, cross_spacing * 7), pygame.SRCALPHA)
# Center the 7x7 matrix of crosses
matrix_offset = (window_center[0] - crosses_surface.get_width() // 2, window_center[1] - crosses_surface.get_height() // 2)

# Draw the 7x7 matrix of crosses on the surface
for i in range(7):
    for j in range(7):
        x = i * cross_spacing + cross_spacing // 2
        y = j * cross_spacing + cross_spacing // 2
        draw_cross(crosses_surface, x, y, cross_size, cross_thickness)

# Angle for rotation and timing
angle = 0
rotation_speed = 5  # Rotation speed (degrees per frame)
start_time = pygame.time.get_ticks()
rotation_period = 30000  # 30 seconds rotation period
show_static_after = start_time + rotation_period  # Timestamp to switch to static crosses

# Main loop
while running:
    screen.fill(black)

    current_time = pygame.time.get_ticks()

    if current_time < show_static_after:
        # Rotate the surface with crosses
        rotated_surface = pygame.transform.rotozoom(crosses_surface, angle, 1)
        rotated_rect = rotated_surface.get_rect(center=window_center)
        screen.blit(rotated_surface, rotated_rect.topleft)
        # Increment the angle for the next frame
        angle = (angle + rotation_speed) % 360
    else:
        # Show static crosses
        screen.blit(crosses_surface, matrix_offset)

    # After the rotation period, draw the yellow dots
    if current_time >= show_static_after:
        for c0 in circles:
            c = (circle_scale * c0[0], circle_scale * c0[1])
            pygame.draw.circle(screen, yellow, coord(c), circle_radius, circle_radius)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
    pygame.draw.line(screen, white, (window_center[0] - central_cross_size, window_center[1]), (window_center[0] + central_cross_size, window_center[1]), central_cross_thickness)
    pygame.draw.line(screen, white, (window_center[0], window_center[1] - central_cross_size), (window_center[0], window_center[1] + central_cross_size), central_cross_thickness)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
