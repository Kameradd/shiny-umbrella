import time
import board
import digitalio
import adafruit_dht

try:
    dht_device = adafruit_dht.DHT22(board.D4, use_pulseio=False)
except Exception as e:
    print(f"Failed to init DHT22: {e}")
    dht_device = None


pir_sensor = digitalio.DigitalInOut(board.D17)
pir_sensor.direction = digitalio.Direction.INPUT


sound_sensor = digitalio.DigitalInOut(board.D27)
sound_sensor.direction = digitalio.Direction.INPUT

print("Sensors initialized. Starting readings...")

motion_detected = False
sound_detected = False

while True:
    try:

        current_motion = pir_sensor.value
        if current_motion and not motion_detected:
            print("Motion detected")
        elif not current_motion and motion_detected:
            print("Motion stopped.")
        motion_detected = current_motion
        current_sound = not sound_sensor.value
        if current_sound and not sound_detected:
            print("Sound detected")
        sound_detected = current_sound

        if dht_device:
            try:
                temp_c = dht_device.temperature
                humidity = dht_device.humidity
                if temp_c is not None and humidity is not None:
                    print(f"Temp: {temp_c:.1f}°C | Humidity: {humidity:.1f}%")
                else:

                    pass
            except RuntimeError as error:
                pass

        time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nExiting program.")
        break
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        break

if dht_device:
    dht_device.exit()
pir_sensor.deinit()
sound_sensor.deinit()
print("GPIO cleanup complete.")
