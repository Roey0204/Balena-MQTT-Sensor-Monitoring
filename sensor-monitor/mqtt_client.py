#!/usr/bin/env python3
"""
MQTT Client Module for publishing sensor data
"""

import json
import logging
import paho.mqtt.client as mqtt
from typing import Dict, Any

logger = logging.getLogger(__name__)


class MQTTClient:
    """MQTT Client for publishing sensor data"""
    
    def __init__(self, broker: str, port: int = 1883, client_id: str = None):
        self.broker = broker
        self.port = port
        self.client_id = client_id or "sensor-monitor"
        self.client = mqtt.Client(client_id=self.client_id)
        
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish
        
        self.connected = False
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback for when client connects to broker"""
        if rc == 0:
            logger.info(f"Connected to MQTT broker at {self.broker}:{self.port}")
            self.connected = True
        else:
            logger.error(f"Failed to connect to MQTT broker. Return code: {rc}")
            self.connected = False
    
    def _on_disconnect(self, client, userdata, rc):
        """Callback for when client disconnects from broker"""
        logger.warning(f"Disconnected from MQTT broker. Return code: {rc}")
        self.connected = False
    
    def _on_publish(self, client, userdata, mid):
        """Callback for when message is published"""
        logger.debug(f"Message published with mid: {mid}")
    
    def connect(self, retry_attempts: int = 5, retry_delay: int = 5) -> bool:
        """Connect to MQTT broker with retry logic"""
        import time
        
        for attempt in range(retry_attempts):
            try:
                logger.info(f"Connecting to MQTT broker (attempt {attempt + 1}/{retry_attempts})...")
                self.client.connect(self.broker, self.port, keepalive=60)
                self.client.loop_start()
                
                timeout = 10
                elapsed = 0
                while not self.connected and elapsed < timeout:
                    time.sleep(0.5)
                    elapsed += 0.5
                
                if self.connected:
                    return True
                else:
                    logger.warning(f"Connection timeout on attempt {attempt + 1}")
                    
            except Exception as e:
                logger.error(f"Connection error on attempt {attempt + 1}: {e}")
            
            if attempt < retry_attempts - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
        
        return False
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        try:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("Disconnected from MQTT broker")
        except Exception as e:
            logger.error(f"Error disconnecting: {e}")
    
    def publish(self, topic: str, payload: Dict[str, Any], qos: int = 1) -> bool:
        """Publish message to MQTT topic"""
        if not self.connected:
            logger.error("Not connected to MQTT broker")
            return False
        
        try:
            json_payload = json.dumps(payload)
            result = self.client.publish(topic, json_payload, qos=qos)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                return True
            else:
                logger.error(f"Publish failed with return code: {result.rc}")
                return False
                
        except Exception as e:
            logger.error(f"Error publishing message: {e}")
            return False
