import spidev
import time

TURB_CHANNEL = 7

spi = spidev.SpiDev() # SPI Device Instance
spi.open(0,0) # open(spi_bus, device_channel) for the MCP3008
spi.max_speed_hz = 1000000

def readadc(adc_channel):  # read out the ADC
    if ((adc_channel > 7) or (adc_channel < 0)):  # Out of range MCP3008 port
        return -1
    r = spi.xfer2([1, (0x08 + adc_channel) << 4, 0])  # 
    adc_out = ((r[1] & 0x03) << 8) + r[2]     #
    return adc_out





if __name__ == "__main__":
    while True:
        Turb_value = readadc(TURB_CHANNEL)
        voltage = Turb_value * (3.3 / 1023)
        print("MCP3008 read value : %d" %Turb_value)
        print("Trubidity : %.1lf" %voltage)
    
        time.sleep(20)
    