import time
import board
import digitalio
import adafruit_dht

# --- 1. SENSOR INITIALIZATION ---

# Initialize DHT22 Temperature/Humidity Sensor
# The 'use_pulseio=False' is important for Linux-based boards
try:
    dht_device = adafruit_dht.DHT22(board.D4, use_pulseio=False)
except Exception as e:
    print(f"Failed to init DHT22: {e}")
    dht_device = None

# Initialize PIR Motion Sensor (HC-SR501)
pir_sensor = digitalio.DigitalInOut(board.D17)
pir_sensor.direction = digitalio.Direction.INPUT

# Initialize Sound Detection Sensor (KY-037) - Digital Output
sound_sensor = digitalio.DigitalInOut(board.D27)
sound_sensor.direction = digitalio.Direction.INPUT

print("Sensors initialized. Starting readings...")

# --- 2. MAIN LOOP ---

# Variables to track state changes
motion_detected = False
sound_detected = False

while True:
    try:
        # --- Read PIR Motion Sensor ---
        # The PIR output is HIGH when motion is detected.
        current_motion = pir_sensor.value
        if current_motion and not motion_detected:
            print("🏃 Motion DETECTED!")
        elif not current_motion and motion_detected:
            print("Motion stopped.")
        motion_detected = current_motion

        # --- Read Sound Sensor ---
        # The DO pin is normally HIGH and goes LOW when sound is detected.
        # So, we check for a 'False' value.
        current_sound = not sound_sensor.value
        if current_sound and not sound_detected:
            print("🎤 Sound DETECTED!")
        sound_detected = current_sound

        # --- Read DHT22 Sensor ---
        if dht_device:
            try:
                temp_c = dht_device.temperature
                humidity = dht_device.humidity
                if temp_c is not None and humidity is not None:
                    print(f"🌡️ Temp: {temp_c:.1f}°C | Humidity: {humidity:.1f}%")
                else:
                    # Sensor read can fail, this is normal
                    pass
            except RuntimeError as error:
                # DHTs are prone to timing errors, just ignore and retry
                pass

        # Small delay to prevent spamming the console
        time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nExiting program.")
        break
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        break

# Clean up GPIO resources
if dht_device:
    dht_device.exit()
pir_sensor.deinit()
sound_sensor.deinit()
print("GPIO cleanup complete.")