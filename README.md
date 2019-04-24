An application to turn your Raspberry Pi into a dedicated looping video playback device.
Can be used in art installations, fairs, theatre, events, infoscreens, advertisment etc...

Easy to use out of the box but also has a lot of settings to make it fit your use case.

If you miss a feature just post an issue on github. (https://github.com/adafruit/pi_video_looper)


#### new in v1.0.1:
 - reworked for python3
 - keyboard control (quiting the player)
 - option for displaying an image instead of a blank screen between videos

#### how to install:
sudo ./install.sh

for a detailed tutorial visit: https://learn.adafruit.com/raspberry-pi-video-looper/installation

Just plugin your USB-Drive to the RaspberryPi and it will scan it for movies. After a few seconds it will start to play the movies found in the root and +1 subdirectory in an endless loop. You can stop the videlooper by hitting the [ESC] - Key.
  
 
Changes:
Show IP-Adress on startup (PIMIYA)
Added ExFat support (PIMIYA)
Added search for files in root + 1 subdirectory (pauldast)
Added NTFS support (gazzer82)
Added passibility to change the countdowntime in the configfile (JAVL)
Removed the undervoltagebolt

This is a Project to learn github.
