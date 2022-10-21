import spidev
#import RPi.GPIO as GPIO
import time
#import sys
import sensor_temP_DS18B20 as temp

spi = spidev.SpiDev()  # SPI Device Instance(SPI 객체 생성)
spi.open(0, 0)  # open(spi_bus, device_channel). CS=0
spi.max_speed_hz=1350000  # SPI speed (135000hz)

pH_channel = 0  # MCP3008 CH0 연결
OFFSET = 0.47

def readadc(adc_channel):  # read out the ADC
    if ((adc_channel > 7) or (adc_channel < 0)):  # Out of range MCP3008 port
        return -1
    r = spi.xfer2([1, (0x08 + adc_channel) << 4, 0]) 
    adc_out = ((r[1] & 0x03) << 8) + r[2]     
    return adc_out


if __name__ == "__main__":
    while True:
        temperature = round(temp.read_temp())
        Value = readadc(pH_channel) #read adc channel 0
        voltage = Value*3.3/1024
        phvalue = voltage*3.5 + OFFSET
    
        print("Temperature : %d" %temperature)
        print("MCP3008 read value = %d " % Value)
        print("change to V = %.2lf " % voltage) 
        print (phvalue, "PH")
        time.sleep(5)