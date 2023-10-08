# Welcome to e-Inkunabula

!!! INFO
    **This project's aim is to create a guide that will help you through the process of setting up your own e-ink display using a Raspberry Pi, a WaveShare 9.7" e-ink display, and Home Assistant.**

``` mermaid
sequenceDiagram
    NAS->>NAS: Generates a screenshot<br/>of the Home Assistant view
    Raspberry Pi-->>NAS: Screenshot requested<br/>by the Raspberry Pi
    NAS->>Raspberry Pi: Screenshot imported<br/> by the Raspberry Pi
    InkyCal-->>Raspberry Pi: Image requested<br/>by InkyCal
    Raspberry Pi->>InkyCal: Screenshot imported<br/> to InkyCal
    InkyCal->>InkyCal: Screenshot converted<br/>to a displayable image by InkyCal
    InkyCal-)WaveShare 9.7" E-Ink Display: Image sent<br/>to the e-ink display

```

Want to skip the preamble? 
[Let's get started with the installation! :rocket:](installation.md){ .md-button .md-button--primary}
---

---

## Concept

E-ink displays are a great way to display information: they are easy on the eyes, and they only use power when the display is updated. This makes them perfect for displaying information that does not change often, such as the weather forecast, the current time, or the current date, or any other information that you would like to display coming from Home Assistant.

Yet, buying an e-ink screen, connecting it to a Raspberry Pi, and displaying information from Home Assistant on it is not as easy as it sounds: There are many different e-ink screens available, and they all have their own quirks. Some e-ink displays are touchscreens, some are not; some e-ink displays are connected to the Raspberry Pi using the 40-pin GPIO header, some are connected using the SPI interface; some e-ink displays are compatible with the WaveShare ESP32 driver board, some are not, and the list goes on.

**This projects aims to help you through the process of setting up your own e-ink display using a Raspberry Pi, a WaveShare 9.7" e-ink display, and Home Assistant in the simplest way we could find.**

!!! Warning
    **This project is meant for e-ink displays that can display HD images at 16bit Grayscale**, such as the WaveShare 9.7" e-ink display. If you are using a e-ink display that can only display images at 8bit grayscale or less, such as the WaveShare 7.5" e-ink display, you should follow the guide offered by [InkyCal](https://github.com/aceinnolab/Inkycal) instead.

## Logic

e-Inkunabula's logic is the following:

1. [Home Assistant Lovelace Kindle Screensaver](https://github.com/sibbl/hass-lovelace-kindle-screensaver) will take a screenshot of "kiosked" Home Assistant view.
2. A python script on the Raspberry Pi will fetch the latest screenshot from the Synology NAS.
3. [InkyCal](https://github.com/aceinnolab/Inkycal) will process and send the image to the e-ink display.

This documentation will help you through the process in detail and guide you through the process of setting up your own e-ink display!

## Project's name

This project's name - *e-Inkunabula* - is a play on the words "e-ink" and "incunabula": *Incunabula* are books printed using metal type from before 1501, and *e-ink* is the technology used for the display used in this project.
