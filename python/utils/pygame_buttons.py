import pygame as pg
from .utils import map_range


class GUI_Element():

    def create_canvas():
        ''' Returns a pygame canvas object that represents this element in its current state '''


class Slider(GUI_Element):

    MARGIN_TOP = 8
    MARGIN_SIDE = 15

    def __init__(self, entity, method, rng=(0, 1), font=None, pos=(0, 0), size=(180, 50)):
        # color definitions, these can be changed afterwars
        self.color_bg            = ( 40,  40,  40)
        self.color_border        = (100, 100, 100)
        self.color_text          = (160, 160, 160)
        self.color_slider        = (190, 190, 190)
        self.color_button        = (  0, 220, 120)
        self.color_button_border = (  0,   0,   0)

        self.entity = entity
        self.method = method

        self.value = float(entity[method])
        self.rng = rng

        self.background = pg.surface.Surface(size)
        self.rect = self.background.get_rect()

        self.clicked = False

        # draw the static background
        pg.draw.rect(self.background, self.color_bg, self.rect, 0) # darkgray background
        pg.draw.rect(self.background, self.color_border, self.rect, 1) # lighter gray border

        self.font = font
        # label
        label_surface = font.render(self.entity.name + ":", 1, self.color_text)
        # label_left = self.label_surface.get_rect().width / 2 - self.rect.width / 2
        self.label_rect = label_surface.get_rect(left=self.MARGIN_SIDE, top=self.MARGIN_TOP)
        self.background.blit(label_surface, self.label_rect)

        # slider
        self.slider_height = 3
        self.slider_rect = pg.Rect(self.MARGIN_SIDE, self.rect.height - self.MARGIN_SIDE, 
                                   self.rect.width - self.MARGIN_SIDE*2, self.slider_height)
        pg.draw.rect(self.background, self.color_slider, self.slider_rect, 0)

        # button
        # dont know why i need this offset at the moment, but without it the button is too high
        self.button_size = 15
        self.button_rect = pg.Rect(self.slider_rect.center[0] - self.button_size / 2,
                                   self.slider_rect.center[1] - self.button_size / 2 + 2, 
                                   self.button_size, self.button_size)


    def create_canvas(self):
        canvas = self.background.copy()

        # display value
        value_surface = self.font.render("%.2f" % self.value, 1, self.color_text)
        value_rect = value_surface.get_rect(left=self.label_rect.left + self.label_rect.width + 5, top=self.MARGIN_TOP)
        canvas.blit(value_surface, value_rect)

        # draw button
        pg.draw.circle(canvas, self.color_button, self.button_rect.center, int(self.button_size / 2), 0)
        pg.draw.circle(canvas, self.color_button_border, self.button_rect.center, int(self.button_size / 2+1), 1)

        return canvas

    def button_clicked(self, pos):
        relative_pos = (pos[0] - self.rect.left, pos[1] - self.rect.top)
        return self.button_rect.collidepoint(relative_pos)

    def move_button(self, pos):
        # set the new position according to the mouse position
        relative_pos = (pos[0] - self.rect.left, pos[1] - self.rect.top)
        self.button_rect.left = relative_pos[0] - self.button_size / 2

        # keep the button in the boundaries of the slider
        if self.button_rect.center[0] < self.slider_rect.left:
            self.button_rect.left = self.slider_rect.left - int(self.button_size / 2)
        elif self.button_rect.center[0] > self.slider_rect.left + self.slider_rect.width:
            self.button_rect.left = self.slider_rect.left + self.slider_rect.width - int(self.button_size / 2)

        # set the value by mapping it from the width of the slider to the range provided
        self.value = map_range(self.button_rect.center[0], (self.slider_rect.left, self.slider_rect.left + self.slider_rect.width), self.rng)
        # update the object so that the change is immediatly visible
        self.entity[self.method] = self.value

class Button(GUI_Element):

    COLOR_BG   = ( 40,  40,  40)
    COLOR_BG_H = ( 80,  80,  80)
    COLOR_TEXT = (160, 160, 160)

    def __init__(self, action, text, font, pos=(0, 0), size=(80, 30), bg=None, fg=None):
        if not bg: bg = self.COLOR_BG
        if not fg: fg = self.COLOR_TEXT
        self.color = bg # the static (normal) color
        self.bg = bg # actual background color, can change on mouse over
        self.fg = fg # text color
        self.size = size

        self.text = text
        self.text_surf = font.render(self.text, 1, self.fg)
        self.text_rect = self.text_surf.get_rect(center=[s//2 for s in self.size])

        self.surface = pg.surface.Surface(size)
        self.rect = self.surface.get_rect(center=pos)

        self.call_back_ = action

    def mouseover(self):
        self.bg = self.color
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.bg = self.COLOR_BG_H # mouseover color

    def create_canvas(self):
        self.mouseover()

        self.surface.fill(self.bg)
        self.surface.blit(self.text_surf, self.text_rect)
        return self.surface

    def call_back(self):
        self.call_back_()