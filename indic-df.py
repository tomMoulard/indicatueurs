# -*- coding: utf-8 -*-
"""
Created on thu Jun 8 16:00:00 2017

@author: tm
For python2.7
This is an indicator for Ubuntu to display disk space/usage
Uses the function df
To run simply run the command "python ./indic-thermal-cpu.py"
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
APPINDICATOR_ICON = os.path.dirname(os.path.realpath(__file__))\
                        + "/indic-df.svg"
def clearData(d):
    """
    This will betterize/reformatize the data
    The outout should be an array

    For this particular usage : 
    Filesystem      Size  Used Avail Use% Mounted on
    udev            3,9G     0  3,9G   0% /dev
    tmpfs           787M   28M  759M   4% /run
    /dev/sda1       433G  396G   16G  97% /
    tmpfs           3,9G   61M  3,8G   2% /dev/shm
    tmpfs           5,0M  4,0K  5,0M   1% /run/lock
    tmpfs           3,9G     0  3,9G   0% /sys/fs/cgroup
    /dev/loop0       80M   80M     0 100% /snap/core/1689
    /dev/loop1       79M   79M     0 100% /snap/core/1577
    /dev/loop2       79M   79M     0 100% /snap/core/1441
    tmpfs           787M  176K  787M   1% /run/user/1000
    /dev/sr0        4,4G  4,4G     0 100% /media/tm/Dexter Saison 1
    or
    ['Filesystem      Size  Used Avail Use% Mounted on',
    'udev            3,9G     0  3,9G   0% /dev',
    'tmpfs           787M   28M  759M   4% /run',
    '/dev/sda1       433G  396G   16G  97% /',
    'tmpfs           3,9G   61M  3,8G   2% /dev/shm',
    'tmpfs           5,0M  4,0K  5,0M   1% /run/lock',
    'tmpfs           3,9G     0  3,9G   0% /sys/fs/cgroup',
    '/dev/loop0       80M   80M     0 100% /snap/core/1689',
    '/dev/loop1       79M   79M     0 100% /snap/core/1577',
    '/dev/loop2       79M   79M     0 100% /snap/core/1441',
    'tmpfs           787M  176K  787M   1% /run/user/1000',
    '/dev/sr0        4,4G  4,4G     0 100% /media/tm/Dexter Saison 1',
    '']
    """
    return d.split("\n")

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
        refresh = 60  # Refresh interval in seconds

        #Get Data
        d = subprocess.check_output("df -h", shell=True)

        # GTK menu
        self.menu      = Gtk.Menu()
        self.item_time = Gtk.MenuItem("Last update: {}".\
                format(strftime("%H:%M:%S", gmtime())))
        self.item_exit = Gtk.MenuItem("Exit")
        self.item_exit.connect("activate", self.quit) 
        
        # Append menu
        self.menu.append(self.item_time)
        self.menu.append(Gtk.SeparatorMenuItem())
        
        
        #self.item_core = Gtk.MenuItem(d)
        #self.menu.append(self.item_core)
        #coreMenu
        # data = d.split("\n")
        data = clearData(d)
        for line in data:
            self.menu.append(Gtk.MenuItem(line))
        # self.menu.append(Gtk.MenuItem(d))
        self.menu.append(Gtk.SeparatorMenuItem())
        self.menu.append(self.item_exit)
        self.ind.set_menu(self.menu)
        
        #show menu
        self.menu.show_all()

        # Refresh indicator
        GLib.timeout_add_seconds(refresh,self.menu_structure) 

    def quit(self, widget):
        sys.exit(0)

if __name__ == "__main__":
    indicator = programa()
    Gtk.main()
