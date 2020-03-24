#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Hidden module not used for front facing code, so it's not going to be
documented well
"""

import logging
import os

# kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window


__all__ = ["World", "Clock"]


class MovableRectangle(Rectangle):
    def __init__(self, *args, refresh_rate=0.08, vel=(0, 0), **kwargs):
        super().__init__(*args, **kwargs)
        self._vel = vel
        self.grabbed = False
        Clock.schedule_interval(self.refresh, refresh_rate)
        self.log = logging.getLogger("kivy")

    @property
    def loc(self):
        x, y = self.pos
        w, h = self.size
        return (round(x + w / 2, 2), round(y + h / 2, 2))

    @loc.setter
    def loc(self, l):
        w, h = self.size
        x, y = l
        self.pos = (x - w / 2, y - h / 2)

    @property
    def vel(self):
        return self._vel

    @vel.setter
    def vel(self, v):
        v = (round(v[0], 2), round(v[1], 1))
        #TODO enforce max velocity
        max_dx, max_dy = (5, 5)
        dx, dy = v
        # check speed in x direction
        dx = max(dx, -1*max_dx)
        dx = min(dx, max_dx)
        # check speed in y direction
        dy = max(dy, -1*max_dy)
        dy = min(dy, max_dy)

        self._vel = (dx, dy)

        if self._vel != v:
            self.log.warning(
                    f"clover-object: vel={self._vel}, max speed reached!")

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
        dx, dy = self._vel
        x, y = self.pos
        self.pos = (x + dx, y + dy)


class World(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        w, h = self.size
        # get leo set up
        leo_png = os.path.join(dir_path, "leo.png")
        leo = MovableRectangle(source=leo_png, size=(100.0, 100.0))
        self.leo = None # initially leo is not in the world
        # get gold set up
        gold_png = os.path.join(dir_path, "gold.png")
        gold = MovableRectangle(source=gold_png, size=(200.0, 200.0))
        self.gold = None # initially leo is not in the world
        # nothing is movable and everything is addable at first
        self.movable = []
        self.addable = [gold, leo] # used to track additions
        self.grabbed = None

    def on_touch_up(self, touch):
        if self.grabbed is None:
            return
        self.grabbed.release()

    def on_touch_down(self, touch):
        w, h = self.size
        if self.gold is None:
            self.gold = self.addable.pop(0)
            self.gold.loc = (touch.x, touch.y)
            self.canvas.add(self.gold)
            self.canvas.ask_update()
            self.movable.append(self.gold)
            self.movable = [self.gold] + self.movable
        elif self.leo is None:
            self.leo = self.addable.pop(0)
            self.leo.loc = (touch.x, touch.y)
            self.canvas.add(self.leo)
            self.canvas.ask_update()
            self.movable = [self.leo] + self.movable
        for g in self.movable:
            g.grab(touch)
            if g.grabbed:
                self.grabbed = g
                break  # only one item can be grabbed at a time

    def on_touch_move(self, touch):
        if self.grabbed is None:
            return
        self.grabbed.move((touch.x, touch.y))


class CloverApp(App):
    def __init__(
            self, 
            on_leo=None, 
            on_gold=None, 
            snapshot_rate=0.2,
            *args, 
            **kwargs):
        super().__init__(*args, **kwargs)
        Window.clearcolor = (0.298, 0.447, 0.149, 1)
        self.world = World()
        # prepare updating
        self.on_leo = on_leo
        self.on_gold = on_gold
        Clock.schedule_interval(self.on_snapshot, snapshot_rate)
        self.snapshot = (None, None)
        self.log = logging.getLogger("kivy")

    def on_snapshot(self, dt):
        leo_loc, gold_loc = self.snapshot
        # leo exists, leo changed location
        if (self.world.leo is not None and 
                self.world.leo.loc != leo_loc):
            # callback exists
            if self.on_leo is not None:
                self.on_leo(self.world.leo)
            leo_loc = self.world.leo.loc
            leo_vel = self.world.leo.vel
            self.log.info(f"clover-leo: vel={leo_vel} loc={leo_loc}")
        if (self.world.gold is not None and 
                self.world.gold.loc != gold_loc):
            # callback exists
            if self.on_gold is not None:
                self.on_gold(self.world.gold)
            gold_loc = self.world.gold.loc
            self.log.info(f"clover-gold: loc={gold_loc}")
        self.snapshot = (leo_loc, gold_loc)

    def set_leo_vel(self, vel):
        if self.world.leo is None:
            # log something
            return
        self.world.leo.vel = vel

    def build(self):
        return self.world
