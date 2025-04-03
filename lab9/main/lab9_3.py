import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    radius = 15
    mode = 'blue'
    tool = 'line'
    points = []
    drawing = False
    
    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                elif event.key == pygame.K_s:
                    tool = 'square'
                elif event.key == pygame.K_t:
                    tool = 'right_triangle'
                elif event.key == pygame.K_e:
                    tool = 'equilateral_triangle'
                elif event.key == pygame.K_h:
                    tool = 'rhombus'
                elif event.key == pygame.K_l:
                    tool = 'line'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    points = [event.pos]
                elif event.button == 3:
                    radius = max(1, radius - 1)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    points.append(event.pos)
            
            if event.type == pygame.MOUSEMOTION and drawing:
                if len(points) == 1:
                    points.append(event.pos)
                else:
                    points[1] = event.pos
                
        screen.fill((255, 255, 255))
        
        if len(points) == 2:
            if tool == 'line':
                pygame.draw.line(screen, pygame.Color(mode), points[0], points[1], radius)
            elif tool == 'square':
                draw_square(screen, points[0], points[1], mode)
            elif tool == 'right_triangle':
                draw_right_triangle(screen, points[0], points[1], mode)
            elif tool == 'equilateral_triangle':
                draw_equilateral_triangle(screen, points[0], points[1], mode)
            elif tool == 'rhombus':
                draw_rhombus(screen, points[0], points[1], mode)
        
        pygame.display.flip()
        clock.tick(60)

def draw_square(screen, start, end, color):
    side = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
    rect = pygame.Rect(start[0], start[1], side, side)
    pygame.draw.rect(screen, pygame.Color(color), rect, 2)

def draw_right_triangle(screen, start, end, color):
    points = [start, (end[0], start[1]), end]
    pygame.draw.polygon(screen, pygame.Color(color), points, 2)

def draw_equilateral_triangle(screen, start, end, color):
    side = abs(end[0] - start[0])
    height = math.sqrt(3) / 2 * side
    points = [start, (start[0] + side, start[1]), (start[0] + side // 2, start[1] - height)]
    pygame.draw.polygon(screen, pygame.Color(color), points, 2)

def draw_rhombus(screen, start, end, color):
    width = abs(end[0] - start[0])
    height = abs(end[1] - start[1])
    points = [
        (start[0] + width // 2, start[1]),
        (start[0] + width, start[1] + height // 2),
        (start[0] + width // 2, start[1] + height),
        (start[0], start[1] + height // 2)
    ]
    pygame.draw.polygon(screen, pygame.Color(color), points, 2)

main()