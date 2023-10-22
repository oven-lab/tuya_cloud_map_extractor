# Tuya cloud vaccum map extractor
This intergraion extracts and exposes live maps from tuya laser vaccums into Home Assistant.

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

* A laser vacuum added to the Tuya Smart app.
* A configured Tuya IoT development platform, with a cloud project and linked device. (Need help? See the [Tuya integration](https://www.home-assistant.io/integrations/tuya/#configuration-of-the-tuya-iot-platform).)

### Configuration in Home Assistant
After the installation of this integration into Home Assistant, the integration is configured via config flow. Add a new integration via the UI and choose "Tuya Vacuum Map Extractor". Then enter your Tuya IoT platform credentials.

## Supported devices

This integraion was developed solely for my own use, so the only known supported device is:
* Elvita CRD4550S

Feel free to test on your own devices, and add them here. If you need any help, create an issue!

## Special thanks
This integraion is largely based on [Xiaomi Cloud Map Extractor](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Xiaomi-Cloud-Map-Extractor). Thanks!
