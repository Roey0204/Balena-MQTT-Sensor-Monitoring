# GPIO Wiring Guide for Raspberry Pi

This guide shows how to connect various sensors to GPIO pin 14 on your Raspberry Pi.

## GPIO Pin Layout

### BCM vs Physical Pin Numbering

This project uses **BCM (Broadcom) numbering**:
- GPIO 14 = Physical Pin 8

```
Raspberry Pi GPIO Pinout (40-pin header):
┌─────────────────────────────────────────┐
│                                         │
│  3.3V    (1)  (2)   5V                  │
│  GPIO2   (3)  (4)   5V                  │
│  GPIO3   (5)  (6)   GND                 │
│  GPIO4   (7)  (8)   GPIO14 ◄── USE THIS │
│  GND     (9)  (10)  GPIO15              │
│  GPIO17  (11) (12)  GPIO18              │
│  GPIO27  (13) (14)  GND                 │
│  GPIO22  (15) (16)  GPIO23              │
│  3.3V    (17) (18)  GPIO24              │
│  GPIO10  (19) (20)  GND                 │
│  GPIO9   (21) (22)  GPIO25              │
│  GPIO11  (23) (24)  GPIO8               │
│  GND     (25) (26)  GPIO7               │
│  ...                                    │
└─────────────────────────────────────────┘
```

## Common Sensor Connections

### 1. Push Button / Switch

**Simple momentary button:**

```
┌──────────┐
│  Button  │
│          │
│   [1]────┼──── GPIO 14 (Pin 8)
│          │
│   [2]────┼──── GND (Pin 6)
│          │
└──────────┘
```

**Configuration:**
- Uses internal pull-down resistor
- Button pressed = HIGH (1)
- Button released = LOW (0)

### 2. PIR Motion Sensor (HC-SR501)

**3-pin sensor:**

```
┌─────────────┐
│ PIR Sensor  │
│             │
│  VCC ───────┼──── 5V (Pin 2 or 4)
│  OUT ───────┼──── GPIO 14 (Pin 8)
│  GND ───────┼──── GND (Pin 6)
│             │
└─────────────┘
```

**Behavior:**
- Motion detected = HIGH (1)
- No motion = LOW (0)
- Typical trigger time: 2-5 seconds

### 3. Magnetic Door/Window Sensor (Reed Switch)

**2-wire sensor:**

```
┌──────────────┐
│ Reed Switch  │
│              │
│   [1] ───────┼──── GPIO 14 (Pin 8)
│              │
│   [2] ───────┼──── GND (Pin 6)
│              │
└──────────────┘
```

**Behavior:**
- Door closed (magnet near) = LOW (0)
- Door open (magnet away) = HIGH (1)

### 4. Water/Moisture Sensor

**Digital output sensor:**

```
┌──────────────┐
│ Water Sensor │
│              │
│  VCC ────────┼──── 3.3V (Pin 1)
│  DO ─────────┼──── GPIO 14 (Pin 8)
│  GND ────────┼──── GND (Pin 6)
│              │
└──────────────┘
```

**Behavior:**
- Water detected = HIGH (1)
- No water = LOW (0)
- Adjust sensitivity with onboard potentiometer

### 5. Infrared Obstacle/Proximity Sensor

**3-pin sensor:**

```
┌──────────────┐
│  IR Sensor   │
│              │
│  VCC ────────┼──── 5V (Pin 2)
│  OUT ────────┼──── GPIO 14 (Pin 8)
│  GND ────────┼──── GND (Pin 6)
│              │
└──────────────┘
```

**Behavior:**
- Obstacle detected = LOW (0)
- No obstacle = HIGH (1)
- Detection range: 2-30cm (adjustable)

### 6. Tilt/Vibration Sensor (SW-520D)

**2-pin sensor:**

```
┌──────────────┐
│ Tilt Sensor  │
│              │
│   [1] ───────┼──── GPIO 14 (Pin 8)
│              │
│   [2] ───────┼──── GND (Pin 6)
│              │
└──────────────┘
```

**Behavior:**
- Upright = LOW (0)
- Tilted = HIGH (1)

### 7. Sound Detection Sensor

**3-pin sensor:**

