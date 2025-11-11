import sys, math
import pygame as pg
import colors as c
from pygame_buttons import *

MARGIN = 80

# Initialization
pg.init()
screen = pg.display.set_mode((1000, 600))
screen.set_colorkey(c.TRANSPARENT)
font = pg.font.SysFont("Verdana", 14)
clock = pg.time.Clock()
changed = False

gui_canvas = pg.Surface((200, 600))
gui_canvas.set_colorkey(c.TRANSPARENT)
gui_pos = (800, 0)
gui_elements = []

main_canvas = pg.Surface((800, 600))


#config = Entity("Basic ECS")
#config.entites = []

def main():
    while True:
        handle_events()


        # CALCULATIONS GO HERE



        screen.fill(c.BLACK)
        main_canvas.fill(c.BLACK)
        gui_canvas.fill(c.TRANSPARENT)


        # DRAWING GOES HERE


        # drawing the main canvas
        screen.blit(main_canvas, main_canvas.get_rect())
        # drawing the GUI
        create_gui()
        gui_rect = gui_canvas.get_rect(left=gui_pos[0], top=gui_pos[1])
        screen.blit(gui_canvas, gui_rect)

        # display the created screen
        pg.display.flip()
        clock.tick(60)
        pg.display.set_caption("{} (FPS: {})".format(config.name, round(clock.get_fps())))

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
    gui_canvas.fill(c.TRANSPARENT)
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