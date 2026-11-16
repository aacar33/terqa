
def parse_sensor_message(message):
    parsed = {}
    readings = message.split("|")

    for reading in readings:
        name, value = reading.split(":")
        name = name.strip()

        if name == "CO2":
            actual_value = int(value.split()[0])
        else:
            actual_value = float(value.split()[0])

        parsed[name] = actual_value

    expected_readings = {"CO2", "Temp", "Humidity"}

    if parsed.keys() != expected_readings:
        raise ValueError("Invalid sensor measurements")

    return parsed
