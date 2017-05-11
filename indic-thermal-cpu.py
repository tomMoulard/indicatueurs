# -*- coding: utf-8 -*-
"""
Created on Wen May 10 16:00:00 2017

@author: tm
This is an indicator for Ubuntu to display core temperature
Uses the function sensors
"""


#main import to display the indicator
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")

import os

import subprocess

import sys
from time import gmtime, strftime

from gi.repository import Gtk, Gdk, GLib, GObject
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID = "indic-thermal-cpu"
APPINDICATOR_ICON = os.path.dirname(os.path.realpath(__file__)) + "/indic-thermal-cpu.svg"
class programa:

    def __init__(self):
    # Create Indicator with icon and label
        # If leave empty "" then load empty icon
        self.ind = appindicator.Indicator.new(APPINDICATOR_ID,\
            APPINDICATOR_ICON,\
            appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE) # 
        self.menu_structure()

    # Menu structure
    def menu_structure(self):
        refresh      = 5  # Refresh interval in seconds

        #Get Data
        #Can use inxi -Fx
        d = subprocess.check_output("sensors", shell=True)
        d += "Batterie: " + subprocess.check_output("acpi -V", shell=True)

        # GTK menu
        self.menu      = Gtk.Menu()
        self.item_time = Gtk.MenuItem("Last update: {}".format(strftime("%H:%M:%S", gmtime())))
        self.item_exit = Gtk.MenuItem("Exit")
        self.item_exit.connect("activate", self.quit) 
        
        # Append menu
        self.menu.append(self.item_time)
        self.menu.append(Gtk.SeparatorMenuItem())
        
        
        #self.item_core = Gtk.MenuItem(d)
        #self.menu.append(self.item_core)
        #coreMenu
        data = d.split("\n")
        for line in data:
            self.menu.append(Gtk.MenuItem(line))
        self.menu.append(Gtk.SeparatorMenuItem())
        self.menu.append(self.item_exit)
        self.ind.set_menu(self.menu)
        
        #show menu
        # self.item_time.show()
        # self.item_exit.show()
        self.menu.show_all()

        # Refresh indicator
        GLib.timeout_add_seconds(refresh,self.menu_structure) 

    def quit(self, widget):
        sys.exit(0)

if __name__ == "__main__":
    indicator = programa()
    Gtk.main()