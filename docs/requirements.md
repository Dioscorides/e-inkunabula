# Requirements

## Hardware used

The hardware used in this project is:

* Raspberry Pi 3 v1.2
* 16GB microSD card
* WaveShare 9.7" e-ink display
* WaveShare e-ink display driver board (IT8951)
* 5V 2A power supply
* Synology DS218+ NAS

The Raspberry Pi and the microSD card are required as they will host and run the necessary scripts to update the e-ink display.

The WaveShare 9.7" e-ink display and the WaveShare IT8951 e-ink display driver board are required. This e-ink displays HD images and requires the additional IT8951 driver board to function.

!!! DANGER
    You can neither immediately connect the WaveShare 9.7" e-ink display directly to the Raspberry Pi nor can you connect the WaveShare ESP32 driver directly to this e-ink display. You **need the WaveShare IT8951 e-ink display driver board** to connect the e-ink display to either the Raspberry Pi or the ESP32 driver board - and to follow along with this guide.

## Software used

The software used in this project is:

* Raspbian
* Python 3.7
* BCM2835 library
* WaveShare IT8951 library
* Docker (running on Synology DS218+)
* Portainer (via Docker, running on Synology DS218+ - Optional: you can create a stack using the Synology interface directly.)
* Home Assistant (via Docker, running on Synology DS218+)
* [sibbl/hass-lovelace-kindle-screensaver](https://github.com/sibbl/hass-lovelace-kindle-screensaver) (via Docker, running on Synology DS218+)
* [Inkycal v.2.0.2](https://github.com/aceinnolab/Inkycal/releases/tag/v2.0.2)

!!! Note
    **We are using Inkycal v.2.0.2 specifically**. This is because we are going to edit some files from that project. If you are using a different version, the files we are going to edit might be different - or the issues we fixed might have been fixed already.
