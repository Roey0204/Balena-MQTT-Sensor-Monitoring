# Quick Start Guide

Get your GPIO sensor monitoring up and running in 5 minutes!

## Prerequisites

- Raspberry Pi (any model with GPIO)
- Balena account ([sign up free](https://dashboard.balena-cloud.com/signup))
- Balena CLI installed ([installation guide](https://github.com/balena-io/balena-cli/blob/master/INSTALL.md))
- A sensor connected to GPIO pin 14

## Step 1: Hardware Setup

Connect your sensor to the Raspberry Pi:

```
Sensor → GPIO Pin 14 (Physical pin 8)
Sensor GND → GND (Physical pin 6)
Sensor VCC → 3.3V (Physical pin 1) or 5V (Physical pin 2)
```

**Simple test with a button:**
- Connect one side of button to GPIO 14
- Connect other side to GND
- No external resistor needed (uses internal pull-down)

## Step 2: Create Balena Application

```bash
# Login to Balena
balena login

# Create new application
balena app create MyGPIOSensor --type raspberrypi4-64

# Add your device
# Follow instructions at: https://dashboard.balena-cloud.com
# Download OS image, flash to SD card, boot your Pi
```

## Step 3: Deploy Application

```bash
# Clone or navigate to this repository
cd Balena-MQTT-Sensor-Monitoring

# Push to Balena
balena push MyGPIOSensor
```

Wait 5-10 minutes for the build and deployment to complete.

## Step 4: Monitor Your Data

### Option A: Command Line (Recommended for testing)

```bash
# Install mosquitto clients
# Ubuntu/Debian: sudo apt-get install mosquitto-clients
# macOS: brew install mosquitto
# Windows: Download from https://mosquitto.org/download/

# Subscribe to your sensor data
mosquitto_sub -h broker.hivemq.com -t "balena/gpio/sensor" -v
```

### Option B: Python Script

```bash
# Install dependencies
pip install paho-mqtt

# Run the example subscriber
python3 examples/mqtt_subscriber.py
```

### Option C: MQTT Explorer (GUI)

1. Download [MQTT Explorer](http://mqtt-explorer.com/)
2. Connect to `broker.hivemq.com` port `1883`
3. Subscribe to topic `balena/gpio/sensor`

## Step 5: Test Your Sensor

- **Button:** Press and release - you should see state change from 0 (LOW) to 1 (HIGH)
- **Motion sensor:** Move in front of sensor - state changes to 1 when motion detected
- **Any digital sensor:** State will be 0 or 1 based on sensor output

## Expected Output

```json
{
  "timestamp": "2026-03-11T15:30:00.000000",
  "device_id": "abc123...",
  "sensors": {
    "gpio_pin": 14,
    "state": 1,
    "state_label": "HIGH"
  }
}
```

## Customization

### Change GPIO Pin

In Balena dashboard → Device Variables:
```
GPIO_PIN = 17
```

### Change Update Interval

```
SENSOR_INTERVAL = 2  # Update every 2 seconds
```

### Use Private MQTT Broker

```
MQTT_BROKER = your-broker.com
MQTT_PORT = 1883
```

## Troubleshooting

### No data appearing?

1. **Check device is online:** Balena dashboard → Devices
2. **View logs:** Click on device → Logs tab
3. **Verify GPIO connection:** Use multimeter or LED to test pin 14
4. **Test MQTT broker:** `ping broker.hivemq.com`

### GPIO permission errors?

The container needs `privileged: true` which is already set in `docker-compose.yml`.

### Wrong pin numbering?

This project uses **BCM numbering** (GPIO 14), not physical pin numbers.

## Next Steps

- **Secure your data:** Set up a private MQTT broker with authentication
- **Add more sensors:** Read multiple GPIO pins simultaneously
- **Create dashboards:** Use Node-RED, Grafana, or Home Assistant
- **Add alerts:** Trigger notifications when sensor state changes
- **Store data:** Connect to InfluxDB or other time-series database

## Support

- [Balena Forums](https://forums.balena.io/)
- [Project README](README.md)
- [Balena Documentation](https://www.balena.io/docs/)

## Example Use Cases

- **Door/Window sensors:** Monitor when doors open/close
- **Motion detection:** Security and automation
- **Water leak detection:** Get alerts when water detected
- **Temperature alerts:** Digital temperature sensor threshold
- **Button controls:** Remote control and triggers
- **Industrial sensors:** Monitor equipment status
