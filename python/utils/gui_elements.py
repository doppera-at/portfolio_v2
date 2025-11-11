import pygame as pg
from .utils import map_range


class GUI_Element():

    MARGIN = 15

    def create_canvas():
        ''' Returns a pygame canvas object that represents this element in its current state '''
    def is_clicked(mouse_pos):
        ''' Returns true if the element has been clicked '''
    def action(mouse_pos=None):
        ''' Performs the action of that element, depending on element type '''
    def update():
        ''' Fetches the actual values '''
        
class Slider(GUI_Element):

    MARGIN_TOP = 8
    MARGIN_SIDE = 15

    def __init__(self, entity, method, rng=(0, 1), font=None, pos=(0, 0), size=(180, 50)):
        # color definitions, these can be changed afterwars
        self.color_bg            = ( 40,  40,  40)
        self.color_border        = (127, 127, 127)
        self.color_text          = (160, 160, 160)
        self.color_slider        = (190, 190, 190)
        self.color_button        = (  0, 220, 120)
        self.color_button_border = (  0,   0,   0)

        self.pos = pos

        self.entity = entity
        self.method = method

        self.value = float(entity[method])
        self.rng = rng

        self.background = pg.surface.Surface(size)
        self.rect = self.background.get_rect()

        self.clicked = False
        self.float = False

        # draw the static background
        pg.draw.rect(self.background, self.color_bg, self.rect, 0) # darkgray background
        pg.draw.rect(self.background, self.color_border, self.rect, 1) # lighter gray border

        self.font = font
        # label
        label_surface = font.render(self.method.capitalize() + ":", 1, self.color_text)
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
        button_x = map_range(self.value, (self.rng[0], self.rng[1]), (self.slider_rect.left, self.slider_rect.width))
        self.button_rect = pg.Rect(button_x, self.slider_rect.center[1] - self.button_size / 2 + 2, 
                                   self.button_size, self.button_size)


    def create_canvas(self):
        canvas = self.background.copy()

        # display value
        value_surface = self.font.render("%.2f" % self.value, 1, self.color_text)
        if self.float:
            value_surface = self.font.render(self.value, 1, self.color_text)
        value_rect = value_surface.get_rect(left=self.label_rect.left + self.label_rect.width + 5, top=self.MARGIN_TOP)
        canvas.blit(value_surface, value_rect)

        # draw button
        pg.draw.circle(canvas, self.color_button, self.button_rect.center, int(self.button_size / 2), 0)
        pg.draw.circle(canvas, self.color_button_border, self.button_rect.center, int(self.button_size / 2+1), 1)

        return canvas

    def is_clicked(self, mouse_pos):
        self.rect.left = self.pos[0]
        self.rect.top = self.pos[1]
        relative_pos = (mouse_pos[0] - self.rect.left, mouse_pos[1] - self.rect.top)
        return self.button_rect.collidepoint(relative_pos) or self.slider_rect.collidepoint(relative_pos)

    def action(self, mouse_pos):
        # set the new position according to the mouse position
        relative_pos = (mouse_pos[0] - self.rect.left, mouse_pos[1] - self.rect.top)
        
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

    def update(self):
        self.value = self.entity[self.method]
        button_x = map_range(self.value, (self.rng[0], self.rng[1]), (self.slider_rect.left, self.slider_rect.width))
        self.button_rect.left = button_x

