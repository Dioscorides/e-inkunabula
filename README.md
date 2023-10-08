# e-Inkunabula

<p align="center">
    <a href="https://github.com/Dioscorides/e-inkunabula" target="_blank">
        <img width="70%" src="img/../docs/img/e-inkunabula-logo.svg" alt="e-Inkunabula logo">
    </a>
</p>

<br/>
<p align="center">
    <a href="LICENSE" target="_blank">
        <img src="https://img.shields.io/github/license/Dioscorides/e-Inkunabula.svg" alt="GitHub license">
    </a>
    <a href="https://github.com/Dioscorides/e-Inkunabula/releases" target="_blank">
        <img src="https://img.shields.io/github/tag/Dioscorides/e-Inkunabula.svg" alt="GitHub tag (latest SemVer)">
    </a>
    </a>
    <a href="https://github.com/Dioscorides/e-Inkunabula/commits" target="_blank">
        <img src="https://img.shields.io/github/commit-activity/y/Dioscorides/e-Inkunabula.svg" alt="GitHub commit activity">
    </a>
    <a href="https://github.com/Dioscorides/e-Inkunabula/graphs/contributors" target="_blank">
        <img src="https://img.shields.io/github/contributors-anon/Dioscorides/e-Inkunabula.svg" alt="GitHub contributors">
    </a>
</p>

[e-Inkunabula](https://github.com/Dioscorides/e-inkunabula) is a project that aims to help you display information coming from [Home Assistant](https://www.home-assistant.io/) on an e-ink display using a Raspberry Pi.

**This repository contains a step-by-step guide on how to setup your Raspberry Pi, modified files from [Inkycal v.2.0.2](https://github.com/aceinnolab/Inkycal/releases/tag/v2.0.2), and WaveShare 9.7" e-ink display.**

## 🚀&nbsp; Installation and Documentation

Ready? Check the **[e-Inkunabula documentation](<https://dioscorides.github.io/e-inkunabula>)** to get started!

---

## 🤝&nbsp; Found a bug? Missing a specific feature?

e-Inkunabula is not perfect! We welcome your contributions to make it better. If you find an issue, please file it in [our GitHub issue tracker](https://github.com/Dioscorides/e-Inkunabula/issues). Make sure to include as much information as you can in your bug report by following the [bug report template](https://github.com/Dioscorides/e-inkunabula/issues/new/choose). If you already found a solution to your problem, **we would love to review your [pull request](https://github.com/Dioscorides/e-inkunabula/pulls)!**

## ✅&nbsp; Requirements

You may use any Raspberry Pi or WaveShare e-ink display and apply the logic described in our documentation, but to follow this guide exactly you will need the following:

### 🖥️&nbsp; Hardware

* Raspberry Pi 3 v1.2
* 16GB microSD card
* WaveShare 9.7" e-ink display
* WaveShare e-ink display driver board (IT8951)
* 5V 2A power supply
* Synology DS218+ NAS (or any Synology NAS that supports Docker)

### 📝&nbsp; Software

* Python 3.7
* BCM2835 library
* WaveShare IT8951 library
* Docker (running on Synology DS218+)
* [Home Assistant](https://www.home-assistant.io/) (via Docker, running on Synology DS218+)
* [Home Assistant Lovelace Kindle Screensaver](https://github.com/sibbl/hass-lovelace-kindle-screensaver) (via Docker, running on Synology DS218+)
* [Inkycal v.2.0.2](https://github.com/aceinnolab/Inkycal/releases/tag/v2.0.2)
* [Portainer](https://www.portainer.io/) (Optional - via Docker, running on Synology DS218+. You can create a stack using the Synology interface directly.)

## 📘&nbsp; License

The e-Inkunabula is released under the under terms of the [GNU GENERAL PUBLIC LICENSE](LICENSE).
