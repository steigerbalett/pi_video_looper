#!/bin/sh

# Error out if anything fails.
set -e

# Make sure script is run as root.
if [ "$(id -u)" != "0" ]; then
  echo "Must be run as root with sudo! Try: sudo ./install.sh"
  exit 1
fi

echo "Installing dependencies..."
echo "=========================="
apt-get update
apt-get -y install build-essential python-dev python-pip python-pygame supervisor git omxplayer exfat-fuse exfat-utils ntfs-3g

echo "Installing video_looper program..."
echo "=================================="
mkdir -p /mnt/usbdrive0 # This is very important if you put your system in readonly after
python setup.py install --force
cp video_looper.ini /boot/video_looper.ini

echo "Configuring video_looper to run on start..."
echo "==========================================="
cp video_looper.conf /etc/supervisor/conf.d/
service supervisor restart

if grep gpu_mem /boot/config.txt; then
  echo "Not changing GPU memory since it's already set"
else
  echo "Increasing GPU memory..."
  echo "========================"
  echo "" >> /boot/config.txt
  echo "# Increase GPU memory to avoid video playback problems" >> /boot/config.txt
  echo "gpu_mem=128" >> /boot/config.txt
fi

echo "Disable undervoltage bolt"
echo "========================"
echo "" >> /boot/config.txt
echo "# Disable under-voltage warning" >> /boot/config.txt
echo "avoid_warnings=1" >> /boot/config.txt

echo "Disable overscan"
echo "========================"
echo "" >> /boot/config.txt
echo "# Disable overscan" >> /boot/config.txt
echo "disable_overscan=1" >> /boot/config.txt


echo "Finished!"
