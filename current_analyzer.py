"""Raspberry Pi Zero current analyzer"""
from datetime import datetime
import time
import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
import keyboard

#Define I2C
i2c_bus = board.I2C()

#Assing variables to I2C buses
ina3 = INA219(i2c_bus,addr=0x42)
ina2 = INA219(i2c_bus,addr=0x41)


# Configuration
ina3.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina3.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina3.bus_voltage_range = BusVoltageRange.RANGE_16V

ina2.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina2.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina2.bus_voltage_range = BusVoltageRange.RANGE_16V

#Create output name
filename = str(datetime.now()).replace("-","").replace(" ","-").split(".")[0] + ".csv"

#Create file and headers
with open(filename,'a') as f:
    f.write("Time,Voltage,Current,Power,BatteryVoltage\n")

# measure and display loop
while True:
    bus_voltage3 = ina3.bus_voltage        # voltage on V- (load side)
    shunt_voltage3 = ina3.shunt_voltage    # voltage between V+ and V- across the shunt
    power3 = ina3.power
    current3 = ina3.current                # current in mA

    bus_voltage2 = ina2.bus_voltage        # voltage on V- (load side)
    shunt_voltage2 = ina2.shunt_voltage    # voltage between V+ and V- across the shunt

    
    # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
    print("PSU Voltage:{:6.3f}V    Power:{:9.6f}W    Current:{:9.6f}mA    Battery Voltage:{:6.3f}   //Hold Esc to stop".format((bus_voltage3 + shunt_voltage3),(power3),(-current3),(bus_voltage2 + shunt_voltage2)))
    print("")
    with open(filename,'a') as f:
        f.write(str(time.strftime("%I:%M:%S"))+",{:6.3f},{:9.6f},{:9.6f},{:63f}\n".format((bus_voltage3+shunt_voltage3),(-current3/1000),(power3),(bus_voltage2+shunt_voltage2)))
    #detect Esc
    if keyboard.is_pressed("Esc"):
        print("Uploading")
        time.sleep(3)
        break

    time.sleep(2)
