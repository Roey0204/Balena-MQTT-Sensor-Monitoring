# Balena MQTT GPIO Sensor Monitor

A complete Balena application template for reading GPIO pin 14 on Raspberry Pi and publishing sensor data to a public MQTT broker. This boilerplate provides a production-ready setup for IoT sensor monitoring projects.

## Features

- 📍 **GPIO Pin 14 Reading** on Raspberry Pi
- 📡 **Public MQTT Broker** (HiveMQ) - accessible from anywhere
- 🐍 **Python-based monitoring** with RPi.GPIO
- 🔄 **Auto-reconnect** and error handling
- ⚙️ **Environment-based configuration**
- 📝 **Comprehensive logging**
- 🎯 **Plug-and-play** - works out of the box

## Architecture

```
┌─────────────────────────────────────────┐
│      Raspberry Pi (Balena Device)       │
│                                         │
│  ┌────────────────────────────────┐    │
│  │   Sensor Monitor (Python)      │    │
│  │   - Reads GPIO Pin 14          │    │
│  │   - Publishes to MQTT          │    │
│  └───────────────┬────────────────┘    │
└──────────────────┼──────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │  Public MQTT Broker │
         │  (broker.hivemq.com)│
         └─────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │  Your MQTT Clients  │
         │  (Subscribe/Monitor)│
         └─────────────────────┘
```

## Services

### Sensor Monitor (sensor-monitor)
- Python-based GPIO monitoring service
- Reads GPIO pin 14 state (HIGH/LOW)
- Publishes data to public MQTT broker
- Configurable GPIO pin and interval
- Automatic GPIO cleanup on shutdown

## Quick Start