```
┌──────────────┐
│Sound Sensor  │
│              │
│  VCC ────────┼──── 3.3V (Pin 1)
│  OUT ────────┼──── GPIO 14 (Pin 8)
│  GND ────────┼──── GND (Pin 6)
│              │
└──────────────┘
```

**Behavior:**
- Sound detected = HIGH (1)
- Quiet = LOW (0)
- Adjust sensitivity with onboard potentiometer

## Voltage Levels

### Important Notes:

⚠️ **Raspberry Pi GPIO pins are 3.3V tolerant!**

- **Safe:** 0V (LOW) to 3.3V (HIGH)
- **Dangerous:** 5V input can damage GPIO pins
- **Solution:** Use voltage divider or level shifter for 5V sensors

### Voltage Divider for 5V Sensors

If your sensor outputs 5V, use this circuit:

```
Sensor 5V OUT
     │
     ├─── 2kΩ resistor ───┬─── GPIO 14
     │                    │
     └─── 3kΩ resistor ───┴─── GND

Output voltage = 5V × (3kΩ / (2kΩ + 3kΩ)) = 3V ✓
```

## Testing Your Wiring

### Method 1: Multimeter
1. Set multimeter to DC voltage mode
2. Connect black probe to GND
3. Connect red probe to GPIO 14
4. Trigger sensor
5. Should read ~3.3V (HIGH) or ~0V (LOW)

### Method 2: LED Test
```
GPIO 14 ──── [220Ω resistor] ──── [LED +] ──── [LED -] ──── GND
```
LED lights up = HIGH, LED off = LOW

### Method 3: Python Test Script

```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        state = GPIO.input(14)
        print(f"GPIO 14: {'HIGH' if state else 'LOW'}")
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
```

## Pull-up vs Pull-down Resistors

### Current Configuration: Pull-down

```python
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
```

- Pin pulled to LOW (0V) by default
- Sensor connects pin to HIGH (3.3V) when triggered
- Best for: Buttons, switches, normally-open sensors

### Alternative: Pull-up

```python
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
```

- Pin pulled to HIGH (3.3V) by default
- Sensor connects pin to LOW (0V) when triggered
- Best for: Normally-closed sensors, inverted logic

## Multiple Sensors

To read multiple GPIO pins, modify the code:

### Wiring Multiple Sensors

```
Sensor 1 OUT ──── GPIO 14 (Pin 8)
Sensor 2 OUT ──── GPIO 15 (Pin 10)
Sensor 3 OUT ──── GPIO 17 (Pin 11)
All GND ──────── GND (Pin 6, 9, 14, 20, 25, 30, 34, 39)
All VCC ──────── 3.3V or 5V (appropriate pins)
```

### Code Modification

Edit `sensor-monitor/sensor_module.py`:

```python
def __init__(self):
    self.gpio_pins = [14, 15, 17]
    GPIO.setmode(GPIO.BCM)
    for pin in self.gpio_pins:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_all_sensors(self):
    return {
        f'gpio_{pin}': {
            'state': GPIO.input(pin),
            'state_label': 'HIGH' if GPIO.input(pin) else 'LOW'
        }
        for pin in self.gpio_pins
    }
```

## Troubleshooting

### Sensor always reads HIGH
- Check pull-down resistor is enabled
- Verify sensor GND is connected
- Test sensor with multimeter

### Sensor always reads LOW
- Check sensor power (VCC) connection
- Verify sensor is working (test with LED)
- Check for loose connections

### Erratic readings
- Add 0.1µF capacitor between GPIO and GND (debouncing)
- Check for electromagnetic interference
- Ensure good connections (solder vs breadboard)

### Permission denied errors
- Container needs `privileged: true` (already set)
- GPIO devices must be mounted (already configured)

## Safety Tips

1. **Never exceed 3.3V on GPIO pins** (except 5V-tolerant pins)
2. **Always connect GND first** when wiring
3. **Use current-limiting resistors** for LEDs
4. **Double-check polarity** before powering on
5. **Disconnect power** before changing wiring

## Additional Resources

- [Raspberry Pi GPIO Pinout](https://pinout.xyz/)
- [RPi.GPIO Documentation](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/)
- [Balena GPIO Guide](https://www.balena.io/docs/learn/develop/hardware/)
