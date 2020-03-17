from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Line, Rectangle
from kivy.clock import Clock

__all__ = ["World", "Clock"]

class MovableRectangle(Rectangle):
    def __init__(self, *args, refresh_rate=0.08, vel=(0, 0), **kwargs):
        super().__init__(
                *args, 
                **kwargs)
        self.vel = vel
        self.grabbed = False
        Clock.schedule_interval(self.refresh, refresh_rate)

    @property
    def loc(self):
        x, y = self.pos
        w, h = self.size
        return (x + w/2, y + h/2)
    
    @loc.setter
    def loc(self, l):
        w, h = self.size
        x, y = l
        self.pos = (x - w/2, y - h/2)
    
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

    def move(self, loc):
        if self.grabbed:
            self.loc = loc

    def refresh(self, dt):
        # refresh delayed if grabbed
        if self.grabbed:
            return
        dx, dy = self.vel
        x, y = self.pos
        self.pos = (x + dx, y + dy)


class World(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.leo = MovableRectangle(
                vel=(1, 1),
                source="leo.png",
                pos=(300, 300),
                size=(100.0, 100.0))
        self.gold = MovableRectangle(
                source="gold.png",
                pos=(50, 50),
                size=(200.0, 200.0))
        self.movable = [self.leo, self.gold]
        for g in self.movable[::-1]:
            self.canvas.add(g)
        self.canvas.ask_update()
        self.grabbed = None

    def run(self):
        w = self
        class LeprechaunApp(App):
            def build(self):
                return w
        LeprechaunApp().run()

    def on_touch_up(self, touch):
        if self.grabbed is None:
            return
        self.grabbed.release()

    def on_touch_down(self, touch):
        for g in self.movable:
            g.grab(touch)
            if g.grabbed:
                self.grabbed = g
                break # only one item can be grabbed at a time

    def on_touch_move(self, touch):
        if self.grabbed is None:
            return 
        self.grabbed.move((touch.x, touch.y))

if __name__ == "__main__":
    World().run()
