from functools import partial

from gui import World, Clock


w = World()


# may want to consider bounding speed
def tick(time_interval):
    gold_x, gold_y = w.gold.loc
    leo_x, leo_y = w.leo.loc
    scale_factor = 0.01
    dx = scale_factor*(gold_x - leo_x)
    dy = scale_factor*(gold_y - leo_y)
    w.leo.vel = (dx, dy)
    
if __name__ == "__main__":
    Clock.schedule_interval(tick, 0.01)
    w.run()
