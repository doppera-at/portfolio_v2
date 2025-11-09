import sys, math
import pygame as pg
import utils.colors as c
from utils.gui_elements import *
from utils.utils import calculate_points_on_circle
from ecs.Entity import Entity


pg.init()
screen = pg.display.set_mode((800, 600))
screen.set_colorkey(c.TRANSPARENT)
pg.display.set_caption("Times table cardoid")
font = pg.font.SysFont("Verdana", 14)
clock = pg.time.Clock()

main_canvas = pg.Surface((600, 600))
gui_canvas = pg.Surface((200, 600))
gui_canvas.set_colorkey(c.TRANSPARENT)
gui_pos = (600, 0)
gui_elements = []


circle = Entity("Circle")
circle.pos = (int(main_canvas.get_rect().width / 2), int(main_canvas.get_rect().height / 2))
circle.radius = main_canvas.get_rect().width / 2 - 50

app_config = Entity("TimesTable")
app_config.num_points = 100
app_config.multiplier = 2
app_config.animate = False
app_config.reset = False

slider_radius = Slider(circle, "radius", (50, 500), font)
gui_elements.append(slider_radius)
slider_points = Slider(app_config, "num_points", (50, 500), font)
gui_elements.append(slider_points)
slider_multiplier = Slider(app_config, "multiplier", (2, 200), font)
gui_elements.append(slider_multiplier)
button_multiplier = ButtonIncrement(app_config, "multiplier", font, step_size=1, rng=(2, 200))
gui_elements.append(button_multiplier)
button_animation = ButtonToggle(app_config, "animate", font)
gui_elements.append(button_animation)
button_reset = ButtonToggle(app_config, "reset", font)
gui_elements.append(button_reset)

def main():
    while True:
        handle_events()

        screen.fill(c.BLACK)
        main_canvas.fill(c.BLACK)
        gui_canvas.fill(c.TRANSPARENT)

        if app_config.reset:
            app_config.animate = False
            app_config.multiplier = 2
            circle.radius = main_canvas.get_rect().width / 2 - 50
            app_config.reset = False
        if app_config.animate:
            app_config.multiplier += 0.1
            if app_config.multiplier > 200: app_config.multiplier = 1

        #pg.draw.circle(main_canvas, c.YELLOW, circle.pos, int(circle.radius), 1)
        app_config.points = calculate_points_on_circle(circle.pos, circle.radius, app_config.num_points)
        app_config.lines = generate_lines(app_config.points, app_config.multiplier)
        for point in app_config.points:
            pg.draw.circle(main_canvas, c.YELLOW_GREEN, (int(point[0]), int(point[1])), 2, 0)
        for (p1, p2) in app_config.lines:
            pg.draw.line(main_canvas, c.YELLOW_GREEN, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), 1)

        screen.blit(main_canvas, main_canvas.get_rect())


        create_gui(gui_canvas)
        gui_rect = gui_canvas.get_rect(left=gui_pos[0], top=gui_pos[1])
        screen.blit(gui_canvas, gui_rect)


        pg.display.flip()
        clock.tick(60)
        pg.display.set_caption("{} (FPS: {})")

def generate_lines(points=[], num=2):
    result = []
    for i in range(0, len(points)):
        p1 = points[i]
        p2 = points[(i*int(num)) % len(points)]
        result.append((p1, p2))
    return result

def handle_events():
    for event in pg.event.get():
        mouse_pos = pg.mouse.get_pos()
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            for element in gui_elements:
                if isinstance(element, Slider) and element.is_clicked(mouse_pos):
                    element.clicked = True
                elif isinstance(element, Button) or isinstance(element, ButtonIncrement) or isinstance(element, ButtonToggle):
                    if element.is_clicked(mouse_pos):
                        element.action(mouse_pos)
        elif event.type == pg.MOUSEMOTION:
            for element in gui_elements:
                if isinstance(element, Slider) and element.clicked:
                    element.action(mouse_pos)
        elif event.type == pg.MOUSEBUTTONUP:
            for element in gui_elements:
                if isinstance(element, Slider):
                    element.clicked = False
    for e in gui_elements:
        e.update()

def create_gui(canvas):
    pg.draw.rect(canvas, c.GRAY, canvas.get_rect(), 1)
    y_offset = GUI_Element.MARGIN
    for element in gui_elements:
        e_canvas = element.create_canvas()
        e_rect = e_canvas.get_rect(left=GUI_Element.MARGIN, top=y_offset)
        element.pos = (e_rect.left + gui_pos[0], e_rect.top + gui_pos[1])
        y_offset += e_rect.height + GUI_Element.MARGIN
        canvas.blit(e_canvas, e_rect)


if __name__ == '__main__':
    main()