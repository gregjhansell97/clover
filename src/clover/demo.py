#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clover.gui import CloverApp, Clock



# may want to consider bounding speed
app = CloverApp(title="leo-demo")


def tick(time_interval):
    if app.world.gold is None or app.world.leo is None:
        return
    try:
        gold_x, gold_y = app.world.gold.loc
        leo_x, leo_y = app.world.leo.loc
    except AttributeError:
        return
    scale_factor = 0.01
    dx = scale_factor * (gold_x - leo_x)
    dy = scale_factor * (gold_y - leo_y)
    app.world.leo.vel = (dx, dy)


def main():
    Clock.schedule_interval(tick, 0.01)
    app.run()
