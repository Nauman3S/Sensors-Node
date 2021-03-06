# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT


import adafruit_bme680

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
temperature_offset = -5


def getTempGasHumidPressAlti_BME680():
    global bme680
    payload = str(bme680.temperature + temperature_offset)+","+str(bme680.gas)+"," + \
        str(bme680.relative_humidity)+"," + \
        str(bme680.pressure)+","+str(bme680.altitude)
    return payload
