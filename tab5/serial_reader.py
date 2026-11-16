
import time

import serial

from tab5.parser import parse_sensor_message


def read_device(
    skip_invalid=False,
    verbose=True,
    port="COM3",
    baudrate=115200,
    serial_timeout=10,
    ):
    measurements = []

    start_time = time.monotonic()
    elapsed = 0
    max_elapsed = 45

    with serial.Serial(port, baudrate, timeout=serial_timeout) as device:
        while elapsed <= max_elapsed and len(measurements) < 5:
            raw_data = device.readline()
            message = raw_data.decode("utf-8", errors="replace").strip()

            if message.startswith("CO2:"):
                try:
                    reading = parse_sensor_message(message)
                    if verbose:
                        print(reading)
                    measurements.append(reading)
                except ValueError as error:
                    print(f"Invalid sensor message: {error}")
                    if not skip_invalid:
                        raise

            elapsed = time.monotonic() - start_time

    return measurements


if __name__ == "__main__":
    read_device()
