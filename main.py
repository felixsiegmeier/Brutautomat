from machine import Pin, I2C
from rotary import Encoder
from ssd1306 import SSD1306_I2C
import bme280_module, stepper
import time

# === Pin-Setup ===

#I2C for oled and bme280
sda = 21 #D2
scl = 22 #D1

# Stepper motor
in1 = Pin(16,Pin.OUT)
in2 = Pin(17,Pin.OUT)
in3 = Pin(18,Pin.OUT)
in4 = Pin(19,Pin.OUT)

# Drehgeber
clk = 26
dt = 27

# Mosfet Ventilator + Heizung = werden zusammen geschaltet
heat_vent_pin = 23

# === Initialize Modules ===

# Sensor
bme_sensor = bme280_module.BME280(sda_pin=sda, scl_pin=scl)

# Oled
oled = SSD1306_I2C(128, 64, I2C(scl=Pin(scl), sda=Pin(sda)))

# stepper
stepper = stepper.create(in1, in2, in3, in4, delay=2)

# drehgeber
enc = Encoder(pin_clk=clk, pin_dt=dt, min_val=0, max_val=450)
prev = time.time()
    # val = enc.value

# mosfet
heat_vent = Pin(heat_vent_pin,Pin.OUT)

# === Zum Beginn einmal drehen ===

stepper.angle(180)

# === Loop ===
while True:
    oled.fill(0)
    oled.text("Ziel: " + str(enc.value/10) + " C", 0, 5)
    oled.text("Temp.: " + str(bme_sensor.get_temp().strip("C")) + " C", 0, 25)
    oled.text("Humidity: " + str(bme_sensor.get_humidity().strip("%")) + " %", 0, 45)
    oled.show()
    if enc.value/10 - float(bme_sensor.get_temp().strip("C")) > 1:
        heat_vent.value(1)
    if float(bme_sensor.get_temp().strip("C")) - enc.value/10 > 0.5:
        heat_vent.value(0)
    if time.time() - prev > 21600: # 21600 Sekunden = 6 Stunden
        stepper.angle(180)
        prev = time.time()