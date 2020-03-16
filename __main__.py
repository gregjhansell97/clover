

from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Line, Rectangle
from kivy.clock import Clock

class GrabableRectangle(Rectangle):
    def __init__(self, *args, **kwargs):
        super().__init__(
                *args, 
                **kwargs)
        self.grabbed = False
    
    def grab(self, touch):
        (x, y) = (touch.x, touch.y)
        (g_x, g_y) = self.pos
        (g_w, g_h) = self.size
        if 0 < x - g_x < g_w and 0 < y - g_y < g_h:
            self.size = (self.size[0] + 1, self.size[1] + 1)
            self.grabbed = True

    def release(self):
        if self.grabbed:
            self.grabbed = False
            self.size = (self.size[0] - 1, self.size[1] - 1)

    def move(self, pos):
        if self.grabbed:
            x, y = pos
            (g_w, g_h) = self.size
            self.pos = (x - g_w/2, y - g_h/2) 

        

class World(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.leo = GrabableRectangle(
                source="leo.png",
                pos=(300, 300),
                size=(100.0, 100.0))
        self.gold = GrabableRectangle(
                source="gold.png",
                pos=(50, 50),
                size=(200.0, 200.0))
        self.grabable = [self.leo, self.gold]
        for g in self.grabable[::-1]:
            self.canvas.add(g)
        self.canvas.ask_update()

    def on_touch_up(self, touch):
        for g in self.grabable:
            g.release()

    def on_touch_down(self, touch):
        for g in self.grabable:
            g.grab(touch)
            if g.grabbed:
                break # only one item can be grabbed at a time

    def on_touch_move(self, touch):
        for g in self.grabable:
            g.move((touch.x, touch.y))

class LeprechaunApp(App):
    def build(self):
        w = World()
        return w

if __name__ == "__main__":
    LeprechaunApp().run()
