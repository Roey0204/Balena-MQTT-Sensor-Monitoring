#!/usr/bin/env python3
"""
Example MQTT Subscriber
Subscribe to GPIO sensor data from your Balena device

Usage:
    python3 mqtt_subscriber.py

Requirements:
    pip install paho-mqtt
"""

import json
import paho.mqtt.client as mqtt
from datetime import datetime


MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "balena/gpio/sensor"


def on_connect(client, userdata, flags, rc):
    """Callback when connected to MQTT broker"""
    if rc == 0:
        print(f"✓ Connected to MQTT broker: {MQTT_BROKER}")
        print(f"✓ Subscribing to topic: {MQTT_TOPIC}")
        client.subscribe(MQTT_TOPIC)
        print("\nWaiting for messages... (Press Ctrl+C to exit)\n")
    else:
        print(f"✗ Connection failed with code {rc}")


def on_message(client, userdata, msg):
    """Callback when message is received"""
    try:
        payload = json.loads(msg.payload.decode())
        
        timestamp = payload.get('timestamp', 'N/A')
        device_id = payload.get('device_id', 'unknown')
        sensors = payload.get('sensors', {})
        
        gpio_pin = sensors.get('gpio_pin', 'N/A')
        state = sensors.get('state', 'N/A')
        state_label = sensors.get('state_label', 'N/A')
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Message received:")
        print(f"  Device ID:   {device_id}")
        print(f"  Timestamp:   {timestamp}")
        print(f"  GPIO Pin:    {gpio_pin}")
        print(f"  State:       {state} ({state_label})")
        print(f"  Raw JSON:    {json.dumps(payload, indent=2)}")
        print("-" * 60)
        
    except json.JSONDecodeError:
        print(f"✗ Invalid JSON received: {msg.payload.decode()}")
    except Exception as e:
        print(f"✗ Error processing message: {e}")


def on_disconnect(client, userdata, rc):
    """Callback when disconnected from broker"""
    if rc != 0:
        print(f"\n✗ Unexpected disconnection (code {rc})")


def main():
    """Main subscriber function"""
    print("=" * 60)
    print("  MQTT GPIO Sensor Subscriber")
    print("=" * 60)
    
    client = mqtt.Client(client_id="gpio_subscriber")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    try:
        print(f"\nConnecting to {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        client.loop_forever()
        
    except KeyboardInterrupt:
        print("\n\n✓ Shutting down gracefully...")
        client.disconnect()
        
    except Exception as e:
        print(f"\n✗ Error: {e}")


if __name__ == '__main__':
    main()
