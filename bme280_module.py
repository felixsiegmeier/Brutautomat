from machine import Pin, I2C
import bme280

class BME280():
    def __init__(self, sda, scl):
        i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)
        self.bme = bme280.BME280(i2c=i2c)
    
    def get_temp(self):
        return self.bme.temperature
    
    def get_humidity(self):
        return self.bme.humidity
    
    def get_pressure(self):
        return self.bme.pressure