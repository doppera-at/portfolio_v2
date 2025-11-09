import sys, math
import pygame as pg
import utils.colors as c
from utils.gui_elements import *
from utils.utils import *
from ecs.Entity import Entity

MARGIN = 10

# Initialization
pg.init()
screen = pg.display.set_mode((800, 600))
screen.set_colorkey(c.TRANSPARENT)
font = pg.font.SysFont("Verdana", 14)
clock = pg.time.Clock()
changed = False

gui_canvas = pg.Surface((200, 600))
gui_canvas.set_colorkey(c.TRANSPARENT)
gui_pos = (600, 0)
gui_elements = []

main_canvas = pg.Surface((600, 600))
curves_canvas = pg.Surface(main_canvas.get_rect().size)
curves_canvas.set_colorkey(c.TRANSPARENT)
curves_canvas.fill(c.TRANSPARENT)


app_config = Entity("Lissajous Curve Table")
app_config.num_circles = 8
app_config.curve_size = 1
app_config.circle_radius = 27
app_config.circle_width = 1
app_config.point_width = 4
app_config.init_speed = 1
app_config.angle_mod = math.pi / 256
app_config.circle_color = c.ORANGE
app_config.point_color = c.YELLOW
app_config.line_color = c.GRAY_DARK
app_config.curve_color = c.FOREST_GREEN
app_config.circles_top = []
app_config.circles_left = []
app_config.reset = False

button_reset = ButtonToggle(app_config, "reset", font)
gui_elements.append(button_reset)
button_initspeed = ButtonIncrement(app_config, "init_speed", rng=(1, 5), font=font)
gui_elements.append(button_initspeed)

def init_circles():
    app_config.circles_top = []
    app_config.circles_left = []
    offset = MARGIN + app_config.circle_radius * 2
    for i in range(0, app_config.num_circles):
        top = Entity("Circle Top {}".format(i))
        top.radius = app_config.circle_radius
        top.pos = (offset * (i+1) + MARGIN + top.radius, MARGIN + top.radius)
        top.angle = 0
        top.speed = app_config.init_speed+i
        app_config.circles_top.append(top)

        left = Entity("Circle Left {}".format(i))
        left.radius = app_config.circle_radius
        left.pos = (MARGIN + left.radius, offset * (i+1) + MARGIN + left.radius)
        left.angle = 0
        left.speed = app_config.init_speed+i
        app_config.circles_left.append(left)
init_circles()

def main():
    while True:
        handle_events()

        if app_config.reset:
            init_circles()
            curves_canvas.fill(c.TRANSPARENT)
            app_config.reset = False

        # CALCULATIONS GO HERE
        for i in range(0, app_config.num_circles):
            top = app_config.circles_top[i]
            left = app_config.circles_left[i]
            # 1. Calculate position of points
            top_x = top.radius * math.cos(top.angle)
            top_y = top.radius * math.sin(top.angle)
            top.point = (top.pos[0] + top_x, top.pos[1] + top_y)
            left_x = left.radius * math.cos(left.angle)
            left_y = left.radius * math.sin(left.angle)
            left.point = (left.pos[0] + left_x, left.pos[1] + left_y)
            # 2. Calculate new angle based on the speed
            top.angle = top.angle - (app_config.angle_mod * top.speed)
            left.angle = left.angle - (app_config.angle_mod * left.speed)


        screen.fill(c.BLACK)
        main_canvas.fill(c.BLACK)


        # DRAWING GOES HERE
        for i in range(0, app_config.num_circles):
            top = app_config.circles_top[i]
            left = app_config.circles_left[i]

            # 2. Draw the scanlines from the points (moved first to be behind everything)
            pg.draw.line(main_canvas, app_config.line_color, (top.point[0], 0), (top.point[0], main_canvas.get_rect().height), 1)
            pg.draw.line(main_canvas, app_config.line_color, (0, left.point[1]), (main_canvas.get_rect().width, left.point[1]), 1)
            # 1. Draw the circles
            pg.draw.circle(main_canvas, app_config.circle_color, top.pos, top.radius, app_config.circle_width)
            pg.draw.circle(main_canvas, app_config.circle_color, left.pos, left.radius, app_config.circle_width)
            # 1.1 Draw Points on Circle
            pg.draw.circle(main_canvas, app_config.point_color, (int(top.point[0]), int(top.point[1])), app_config.point_width, 0)
            pg.draw.circle(main_canvas, app_config.point_color, (int(left.point[0]), int(left.point[1])), app_config.point_width, 0)
        
        # 4. Dot the crosssection of each circles point
        for top in app_config.circles_top:
            for left in app_config.circles_left:
                pg.draw.line(curves_canvas, app_config.curve_color, (int(top.point[0]), int(left.point[1])), (int(top.point[0]), int(left.point[1])))
                #pg.draw.circle(curves_canvas, app_config.curve_color, (int(top.point[0]), int(left.point[1])), app_config.curve_size)


        # drawing the main canvas
        screen.blit(main_canvas, main_canvas.get_rect())
        # drawing the curves on top of it
        screen.blit(curves_canvas, curves_canvas.get_rect())
        # drawing the GUI
        create_gui()
        gui_rect = gui_canvas.get_rect(left=gui_pos[0], top=gui_pos[1])
        screen.blit(gui_canvas, gui_rect)

        # display the created screen
        pg.display.flip()
        clock.tick(60)
        pg.display.set_caption("{} (FPS: {})".format(app_config.name, round(clock.get_fps())))

def handle_events():
    for event in pg.event.get():
        mouse_pos = pg.mouse.get_pos()
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            for element in gui_elements:
                if element.is_clicked(mouse_pos):
                    if isinstance(element, Slider):
                        element.clicked = True
                    else:
                        element.action(mouse_pos)
                        changed = True
        elif event.type == pg.MOUSEMOTION:
            for element in gui_elements:
                if isinstance(element, Slider) and element.clicked:
                    element.action(mouse_pos)
                    changed = True
        elif event.type == pg.MOUSEBUTTONUP:
            for element in gui_elements:
                if isinstance(element, Slider):
                    element.clicked = False
    for e in gui_elements:
        e.update()

def create_gui():
    gui_canvas.fill(c.GRAY_DARKEST)
    pg.draw.rect(gui_canvas, c.GRAY, gui_canvas.get_rect(), 1)
    y_offset = GUI_Element.MARGIN
    for element in gui_elements:
        e_canvas = element.create_canvas()
        e_rect = e_canvas.get_rect(left=GUI_Element.MARGIN, top=y_offset)
        element.pos = (e_rect.left + gui_pos[0], e_rect.top + gui_pos[1])
        y_offset += e_rect.height + GUI_Element.MARGIN
        gui_canvas.blit(e_canvas, e_rect)


if __name__ == '__main__':
    main()