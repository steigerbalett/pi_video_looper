# Copyright 2015 Adafruit Industries.
# Author: Tony DiCola
# License: GNU GPLv2, see LICENSE.txt
# 2017/11/12 Small modification to also inlude 1
# subdirectory layer in search path for USB drives
# Author: Paul Stewart

import glob
import socket
import fcntl
import struct

from .usb_drive_mounter import USBDriveMounter

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915, #SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
    except:
        return None
    
class USBDriveReader:

    def __init__(self, config):
        """Create an instance of a file reader that uses the USB drive mounter
        service to keep track of attached USB drives and automatically mount
        them for reading videos.
        """
        self._load_config(config)
        self._mounter = USBDriveMounter(root=self._mount_path,
                                        readonly=self._readonly)
        self._mounter.start_monitor()


    def _load_config(self, config):
        self._mount_path = config.get('usb_drive', 'mount_path')
        self._readonly = config.getboolean('usb_drive', 'readonly')

    def search_paths(self):
        """Return a list of paths to search for files. Will return a list of all
        mounted USB drives and one layer of subdirecotries.
        """
        self._mounter.mount_all()
        vid_dirs = glob.glob(self._mount_path + '*')
        vid_dirs.extend(glob.glob(self._mount_path + '*/*'))
        # print vid_dirs
        return vid_dirs


    def is_changed(self):
        """Return true if the file search paths have changed, like when a new
        USB drive is inserted.
        """
        return self._mounter.poll_changes()

    def idle_message(self):
        """Return a message to display when idle and no files are found."""
        if get_ip_address('eth0') is None:
            return 'Insert USB Drive with compatible movies.'
        else:
            return 'Insert USB drive with compatible movies. (IP: ' + (get_ip_address('eth0')) + ')'


def create_file_reader(config):
    """Create new file reader based on mounting USB drives."""
    return USBDriveReader(config)
