from machine import Pin, I2C
from rotary import Encoder
from ssd1306 import SSD1306_I2C
import bme280_module, stepper

# === Pin-Setup ===

#I2C for oled and bme280
sda_pin = 5 #D2
scl_pin = 4 #D1

# Stepper motor
in1 = 1 #TX
in2 = 0 #D3
in3 = 2 #D4
in4 = 15 #D8

# Drehgeber
clk = 14 #D5
dt = 12 #D6
sw = 3 #RX

# Mosfet Ventilator + Heizung = werden zusammen geschaltet
heat_vent_pin = 13 #D7

# === Initialize Modules ===

# Sensor
bme_sensor = bme280_module.BME280(sda_pin=sda_pin, scl_pin=scl_pin)

# Oled
oled = SSD1306_I2C(128, 64, I2C(scl=Pin(scl_pin), sda=Pin(sda_pin)))

# stepper
stepper = stepper.create(in1, in2, in3, in4, delay=2)

# drehgeber
enc = Encoder(pin_clk=clk, pin_dt=dt, min_val=0, max_val=450)
prev = time.ticks_ms()
    # val = enc.value

'''
Falls der Button überhaupt gebraucht wird.... aktuell sehe ich keine Notwendigkeit für das Teil
def callback(arg):
    global prev
    if time.ticks_ms() - prev > 500 or prev > time.ticks_ms():
        # do something special
        prev = time.ticks_ms()

button = Pin(sw, Pin.IN)
button.irq(trigger=Pin.IRQ_FALLING, handler=callback)
'''
# mosfet
heat_vent = Pin(heat_vent_pin,Pin.OUT)

# === Loop ===
while True:
    self.oled.fill(0)
    self.oled.text("Temp. Ziel: " + str(enc.value/10) + " C", 0, 5)
    self.oled.text("Temp.: " + str(sensor.get_temp()) + " C", 0, 5)
    self.oled.text("Humidity: " + str(sensor.get_humidity()) + " %", 0, 25)
    self.oled.show()
    if enc.value/10 - sensor.get_temp() > 1:
        heat_vent.value(1)
    if sensor.get_temp() - enc.value/1 > 0.5:
        heat_vent.value(0)