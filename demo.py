"""Sample code and test for adafruit_in219"""

import time
import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219


i2c_bus = board.I2C()

ina3 = INA219(i2c_bus,addr=0x42)

print("ina219 test")


ina3.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina3.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina3.bus_voltage_range = BusVoltageRange.RANGE_16V


# measure and display loop
while True:
    
    bus_voltage3 = ina3.bus_voltage        # voltage on V- (load side)
    shunt_voltage3 = ina3.shunt_voltage    # voltage between V+ and V- across the shunt
    power3 = ina3.power
    current3 = ina3.current                # current in mA
    

    
    # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
    print("PSU Voltage:{:6.3f}V    Shunt Voltage:{:9.6f}V    Load Voltage:{:6.3f}V    Power:{:9.6f}W    Current:{:9.6f}A".format((bus_voltage3 + shunt_voltage3),(shunt_voltage3),(bus_voltage3),(power3),(current3/1000)))
    print("")
    time.sleep(1)