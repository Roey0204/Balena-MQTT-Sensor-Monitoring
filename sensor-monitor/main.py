#!/usr/bin/env python3
"""
Balena MQTT Sensor Monitoring Application
Monitors system sensors and publishes data to MQTT broker
"""

import os
import time
import json
import logging
from datetime import datetime
from sensor_module import SensorReader
from mqtt_client import MQTTClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SensorMonitor:
    """Main application class for sensor monitoring"""
    
    def __init__(self):
        self.mqtt_broker = os.getenv('MQTT_BROKER', 'broker.hivemq.com')
        self.mqtt_port = int(os.getenv('MQTT_PORT', 1883))
        self.mqtt_topic = os.getenv('MQTT_TOPIC', 'balena/gpio/sensor')
        self.sensor_interval = int(os.getenv('SENSOR_INTERVAL', 5))
        self.gpio_pin = int(os.getenv('GPIO_PIN', 14))
        
        self.mqtt_client = MQTTClient(
            broker=self.mqtt_broker,
            port=self.mqtt_port
        )
        self.sensor_reader = SensorReader(gpio_pin=self.gpio_pin)
        
        logger.info(f"Initialized SensorMonitor")
        logger.info(f"MQTT Broker: {self.mqtt_broker}:{self.mqtt_port}")
        logger.info(f"MQTT Topic: {self.mqtt_topic}")
        logger.info(f"GPIO Pin: {self.gpio_pin}")
        logger.info(f"Sensor Interval: {self.sensor_interval}s")
    
    def run(self):
        """Main monitoring loop"""
        logger.info("Starting sensor monitoring...")
        
        if not self.mqtt_client.connect():
            logger.error("Failed to connect to MQTT broker")
            return
        
        try:
            while True:
                sensor_data = self.sensor_reader.read_all_sensors()
                
                payload = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'device_id': os.getenv('BALENA_DEVICE_UUID', 'unknown'),
                    'sensors': sensor_data
                }
                
                if self.mqtt_client.publish(self.mqtt_topic, payload):
                    logger.info(f"Published sensor data: {json.dumps(payload, indent=2)}")
                else:
                    logger.warning("Failed to publish sensor data")
                
                time.sleep(self.sensor_interval)
                
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}", exc_info=True)
        finally:
            self.sensor_reader.cleanup()
            self.mqtt_client.disconnect()


if __name__ == '__main__':
    monitor = SensorMonitor()
    monitor.run()
