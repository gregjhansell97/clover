#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import importlib.util
from threading import Thread
import time

from pubsub import pub

def run_app():
    # need to import in thread (kivy breaks otherwise)
    from clover.gui import CloverApp
    # set up publish points 
    def on_leo(leo):
        pub.sendMessage("leo.location", loc=leo.loc)
    def on_gold(gold):
        pub.sendMessage("gold.location", loc=gold.loc)
     
    app = CloverApp(
            on_leo=on_leo, 
            on_gold=on_gold, 
            snapshot_rate=0.2,
            title="clover-pypubsub")
    # set up subscriptions
    pub.subscribe(app.set_leo_vel, "leo.velocity")
    app.run()

def main():
    # start kivy app
    app_thread = Thread(target=run_app, daemon=True)
    app_thread.start()
    # grab file name from system args
    filename = sys.argv[1]
    # TODO handle incorrect file name input
    spec = importlib.util.spec_from_file_location("", filename)
    foo = importlib.util.module_from_spec(spec)
    # run module provided
    spec.loader.exec_module(foo)
