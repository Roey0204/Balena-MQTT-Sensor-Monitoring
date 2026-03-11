#!/usr/bin/env python3
"""
Sensor Module for reading GPIO inputs on Raspberry Pi
"""

import logging
from typing import Dict, Any
import os

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except (ImportError, RuntimeError) as e:
    GPIO_AVAILABLE = False
    print(f"GPIO not available: {e}")

logger = logging.getLogger(__name__)


class SensorReader:
    """Reads GPIO pin 14 on Raspberry Pi"""
    
    def __init__(self, gpio_pin: int = 14):
        self.gpio_pin = gpio_pin
        self.gpio_initialized = False
        
        if GPIO_AVAILABLE:
            try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                self.gpio_initialized = True
                logger.info(f"Initialized GPIO pin {self.gpio_pin} for input reading")
            except Exception as e:
                logger.error(f"Failed to initialize GPIO: {e}")
                self.gpio_initialized = False
        else:
            logger.warning("GPIO library not available - running in simulation mode")
    
    def read_gpio_state(self) -> int:
        """Read the current state of GPIO pin 14"""
        if self.gpio_initialized:
            try:
                state = GPIO.input(self.gpio_pin)
                logger.debug(f"GPIO {self.gpio_pin} state: {state}")
                return state
            except Exception as e:
                logger.error(f"Error reading GPIO {self.gpio_pin}: {e}")
                return -1
        else:
            import random
            simulated_state = random.choice([0, 1])
            logger.debug(f"Simulated GPIO {self.gpio_pin} state: {simulated_state}")
            return simulated_state
    
    def read_all_sensors(self) -> Dict[str, Any]:
        """Read GPIO sensor data"""
        gpio_state = self.read_gpio_state()
        
        sensor_data = {
            'gpio_pin': self.gpio_pin,
            'state': gpio_state,
            'state_label': 'HIGH' if gpio_state == 1 else 'LOW' if gpio_state == 0 else 'ERROR'
        }
        
        return sensor_data
    
    def cleanup(self):
        """Cleanup GPIO resources"""
        if self.gpio_initialized and GPIO_AVAILABLE:
            try:
                GPIO.cleanup()
                logger.info("GPIO cleanup completed")
            except Exception as e:
                logger.error(f"Error during GPIO cleanup: {e}")
