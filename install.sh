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
apt update
apt -y full-upgrade
apt -y install build-essential python-dev python-pip python-pygame supervisor git omxplayer exfat-fuse exfat-utils ntfs-3g hfsutils hfsprogs

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
  echo "Increasing GPU memory (universal)..."
  echo "========================"
  echo "" >> /boot/config.txt
  echo "# Increase GPU memory to avoid video playback problems" >> /boot/config.txt
  echo "gpu_mem_256=128" >> /boot/config.txt
  echo "gpu_mem_512=256" >> /boot/config.txt
  echo "gpu_mem_1024=256" >> /boot/config.txt
fi

if grep avoid_warnings=1 /boot/config.txt; then
  echo "Undervoltge-Tweak already set"
else
echo "Disable undervoltage bolt"
echo "========================"
echo "" >> /boot/config.txt
echo "# Disable under-voltage warning" >> /boot/config.txt
echo "avoid_warnings=1" >> /boot/config.txt
fi

if grep disable_overscan=1 /boot/config.txt; then
  echo "Overscan-Tweak already set"
else
echo "Disable overscan"
echo "========================"
echo "" >> /boot/config.txt
echo "# Disable overscan" >> /boot/config.txt
echo "disable_overscan=1" >> /boot/config.txt
fi

if grep disable_splash=1 /boot/config.txt; then
  echo "Splashscreen-Tweak already set"
else
echo "Disable Splashscreen"
echo "========================"
echo "" >> /boot/config.txt
echo "# Disable Splashscreen" >> /boot/config.txt
echo "disable_splash=1" >> /boot/config.txt
fi

echo "Force FullHD 1920x1080"
echo "========================"
echo "" >> /boot/config.txt
echo "# Force FullHD 1920x1080" >> /boot/config.txt
echo "hdmi_group=1" >> /boot/config.txt
echo "hdmi_mode=16" >> /boot/config.txt

echo "Finished!"
