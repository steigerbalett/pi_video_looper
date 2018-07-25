# Author: Jason Zylks
# License: GNU GPLv2, see LICENSE.txt

import json
import os

import Queue

import cec


KEY_DOWNARROW = 2
KEY_UPARROW = 1
KEY_SELECT = 0
KEY_PLAY = 68

cec_queue = Queue.Queue()

def cec_handler(event_id, key_id, duration):
    print key_id, duration
    if duration != 0:
        return
    if event_id != cec.EVENT_KEYPRESS:
        return
    cec_queue.put_nowait(key_id)

cec.init()
cec.add_callback(cec_handler, cec.EVENT_KEYPRESS)

class InteractiveReader(object):

    def __init__(self, config):
        self._load_config(config)
        self._selected_item = 0
        self._selection_confirmed = False

    def _load_config(self, config):
        self._paths = json.loads(config.get('interactive', 'paths'))

    def search_paths(self):
        """Return a list of paths to search for files."""
        return [self._paths[self._selected_item]]

    def is_changed(self):
        return not self._selection_confirmed

    def idle_message(self):
        """Return a message to display when idle and no files are found."""
        return 'No files found in {0}'.format(self._paths[self._selected_item])

    def menu(self):
        menu_options = [os.path.basename(path) for path in self._paths]
        return menu_options, self._selected_item

    def selection_confirmed(self):
        return self._selection_confirmed
    
    def handle_keypress(self):
        try:
            key_id = cec_queue.get(block=False)
        except Queue.Empty:
            return
        if key_id == KEY_DOWNARROW:
            self._selection_confirmed = False
            self._selected_item = min(len(self._paths) - 1, self._selected_item + 1)
        elif key_id == KEY_UPARROW:
            self._selection_confirmed = False
            self._selected_item = max(0, self._selected_item - 1)
        elif key_id == KEY_SELECT:
            self._selection_confirmed = True
    

def create_file_reader(config):
    """Create new file reader based on reading a directory on disk."""
    return InteractiveReader(config)