class ButtonIncrement(GUI_Element):

    COLOR_BG   =   ( 40,  40,  40)
    COLOR_BG_H =   ( 80,  80,  80)
    COLOR_BORDER = (127, 127, 127)
    COLOR_TEXT =   (160, 160, 160)

    MARGIN_TOP = 8
    MARGIN_SIDE = 15
    MARGIN_BOXES = 3

    BOX_SIZE = 25

    def __init__(self, entity, method, font, rng=(0, 1), step_size=1, pos=(0, 0), size=(180, 65)):
        self.entity = entity
        self.method = method

        self.value = entity[method]
        self.rng = rng
        self.step_size = step_size
        self.float = False

        self.pos = pos
        self.size = size 

        self.background = pg.Surface(size)
        self.rect = self.background.get_rect()

        self.minus_button = pg.Surface((self.BOX_SIZE, self.BOX_SIZE))
        self.minus_button.fill(self.COLOR_BG)
        pg.draw.rect(self.minus_button, self.COLOR_BORDER, self.minus_button.get_rect(), 1)
        minus_sign = font.render("-", 1, self.COLOR_TEXT)
        self.minus_button.blit(minus_sign, minus_sign.get_rect(center=[s//2 for s in self.minus_button.get_size()]))
        self.plus_button = pg.Surface((self.BOX_SIZE, self.BOX_SIZE))
        self.plus_button.fill(self.COLOR_BG)
        pg.draw.rect(self.plus_button, self.COLOR_BORDER, self.plus_button.get_rect(), 1)
        plus_sign = font.render("+", 1, self.COLOR_TEXT)
        self.plus_button.blit(plus_sign, plus_sign.get_rect(center=[s//2 for s in self.plus_button.get_size()]))

        self.font = font

    def create_canvas(self):
        self.background.fill(self.COLOR_BG)
        pg.draw.rect(self.background, self.COLOR_BORDER, self.background.get_rect(), 1)

        text_surf = self.font.render(self.method.capitalize() + ": " + str("%.2f" % self.value), 1, self.COLOR_TEXT)
        if self.float:
            text_surf = self.font.render(self.method.capitalize() + ": " + str(self.value), 1, self.COLOR_TEXT)
        text_rect = text_surf.get_rect(left=self.MARGIN_SIDE, top=self.MARGIN_TOP)
        self.background.blit(text_surf, text_rect)

        center_x = self.background.get_rect().width / 2
        self.box1x = center_x - self.MARGIN_BOXES - self.minus_button.get_rect().width
        self.box2x = center_x + self.MARGIN_BOXES
        self.boxy = self.background.get_rect().height - 30
        self.background.blit(self.minus_button, self.minus_button.get_rect(left=self.box1x, top=self.boxy))
        self.background.blit(self.plus_button, self.plus_button.get_rect(left=self.box2x, top=self.boxy))

        return self.background

    def is_clicked(self, mouse_pos):
        self.rect.left = self.pos[0]
        self.rect.top = self.pos[1]
        relative_pos = (mouse_pos[0] - self.rect.left, mouse_pos[1] - self.rect.top)
        if (self.minus_button.get_rect(left=self.box1x, top=self.boxy).collidepoint(relative_pos)):
            return True
        if (self.plus_button.get_rect(left=self.box2x, top=self.boxy).collidepoint(relative_pos)):
            return True
        return False

    def action(self, mouse_pos):
        self.rect.left = self.pos[0]
        self.rect.top = self.pos[1]
        relative_pos = (mouse_pos[0] - self.rect.left, mouse_pos[1] - self.rect.top)
        if (self.minus_button.get_rect(left=self.box1x, top=self.boxy).collidepoint(relative_pos)):
            self.value -= self.step_size
            if self.value < self.rng[0]: self.value = self.rng[0]
        if (self.plus_button.get_rect(left=self.box2x, top=self.boxy).collidepoint(relative_pos)):
            self.value += self.step_size
            if self.value > self.rng[1]: self.value = self.rng[1]
        self.entity[self.method] = self.value

    def update(self):
        self.value = self.entity[self.method]

class ButtonToggle(GUI_Element):

    COLOR_BG =     ( 40,  40,  40)
    COLOR_BORDER = (127, 127, 127)
    COLOR_TEXT =   (160, 160, 160)

    MARGIN_SIDE = 15
    MARGIN = 8

    def __init__(self, entity, method, font, pos=(0, 0), size=(180, 40)):
        self.entity = entity
        self.method = method

        self.pos = pos
        self.size = size

        self.font = font
        self.background = pg.Surface(size)
        self.background.fill(self.COLOR_BG)
        self.rect = self.background.get_rect()
        pg.draw.rect(self.background, self.COLOR_BORDER, self.rect, 1)


    def create_canvas(self):
        canvas = self.background.copy()
        text_surf = self.font.render(self.method.capitalize() + ": " + str(self.entity[self.method]), 1, self.COLOR_TEXT)
        text_rect = text_surf.get_rect(left=self.MARGIN_SIDE, top=self.MARGIN)
        canvas.blit(text_surf, text_rect)
        return canvas

    def is_clicked(self, mouse_pos):
        self.rect.left = self.pos[0]
        self.rect.top = self.pos[1]
        return self.rect.collidepoint(mouse_pos)

    def action(self, mouse_pos):
        self.entity[self.method] = not self.entity[self.method]

    def update(self):
        return


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

    def is_clicked(self):
        return self.rect.collidepoint(mouse_pos)

    def create_canvas(self):
        self.mouseover()
        self.surface.fill(self.bg)
        self.surface.blit(self.text_surf, self.text_rect)
        return self.surface

    def action(self, mouse_pos=None):
        self.call_back_()

    def update(self):
        return