### Prerequisites
- [Balena CLI](https://github.com/balena-io/balena-cli) installed
- Balena account and application created
- Device provisioned and connected

### Deploy to Balena

1. **Clone this repository:**
   ```bash
   git clone <your-repo-url>
   cd Balena-MQTT-Sensor-Monitoring
   ```

2. **Login to Balena:**
   ```bash
   balena login
   ```

3. **Push to your Balena application:**
   ```bash
   balena push <your-app-name>
   ```

### Local Development

1. **Test locally with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f sensor-monitor
   ```

## Configuration

### Environment Variables

Configure the application using these environment variables in the Balena dashboard or `docker-compose.yml`:

| Variable | Default | Description |
|----------|---------|-------------|
| `MQTT_BROKER` | `broker.hivemq.com` | Public MQTT broker hostname |
| `MQTT_PORT` | `1883` | MQTT broker port |
| `MQTT_TOPIC` | `balena/gpio/sensor` | MQTT topic for sensor data |
| `SENSOR_INTERVAL` | `5` | Sensor reading interval (seconds) |
| `GPIO_PIN` | `14` | GPIO pin number to read (BCM numbering) |

### Available Public MQTT Brokers

You can use any of these free public MQTT brokers:

| Broker | Hostname | Port | Notes |
|--------|----------|------|-------|
| **HiveMQ** | `broker.hivemq.com` | 1883 | Default, reliable |
| **Eclipse** | `mqtt.eclipseprojects.io` | 1883 | Open source project |
| **Mosquitto** | `test.mosquitto.org` | 1883 | Test broker |
| **EMQX** | `broker.emqx.io` | 1883 | High performance |

**Note:** Public brokers are not secure and should only be used for testing. For production, use a private broker with authentication.

### Setting Variables in Balena Dashboard

1. Go to your application in the Balena dashboard
2. Navigate to **Device Variables** or **Fleet Variables**
3. Add the variables you want to customize

## Hardware Setup

### Wiring GPIO Pin 14

Connect your sensor to GPIO pin 14 on the Raspberry Pi:

```
Raspberry Pi GPIO Layout (BCM numbering):
┌─────────────────────────────┐
│  3V3  (1) (2)  5V           │
│  GPIO2 (3) (4)  5V          │
│  GPIO3 (5) (6)  GND         │
│  GPIO4 (7) (8)  GPIO14 ◄──  │  Connect your sensor here
│  GND   (9) (10) GPIO15      │
│  ...                        │
└─────────────────────────────┘
```

**Example connections:**
- **Digital sensor:** Connect sensor output to GPIO 14, sensor GND to Pi GND, sensor VCC to Pi 3.3V
- **Button/Switch:** Connect one side to GPIO 14, other side to GND (uses internal pull-down resistor)
- **Motion sensor (PIR):** Connect OUT to GPIO 14, GND to Pi GND, VCC to Pi 5V

## Project Structure

```
Balena-MQTT-Sensor-Monitoring/
├── docker-compose.yml           # Container orchestration
├── balena.yml                   # Balena application configuration
├── README.md                    # This file
└── sensor-monitor/              # Python GPIO monitoring service
    ├── Dockerfile.template      # Balena-optimized Dockerfile
    ├── requirements.txt         # Python dependencies (RPi.GPIO, paho-mqtt)
    ├── main.py                  # Main application entry point
    ├── sensor_module.py         # GPIO reading module
    └── mqtt_client.py           # MQTT client module
```

## Python Modules

### sensor_module.py
Handles reading GPIO pin 14:
- Reads digital state (HIGH/LOW)
- BCM pin numbering mode
- Automatic GPIO cleanup
- Simulation mode for testing without hardware

### mqtt_client.py
Manages MQTT communication:
- Connection handling with retry logic
- Message publishing
- Automatic reconnection
- Error handling

### main.py
Main application orchestrator:
- Initializes sensor reader and MQTT client
- Runs monitoring loop
- Publishes sensor data at configured intervals

## Data Format

GPIO sensor data is published in JSON format:

```json
{
  "timestamp": "2026-03-11T10:50:00.000000",
  "device_id": "abc123def456",
  "sensors": {
    "gpio_pin": 14,
    "state": 1,
    "state_label": "HIGH"
  }
}
```

**Field descriptions:**
- `timestamp`: ISO 8601 UTC timestamp
- `device_id`: Balena device UUID
- `gpio_pin`: GPIO pin number being monitored
- `state`: Digital state (0 = LOW, 1 = HIGH, -1 = ERROR)
- `state_label`: Human-readable state (LOW/HIGH/ERROR)

## Monitoring & Debugging

### View Logs in Balena Dashboard
1. Go to your device in the Balena dashboard
2. Click on **Logs** tab
3. Filter by service: `sensor-monitor` or `mqtt-broker`

### Using Balena CLI
```bash
# View all logs
balena logs <device-uuid>

# Follow logs for specific service
balena logs <device-uuid> --service sensor-monitor --tail
```

### Test MQTT Connection

You can subscribe to your sensor data from anywhere using MQTT clients:

**Using mosquitto_sub (command line):**
```bash
# Subscribe to your sensor data
mosquitto_sub -h broker.hivemq.com -t "balena/gpio/sensor" -v
```

**Using MQTT Explorer (GUI):**
1. Download [MQTT Explorer](http://mqtt-explorer.com/)
2. Connect to `broker.hivemq.com:1883`
3. Subscribe to topic `balena/gpio/sensor`

**Using Python:**
```python
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message
client.connect("broker.hivemq.com", 1883)
client.subscribe("balena/gpio/sensor")
client.loop_forever()
```

**Using Node-RED:**
Add an MQTT input node with broker `broker.hivemq.com` and topic `balena/gpio/sensor`

## Customization

### Change GPIO Pin

Set the `GPIO_PIN` environment variable to read from a different pin:

```yaml
environment:
  - GPIO_PIN=17  # Use GPIO 17 instead
```

### Read Multiple GPIO Pins

Edit `sensor-monitor/sensor_module.py` to read multiple pins:

```python
def __init__(self, gpio_pins: list = [14, 15, 17]):
    self.gpio_pins = gpio_pins
    for pin in self.gpio_pins:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_all_sensors(self) -> Dict[str, Any]:
    return {
        f'gpio_{pin}': GPIO.input(pin) 
        for pin in self.gpio_pins
    }
```

### Use Different MQTT Topics

Modify the `MQTT_TOPIC` environment variable or publish to multiple topics:

```python
# Publish to device-specific topic
topic = f"balena/{device_id}/gpio14"
self.mqtt_client.publish(topic, payload)
```

### Add Authentication to MQTT

For private brokers with authentication, modify `mqtt_client.py`:

```python
self.client.username_pw_set(username, password)
```

## Troubleshooting

### GPIO Permission Errors
- Ensure `privileged: true` is set in `docker-compose.yml`
- Check that GPIO devices are mounted: `/dev/gpiomem` and `/dev/mem`
- Verify RPi.GPIO library is installed: check container logs

### MQTT Connection Issues
- Test broker connectivity: `ping broker.hivemq.com`
- Try alternative public brokers (see table above)
- Check firewall settings if using custom broker
- Verify internet connectivity on device

### GPIO Not Reading Correctly
- Check physical wiring connections
- Verify correct GPIO pin number (BCM vs BOARD numbering)
- Test with a simple LED or multimeter
- Check if pull-up/pull-down resistors are needed

### Container Restart Loops
- Check logs: `balena logs <device-uuid> --service sensor-monitor`
- Verify Raspberry Pi is the device type
- Ensure all dependencies are installed
- Check for Python syntax errors in logs

## Contributing

Feel free to fork this repository and customize it for your needs. Pull requests are welcome!

## License

MIT License - feel free to use this boilerplate for your projects.

## Resources

- [Balena Documentation](https://www.balena.io/docs/)
- [Eclipse Mosquitto](https://mosquitto.org/)
- [Paho MQTT Python Client](https://www.eclipse.org/paho/index.php?page=clients/python/index.php)
- [psutil Documentation](https://psutil.readthedocs.io/)

## Support

For issues and questions:
- Check the [Balena Forums](https://forums.balena.io/)
- Review the logs in Balena dashboard
- Open an issue in this repository
