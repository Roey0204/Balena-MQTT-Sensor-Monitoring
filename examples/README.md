# MQTT Subscriber Examples

This folder contains example scripts for subscribing to GPIO sensor data published by your Balena device.

## Python Subscriber

### Installation

```bash
pip install paho-mqtt
```

### Usage

```bash
python3 mqtt_subscriber.py
```

### Customize

Edit the script to change broker or topic:

```python
MQTT_BROKER = "broker.hivemq.com"  # Change to your broker
MQTT_PORT = 1883
MQTT_TOPIC = "balena/gpio/sensor"   # Change to your topic
```

## Node.js Subscriber

### Installation

```bash
npm install mqtt
```

### Usage

```javascript
const mqtt = require('mqtt');

const client = mqtt.connect('mqtt://broker.hivemq.com');

client.on('connect', () => {
  console.log('Connected to MQTT broker');
  client.subscribe('balena/gpio/sensor');
});

client.on('message', (topic, message) => {
  const data = JSON.parse(message.toString());
  console.log('Received:', data);
});
```

## MQTT Explorer (GUI)

1. Download from [http://mqtt-explorer.com/](http://mqtt-explorer.com/)
2. Connect to `broker.hivemq.com:1883`
3. Subscribe to `balena/gpio/sensor`

## Node-RED

Add these nodes to your flow:

1. **MQTT In** node:
   - Server: `broker.hivemq.com:1883`
   - Topic: `balena/gpio/sensor`

2. **JSON** node: Parse the message

3. **Debug** node: Display the data

## Testing

To test without a Raspberry Pi, the sensor module includes a simulation mode that generates random GPIO states when RPi.GPIO is not available.
