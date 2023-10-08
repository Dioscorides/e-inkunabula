# Installation

## Hardware

1. Connect the IT8951 driver board to the Raspberry Pi using the [40-pin GPIO header](https://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/).
2. Connect the WaveShare 9.7" e-ink display to the 9.7" e-ink display adapter, and connect the 9.7" e-ink display adapter to the IT8951 driver board using the FPC cable[^1]. The FPC cable is the orange cable at the bottom of your display.

[^1]: You can connect the FPC cable directly to the IT8951 driver board, but this is not recommended as it is more difficult to move the Raspberry Pi around and, later on, hide it in a case.

## Software

This guide is structured as follows:

* [Step 1 - Setting up Home Assistant and Kiosk Mode](#step-1---setting-up-home-assistant-and-kiosk-mode) - We will use [Home Assistant](https://www.home-assistant.io/) in "Kiosk mode" to create a view that is optimized for our e-ink display.
* [Step 2 - Setting up Home Assistant Lovelace Kindle Screensaver](#step-2---setting-up-home-assistant-lovelace-kindle-screensaver) - We will use [Home Assistant Lovelace Kindle Screensaver](https://github.com/sibbl/hass-lovelace-kindle-screensaver) to take a screenshot of our Home Assistant view.
* [Step 3 - Setting up the Raspberry Pi](#step-3---setting-up-the-raspberry-pi) and [Step 4 - Installing Inkycal on the Raspberry Pi](#step-4---installing-inkycal-on-the-raspberry-pi) - Next we will set up the Raspberry Pi and install [Inkycal](https://github.com/aceinnolab/Inkycal) on it.
* [Step 5 - Modifying Inkycal's files](#step-5---modifying-inkycals-files) and [Step 6 - Import your screenshot to the Raspberry Pi and autostarting](#step-6---import-your-screenshot-to-the-raspberry-pi-and-autostarting) - Finally, we will use a Python script to fetch the screenshot from the server to the Raspberry Pi and display it on the e-ink display.

### Important notes before you start

This guide assumes you have Home Assistant (HA) already up and running. In this guide Home Assistant instance is running on a Synology DS218+ NAS, but the workflow should work if you are running HA in other ways as well.

We will also reference to [Portainer](https://www.portainer.io/). Portainer is a Docker management tool that makes it easier to manage Docker containers and we will use is to create a stack to run [Home Assistant Lovelace Kindle Screensaver](https://github.com/sibbl/hass-lovelace-kindle-screensaver). You can use Synology's Container Manager to create a stack too, but Portainer is easier to use[^2] and the Community Edition (CE) is free.

[^2]: If you are using Synology's Container Manager, but are interested in Portainer you can follow [this excellent guide](https://mariushosting.com/synology-30-second-portainer-install-using-task-scheduler-docker/) to install Portainer on your Synology NAS.

## Step 1 - Setting up Home Assistant and Kiosk Mode

This is not strictly necessary, but we recommend setting up a dedicated view in Home Assistant for your e-ink display using "Kiosk Mode". This will allow you to create a view that is optimized for your e-ink display by removing unnecessary elements, such as the sidebar and the header.

While out of the scope of this guide, here is a quick guide on how to install HACS for Home Assistant running on a Synology NAS:

1. Manually download the latest version of HACS from this link: [HACS Releases](https://github.com/hacs/integration/releases).
2. After downloading, unzip the contents of the `hacs.zip` file on your computer.
3. Using Synology's "File Station", locate your Home Assistant docker installation directory, usually located in the `/volume1/docker/` folder.
4. Navigate to the `custom_components` folder within your Home Assistant directory.
5. Copy the contents of the unzipped HACS folder into the custom_components/hacs directory.
6. Restart your Home Assistant server to apply the changes.
7. Open your Home Assistant web interface.
8. Navigate to "Configuration" and then "Integrations."
9. Search for the HACS integration and activate it.

If you know how to SSH directly into your Home Assistant docker container, you can also install HACS using the following command - although you might encounter issues we are not covering in this guide:

``` bash
wget -O - https://get.hacs.xyz | bash -
```

Refer to the [HACS Documentation](https://hacs.xyz/docs/configuration/basic/) for additional guidance on initial configuration and how to view a "kiosked" view in Home Assistant.

If the HACS integration does not appear:

1. Try using a different web browser.
2. Clear your browser cache and attempt the search again.

Open HACS by clicking "HACS" on the Home Assistant sidebar, and install [Kiosk Mode](https://github.com/maykar/kiosk-mode). Have fun creating a view that is optimized for your e-ink display!

!!! Tip
    Consider also installing [layout-card](https://github.com/thomasloven/lovelace-layout-card#layout-card) using HACS for more control on how your view is displayed.

## Step 2 - Setting up Home Assistant Lovelace Kindle Screensaver

Now that we have a dedicated view for our e-ink display, we want to take screenshots of it. We are going to use [Home Assistant Lovelace Kindle Screensaver](https://github.com/sibbl/hass-lovelace-kindle-screensaver) via a docker container to achieve this.

!!! Note
    As mentioned earlier, we will be using Portainer for this step.

1. Create a new folder in your Synology NAS. We will use `/volume1/docker/screenshotter` in this guide.
2. Got to your Portainer instance and create a new stack. You can do this by clicking on `Stacks` in the left sidebar, and then clicking on `Add stack`:
    * Give your stack a name. We will use `screenshotter`.
    * As `Build method` select `Web editor`.
    * In the `Web editor` field, copy and paste the following code:

    ``` yaml
    version: "3.8"

    services:
      app:
        image: sibbl/hass-lovelace-kindle-screensaver:latest
        environment:
          - HA_BASE_URL=http://YOUR_LOCAL_HOME_ASSISTANT_IP:PORT
          - HA_SCREENSHOT_URL=/dashboard-kiosk/default_view?kiosk
          - HA_ACCESS_TOKEN=
          - CRON_JOB=*/1 * * * *
          - RENDERING_TIMEOUT=30000
          - RENDERING_DELAY=0
          - RENDERING_SCREEN_HEIGHT=805
          - RENDERING_SCREEN_WIDTH=1150
          - COLOR_MODE=TrueColor
          - GRAYSCALE_DEPTH=16
          - OUTPUT_PATH=/output/image.png
          - LANGUAGE=en
        deploy:
          restart_policy:
            condition: on-failure
            delay: 5s
            max_attempts: 3
            window: 120s

        ports:
          - 7799:5000
        volumes:
          - /volume1/docker/screenshotter/output:/output:rw
    ```

    Be mindful of the indentations.

    An explanation of the different fields:

    * `image`: The image that will be used to run the container. We will use `sibbl/    hass-lovelace-kindle-screensaver:latest` in this guide. `latest` is **version 1.0.5**   at the time of writing.
    * `HA_BASE_URL`: The URL of your local Home Assistant instance.
    * `HA_SCREENSHOT_URL`: The path of the view you want to take a screenshot of.
    * `HA_ACCESS_TOKEN`: The access token of your Home Assistant instance. See [Creating    a Home Assistant Access Token](#creating-a-home-assistant-access-token) for more   information.
    * `CRON_JOB`: The cron job that will be used to take a screenshot of your Home  Assistant view. The default value is `*/1 * * * *`, which means that a screenshot    will be taken every minute. You can change this value to your liking.
    * `RENDERING_TIMEOUT`: The timeout for the screenshot. The default value is `30000`,    which means that the screenshot will timeout after 30 seconds. You can change this     value to your liking.
    * `RENDERING_DELAY`: The delay before the screenshot is taken. The default value is     `0`. In our case, changing this value resulted in HA's cards not being rendered     correctly, so we left it at `0`.
    * `RENDERING_SCREEN_HEIGHT`: The height of the screenshot. Check the specifications     of your e-ink display to find out what the height of your display is. From there,   experiment with different values to find out what works best for you.
    * `RENDERING_SCREEN_WIDTH`: The width of the screenshot. Same as above.
    * `COLOR_MODE`: The color mode of the screenshot. Since our WaveShare 9.7" e-ink    display can display HD images at 16bit Grayscale, we set this value to `TrueColor` as  the screen is capable of rendering the various shades of colors transformed to gray.
    * `GRAYSCALE_DEPTH`: The grayscale depth of the screenshot. Since our WaveShare 9.7"    e-ink display can display HD images at 16bit Grayscale, we set this value to `16`  (optional).
    * `OUTPUT_PATH`: The path where the screenshot will be saved. We will use `/output/ image.png` in this guide.
    * `LANGUAGE`: The language of the screenshot. We will use `en` in this guide    (optional).
    * `restart_policy`: The restart policy of the container. We are using `on-failure`,     with a `delay` of `5s`, `max_attempts` of `3`, and a `window` of `120s` in this case.   This means that the container will be restarted if it fails, with a delay of 5    seconds between each attempt, a maximum of 3 attempts, and a window of 120 seconds. You can change these values to your liking.
    * `ports`: The port that will be used to access the container. We will use `7799` in this guide.
3. Click on `Deploy stack`.
4. Navigate to `http://YOUR_LOCAL_HOME_ASSISTANT_IP:7799` to check if the container is running correctly. You should see a screenshot of the Home Assistant view you specified in the `HA_SCREENSHOT_URL` field.

### Creating a Home Assistant Access Token

The easiest way to create a Home Assistant access token is to use the navigate to your Home Assistant instance, login as an administrator, click on your profile picture in the bottom left corner, scroll down to the `Long-Lived Access Tokens` section, and click on `Create Token`. Give your token a name, and copy the token to your clipboard. Paste the token in the `HA_ACCESS_TOKEN` field in the Portainer stack here above.

## Step 3 - Setting up the Raspberry Pi

We finally have an image of a Home Assistant dashboard. Now we "just" need to display it on our e-ink display! First up, we need to install Raspberry Pi OS on our Raspberry Pi:

* Install Raspberry Pi OS using [Raspberry Pi Imager](https://www.raspberrypi.com/software/). Follow the on-screen instructions and **make sure you pre-configure your WiFi settings and enable SSH**.

!!! Tip
    Note down your `hostname`, `username`, and `password` you have chosen, as you will need them to SSH into your Raspberry Pi later on. You can find more information about how to SSH into your Raspberry Pi [here](https://www.raspberrypi.com/documentation/computers/remote-access.html#ssh-access-to-the-pi).

After installing Raspberry Pi OS, boot your Raspberry Pi and try to SSH into using, as an example, [Terminus](https://termius.com/) or [Solar-PuTTY](https://www.solarwinds.com/free-tools/solar-putty).

## Step 4 - Installing Inkycal on the Raspberry Pi

We have the screenshot, we have a working Raspberry Pi. Now it's time to install Inkycal on the Raspberry Pi: a Python application that will allow us to display the screenshot on our e-ink display.

!!! Warning
    We are using **Inkycal v.2.0.2 specifically**! Inkycal is in constant development, and the issues encountered in this guide might have been fixed already. If you are using a different version, the files we are going to edit might be different.

!!! Warning
    You might encounter issues while installing Inkycal on your Raspberry Pi. Check the [Troubleshooting](#troubleshooting) section for more information.

1. Follow the instructions at [Inkycal's GitHub page](https://github.com/aceinnolab/Inkycal) to install Inkycal on your Raspberry Pi.
2. Step 2 on the Inkcal's guide will tell you to create a `settings.json` file to flash in the `/boot` folder, using their [web-ui](https://aceisace.eu.pythonanywhere.com/inkycal-config-v2-0-0). Do so, and fill the fields with the information that applies to your case.  
   In the `Modules config` area you should add only 1 module: `Inkycal Image`, with a `Module height (by ratio)` of `1`. Click on `Generate settings file` and download the `settings.json` file.

    For reference, the following is the `settings.json` we'll be using for this guide:

    ``` json
    {
        "model": "9_in_7",
        "update_interval": 15,
        "orientation": 0,
        "info_section": true,
        "info_section_height": 30,
        "border_around_modules": false,
        "calibration_hours": [
            2,
            6,
            12
        ],
        "modules": [
            {
                "position": 1,
                "name": "Inkyimage",
                "config": {
                    "size": [
                        825,
                        1170
                    ],
                    "path": "/home/pi/screenshots/image.png",
                    "palette": "bw",
                    "autoflip": true,
                    "orientation": "vertical",
                    "padding_x": 10,
                    "padding_y": 10,
                    "fontsize": 12,
                    "language": "en"
                }
            }
        ]
    }
    ```

3. Carefully follow Inkycal's instructions on step `6.`.  
   This step mentions that `If you have the 12.48" display, these steps are also required:`, but this also applies to our 9.7" screen:  
   Use the following commands to install the BCM2835 library on the Raspberry Pi. Load the terminal on the Raspberry Pi via SSH and type the following commands:

    ``` bash
    wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.xx.tar.gz
    tar zxvf bcm2835-1.xx.tar.gz
    cd bcm2835-1.xx/
    sudo ./configure
    sudo make
    sudo make check
    sudo make install
    ```

    * Replace `1.xx` with the version number of the library that you downloaded. `1.73` at the time of writing.
    * `./configure`: This command runs a script that checks the system for any necessary dependencies and configures the library for the system.
    * `make`: This command compiles the library.
    * `sudo make check`: This command runs a set of tests to ensure that the library was compiled correctly.
    * `sudo make install`: This command installs the library on the system.
  
    Next, install `WiringPi`:

    ``` bash
    wget https://project-downloads.drogon.net/wiringpi-latest.deb
    sudo dpkg -i wiringpi-latest.deb
    ```

4. Next, follow the instructions in the "[Manual installation](https://github.com/aceinnolab/Inkycal#manual-installation)" section.

!!! Tip
    This is where you might encounter issues. Specifically, you might encounter issues while installing `numpy` and `matplotlib` while running the `pip install -e ./` command. If you do, follow the instructions in the [Troubleshooting](#troubleshooting) section.

!!! Danger
    If you were able to successfully install Ikycal we strongly advise against running it just yet! The default settings have a VCOM hardcoded to 2.00 which might be too high for your e-ink display and might cause ghosting in the long term. We will fix this in the next steps.

## Step 5 - Modifying Inkycal's files

You are almost there! Once you have successfully installed Inkycal, you need to modify some of its files to make sure it works correctly with your e-ink display.

1. Adapt the VCOM value being passed to the e-ink display which might in its original value might cause ghosting in the long run.
2. Fix the hardcoded `.convert('1', dither=dither)` value that forces the image to be converted to bilevel (black and white only), using dither to simulate grayscale.

### Step 5.1: Adapting the VCOM

The official WaveShare documentation is very clear about this:

!!! quote
    The VCOM value of each E-paper has certain differences. The VCOM value of each E-paper is marked on the FPC cable, so make sure the correct VCOM value is used in each execution of the demo, otherwise, the display will become worse if the E-paper works under the wrong VCOM value for a long time[^3].

[^3]: Source: [WaveShare's Wiki](https://www.waveshare.com/wiki/7.8inch_e-Paper_HAT)

What WaveShare means is that if the e-ink display runs using the wrong VCOM for an extended period of time, it will burn in; the screen will not be able to refresh itself properly and you will experience irreversible ghosting.

The drivers used by Inkycal use a default hardcoded value. In the case of the 9.7" inch driver, it is set to `2.00`.

Check the VCOM value on the FPC of your e-ink display. The FPC is the orange cable at the bottom of your display. The VCOM value is printed on the FPC in rather small letters and starts with a `-` (minus). On newer models it is printed on top of a QR code. In our case the value visible was `-1.81`

On your Raspberry Pi, navigate to your display's driver. In this case we will edit the 9.7" driver in `/home/pi/Inkycal/inkycal/display/drivers/9_in_7.py`. Find the `VCOM = "2.00`. Replace `2.00` with the VCOM value of your display. In our case: `1.81`. Note that it is not necessary to add the minus `-`; it is added later in the same script.

Save the edited script.

### Step 5.2: Saving the image in the right format for the display

Inkycal's `main.py` describes the attributes of the `main` class with the following statement:

``` python
"""
Attributes:
  - optimize = True/False. Reduce number of colours on the generated image
    to improve rendering on E-Papers. Set this to False for 9.7" E-Paper.
"""
```

Yet, in the same file, we see that in TODO: ADD EXACT LINE, we see a hardcoded variable:

``` python
# Option to use epaper image optimisation, reduces colours
self.optimize = True
```

This will *always* reduce the quality of the images before sending them to the e-ink display.  
Switch the statement to `False` to fix this:

``` python
self.optimize = False
```

Next, it is crucial that you edit the Inkcal "Image" module at `/home/pi/Inkycal/inkycal/modules/inky_image.py`. In this file, find the following line of code:

``` python
im_black = image.convert('1', dither=dither)
```

This means that the the script will always attempt to convert the image to a bilinear black and white image. There will be no grayscale, rather the shades of gray will be emulated using dither: a technique that uses a pattern of dots to simulate shades of gray.

Change this value to:

``` python
im_black = image.convert('RGB')
```

For more information about the different image modes, check [Pillow's documentation](https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes).

## Step 6 - Import your screenshot to the Raspberry Pi and autostarting

1. Using your favorite SFTP client, connect to your Raspberry Pi, using the same credentials used for the SSH connection, and navigate to the `/home/pi/screenshots` folder.
2. Upload the `fetch_image.py` in the `raspberry_pi/screenshots` folder of this repository to the `/home/pi/screenshots` folder on your Raspberry Pi.
3. Run the script.

You should see a new `image.png` file in the `/home/pi/screenshots` folder!

!!! Important
    You must make sure that this script runs when you start your Raspberry Pi, and that it runs regularl using [Cron](hhttps://www.raspberrypi.com/documentation/computers/camera_software.html#automating-using-cron-jobs) and the command ```sudo crontab -e```.
    For example:

    ``` bash
    */3 * * * * python3 /home/pi/screenshots/fetch_image.py
    @reboot python3 /home/pi/screenshots/fetch_image.py
    ```

## Troubleshooting

### Inkycal get stuck while installing, or the installation seems to take hours

This is a known issue. You can find more information about it [here](https://github.com/aceinnolab/Inkycal/issues/262). We solved it like this:

1. Increase the swapfile size on your Raspberry Pi: SSH to your Raspberry Pi and run the following commands, line by line. This will increase the swapfile size to 256MB.

    ``` bash
    sudo dphys-swapfile swapoff
    sudo nano /etc/dphys-swapfile
    sudo sed -i -E '/^CONF_SWAPSIZE=/s/=.*/=256/' /etc/dphys-swapfile
    sudo dphys-swapfile setup
    sudo dphys-swapfile swapon
    ```

2. Reboot your Raspberry Pi.
3. You will notice that the ticket linked above mentions installing `numpy` and `matplotlib` separately and individually. In our case, we were not able to install them because of missing BLAS libraries. We solved this by installing the following package:

    ``` bash
    cd ~/Inkycal && source venv/bin/activate
    sudo apt install libopenblas-dev
    pip install --upgrade --verbose --no-cache-dir numpy
    pip install --upgrade --verbose --no-cache-dir matplotlib
    pip install -e --verbose ./
    ```

    These installation can take a long time (30+ minutes) and might seem stuck. That is why we added the `--verbose` flag to the `pip install` commands: this will show you the progress of the installation.
