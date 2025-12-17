# ⚠️🔴 **This integration has stopped receiving updates** 🔴⚠️

**Important notice:** This custom integration is no longer maintained and will not receive any further updates, bug fixes, or new features.
The Tuya vacuum protocol is not standardized across manufacturers. While Tuya provides a common cloud platform, each robot vacuum brand (or even different models from the same brand) implements its own proprietary variations of the protocol, including custom message formats, encryption methods, map data structures, and command sets.

This integration was developed primarily through reverse engineering and currently works with the devices listed further down in the readme.

However, compatibility with other Tuya-based vacuums is limited and often inconsistent. Adding support for new models typically requires extensive reverse engineering, decoding binary map data, and handling manufacturer-specific quirks—for each individual device or firmware version.

Given the tremendous amount of work required to support additional devices, and the lack of official documentation or a unified protocol from Tuya, I have decided to discontinue active development and maintenance of this project.

### What this means for users
- The integration will continue to function as-is for supported devices, as long as the Tuya cloud API remains compatible.
- No guarantees are made about long-term functionality, especially if Tuya changes their cloud services or manufacturers update firmware.
- If your device currently works, you may wish to avoid updating the vacuum's firmware when possible.
- For future needs, consider exploring alternatives such as:
  - Regular controls through localtuya and tuya integrations.
  - Manufacturer-specific integrations if available

Thanks to everyone that has been participant in the development of this project, even if it didn't work out like i planned.

# Tuya cloud vaccum map extractor
This integration extracts and exposes live maps from tuya laser vaccums into Home Assistant.

## Disclaimer
This is my first Home Assistant integration, so if things go terribly wrong, please create an issue so i can learn from and fix it.

## Installation


### Using HACS
This integration is included in the HACS default repository. Just search for Tuya cloud map extractor and install!


### Manually 
To install this integration, manually add the contents of custom_components to your home assistant custom_components folder, and reboot.

## Configuration


### Prerequisites
* A vacuum with Lidar support already added to the Tuya/Smart app.
* A configured Tuya IoT development platform, including the following components:
    - A cloud project and linked device. (Need help? See the [Tuya integration](https://www.home-assistant.io/integrations/tuya/#configuration-of-the-tuya-iot-platform).)
    - The Tuya Sweeping Robot Open API added to the cloud platform (Main Menu -> Cloud -> Development - Service API and make sure to have Sweeping Robot Open Service added to the list of authorized services or the integration will not install and will return an "unknown" error).

### Configuration in Home Assistant
After the installation of this integration into Home Assistant, the integration is configured via config flow. Add a new integration via the UI and choose "Tuya Vacuum Map Extractor". Then enter your Tuya IoT platform credentials.

### Turn on and turn off
By default, the vacuum map camera is turned off. You have to manually call the service camera.turn_on and camera.turn_off. I would recommend [this](https://raw.githubusercontent.com/PiotrMachowski/Home-Assistant-custom-components-Xiaomi-Cloud-Map-Extractor/master/blueprints/automation/disable_vacuum_camera_update_when_docked.yaml) blueprint to automatically turn on and off camera updates depending on if the vacuum is docked or not.

## Supported devices
Following is a list of currently supported devices (confirmed tested by individual users): 

* Elvita CRD4550S [Product Website - SE](https://elvita.se/produkter/rengoring/robotdammsugare/elvita-robotdammsugare-crd4550s)
* Neatsvor x600 pro [Product Website - EN](https://neatsvor.com/products/neatsvor-x600-pro)
* Lubluelu SL60D [Product Website - EN](https://lubluelu.com/products/sl60d-poweful-breakpoint-mode-wifi-connected)
* Zedar R-600 [Product Website - DE](https://zedar.eu)
* Liectroux xr-500 [Product Website - EN](https://liectrouxrobotics.com/products/liectroux-xr500-high-end-robot-vacuum-laser-navigation-6500pa-suction-power-save-5-maps-in-the-app-y-shape-wet-mopping-virtual-wall-setting-have-stock-in-eu-warehouse)
* Honiture Q6 Lite [Product Website - EN](https://www.honiture.com/product/honiture-q6-mapping-robot-vacuum-with-xl-self-empty-base-2-in-1-of-vacuuming-and-mopping-2700pa-super-suction-with-tangle-free-ideal-for-pet-hair-hard-floor-and-carpet-2)

Feel free to test on your own devices, and add them here. For help, please create an issue!

## Special thanks
This integration is largely based on [Xiaomi Cloud Map Extractor](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Xiaomi-Cloud-Map-Extractor). Thanks!
