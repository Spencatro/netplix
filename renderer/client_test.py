#! /usr/bin/python
"""
This program is adapted from a simple libVLC / GTK  widget.

This file loads a streaming resource and plays or pauses, according to commands it pulls from a server "heartbeat."
"""

#
# gtk example/widget for VLC Python bindings
# Copyright (C) 2009-2010 the VideoLAN team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#

import json
import sys
import os.path as path
import threading
import time
import requests

PROJECT_PATH = path.normpath(path.join(path.dirname(path.realpath(__file__)), ".."))

sys.path.insert(0,PROJECT_PATH)

import config

import gtk
gtk.gdk.threads_init()

import sys
import vlc

from gettext import gettext as _

# Create a single vlc.Instance()
instance = vlc.Instance()

class VLCWidget(gtk.DrawingArea):
    """Simple VLC widget.

    Its player can be controlled through the 'player' attribute, which
    is a vlc.MediaPlayer() instance.
    """
    def __init__(self, *p):
        gtk.DrawingArea.__init__(self)
        self.player = instance.media_player_new()
        def handle_embed(*args):
            if sys.platform == 'win32':
                self.player.set_hwnd(self.window.handle)
            else:
                self.player.set_xwindow(self.window.xid)
            return True
        self.connect("map", handle_embed)
        self.set_size_request(320, 200)

class DecoratedVLCWidget(gtk.VBox):
    """Decorated VLC widget.

    VLC widget decorated with a player control toolbar.

    Its player can be controlled through the 'player' attribute, which
    is a Player instance.
    """
    def __init__(self, *p):
        gtk.VBox.__init__(self)
        self._vlc_widget = VLCWidget(*p)
        self.player = self._vlc_widget.player
        self.pack_start(self._vlc_widget, expand=True)
        self._toolbar = self.get_player_control_toolbar()
        self.pack_start(self._toolbar, expand=False)

    def get_player_control_toolbar(self):
        """Return a player control toolbar
        """
        tb = gtk.Toolbar()
        tb.set_style(gtk.TOOLBAR_ICONS)
        tb.show_all()
        return tb

class VideoPlayer:
    """Simple video player.
    """
    def __init__(self):
        self.vlc = DecoratedVLCWidget()

    def update_media(self, new_media):
        self.vlc.player.set_media(instance.media_new(new_media))

    def make_request(self, pass_number = 1):
        """
        Helps keep requests simple; will retry 3 times on failure before returning None, which will cause an exception from the caller
        """
        result = None
        http_result = requests.get(config.SERVER_URL+"/heartbeat/")
        try:
            result = json.loads(http_result.text)
        except:
            pass
        if not result or result['uri'] == None:
            if pass_number < 3:
                time.sleep(.5)
                return self.make_request(pass_number+1)
            else:
                return None
        return result['uri']

    def heartbeat(self):
        """
        Continuously poll the server on 1 second intervals to see if there are any new commands to handle
        """
        while(1):
            time.sleep(1)
            uri = self.make_request()
            if uri != self.uri:
                # Only check for commands if the URI has changed (this signals a new command has been issued)
                self.uri = uri
                if uri:
                    # A play command always contains a valid URI, so update the media and play
                    self.update_media(self.uri)
                    self.vlc.player.play()
                else:
                    # A pause command will contain a null URI, so stop the player
                    self.vlc.player.stop()

    def main(self):
        # Create a thread for the heartbeat
        self.heartbeat_thread = threading.Thread(target=self.heartbeat)
        self.heartbeat_thread.start()

        # Allocate a variable for the uri
        self.uri = ""

        # Create GTK resources
        w = gtk.Window()
        w.add(self.vlc)
        w.show_all()
        w.connect("destroy", gtk.main_quit)

        #Run the program
        gtk.main()

if __name__ == '__main__':
    p=VideoPlayer()
    p.main()