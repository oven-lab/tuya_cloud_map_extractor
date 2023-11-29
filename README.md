# Tuya cloud vaccum map extractor
This integration extracts and exposes live maps from tuya laser vaccums into Home Assistant.

## Disclaimer
This is my first Home Assistant integration, so if things go terribly wrong, please create an issue so i can learn from and fix it.

## Installation


### Using HACS
This integration is not yet in HACS default repository, but can be manually installed via HACS.
Add this repository as a custom repository in HACS, and install as normal.


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

## Supported devices
Following is a list of currently supported devices (confirmed tested by individual users): 

* Elvita CRD4550S [Product Website - SE](https://elvita.se/produkter/rengoring/robotdammsugare/elvita-robotdammsugare-crd4550s)
* Neatsvor x600 pro [Product Website - EN](https://neatsvor.com/products/neatsvor-x600-pro)
* Lubluelu SL60D [Product Website - EN](https://lubluelu.com/products/sl60d-poweful-breakpoint-mode-wifi-connected)
* Zedar R-600 [Product Website - DE](https://zedar.eu)
* Liectroux xr-500 [Product Website - EN](https://liectrouxrobotics.com/products/liectroux-xr500-high-end-robot-vacuum-laser-navigation-6500pa-suction-power-save-5-maps-in-the-app-y-shape-wet-mopping-virtual-wall-setting-have-stock-in-eu-warehouse)

Feel free to test on your own devices, and add them here. For help, please create an issue!

## Special thanks
This integration is largely based on [Xiaomi Cloud Map Extractor](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Xiaomi-Cloud-Map-Extractor). Thanks!
