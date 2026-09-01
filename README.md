# Mixy
 Custom peripheral to mix game and chat audio on the fly, meant to emulate the Steelseries chatmix dial.
 Tested with Python 3.14.7, PipeWire on Fedora.

<img src="https://github.com/adambdia/mixy/blob/main/mixy.jpg?raw=true" alt="Mixy Device" width="357" height="300">

## Usage
Turn all the way to the left for desktop only, and all the way to the right for chat only. Center the dial to equalize both. You'll hear a pop noise when you've centered the dial for feedback.

## Build your own

### What you'll need
- A potentiometer, I used a generic 10k I had laying around
- A dial for your potentiometer, I got some nice metal ones on Aliexpress but you can 3D print one if you wish
- A USB-C microcontroller, I used a clone of the [Waveshare RP2040-zero ](https://www.waveshare.com/rp2040-zero.htm)
  - If not using a pi pico you'll need to modify the platformio.ini
- 4 M3x4mm threaded inserts
- 4 M3x5mm screws
  - I used hex button head screws because I think they look nice
- Some wire
- Hot glue

### Steps
- Print the `mixy-shell.stl` and `mixy-lid.stl` from the hardware folder
- Add the threaded inserts to the shell
- Solder up the potentiometer as a 3.3V voltage divider to pin 26
- Screw on the potentiometer to the lid with its nut
- Hotglue the board in place with the USB port flush with the shell
- Upload code to board from the firmware folder with platformio

## Setup Software
- Create a venv and install packages from `requirements.txt`
- Add yourself to the dialout group with `sudo usermod -aG dialout $USER`
- Create a mixy.service file in `/home/USER/.config/systemd/user` with the following contents
```
[Unit]
Description=Mixy Audio Dial Service
# Wait until PipeWire and the user audio session are fully loaded
After=pipewire.service pipewire-pulse.service wireplumber.service

[Service]
Type=simple
# Replace with the absolute path to your Python interpreter and script
ExecStart=/pathtovenv/bin/python3 /pathtomixy/host-software/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```
- Enable the service and start the service with the following commands
```
systemctl --user daemon-reload
systemctl --user enable mixy.service
systemctl --user start mixy.service
```
- Find your speakers/headphones with `pactl list sinks short | grep -v mixy` and replace the one in `99-mixy-sinks.conf` at `target.object = "YOURDEVICE"`
- Copy or symlink the conf file with `ln -sf /home/adam/Documents/mixy/host-software/99-mixy-sinks.conf ~/.config/pipewire/pipewire.conf.d/99-mixy-sinks.conf` then log out and back in
- Use something like [pavucontrol](https://flathub.org/en/apps/org.pulseaudio.pavucontrol) to make sure all the audio devices are pointing to the right places
- Done!
