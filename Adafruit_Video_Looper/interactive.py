# Author: Jason Zylks
# License: GNU GPLv2, see LICENSE.txt

import json
import os

import cec


KEY_DOWNARROW = 2
KEY_UPARROW = 1
KEY_SELECT = 0
KEY_PLAY = 68


class InteractiveReader(object):

    def __init__(self, config):
        self._load_config(config)
        self._selected_item = 0
        self._selection_confirmed = False
        self._paused = False
        cec.init()
        cec.add_callback(self.handle_keypress, cec.EVENT_KEYPRESS)

    def _load_config(self, config):
        self._paths = json.loads(config.get('directory', 'paths'))

    def search_paths(self):
        """Return a list of paths to search for files."""
        return [self._paths[self._selected_item]]

    def is_changed(self):
        return not self._selection_confirmed

    def idle_message(self):
        """Return a message to display when idle and no files are found."""
        return 'No files found in {0}'.format(self._paths[self._selected_item])

    def menu(self):
        menu_options = [[os.path.basename(path), path] for path in self._paths]
        return menu_options, self._selected_item

    def selection_confirmed(self):
        return self._selection_confirmed

    def handle_keypress(self, event_id, key_id, duration):
        if duration != 0:
            return
        if event_id != cec.EVENT_KEYPRESS:
            return
        if key_id == KEY_DOWNARROW:
            self._selection_confirmed = False
            self._selected_item += 1
        elif key_id == KEY_UPARROW:
            self._selection_confirmed = False
            self._selected_item -= 1
        elif key_id == KEY_SELECT:
            self._selection_confirmed = True
        elif key_id == KEY_PLAY:
            self._paused = not self._paused


def create_file_reader(config):
    """Create new file reader based on reading a directory on disk."""
    return InteractiveReader(config)
