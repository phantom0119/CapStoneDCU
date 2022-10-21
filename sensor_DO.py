import spidev
import time
import sensor_temP_DS18B20 as temp

spi = spidev.SpiDev() # SPI Device Instance
spi.open(0,0) # open(spi_bus, device_channel) for the MCP3008
spi.max_speed_hz =1350000

DO_Channel = 1
TWO_CALIBRATION = 1

# value (mg/L * 1000), refer to the DO_table in the DFRobot.com
DO_Table = [14600, 14220, 13800, 13440, 13080, 12760, 12440, 12110, 11830, 11560,
    11290, 11040, 10760, 10540, 10310, 10060, 9860, 9640, 9470, 9270,
    9090, 8910, 8740, 8570, 8410, 8250, 8110, 7960, 7830, 7680,
    7560, 7430, 7300, 7170, 7060, 6940, 6840, 6720, 6600, 6520,
    6400, 6330, 6230, 6130, 6060, 5970, 5880, 5790]

def readadc(adc_channel):  # read out the ADC
    if ((adc_channel > 7) or (adc_channel < 0)):  # Out of range MCP3008 port
        return -1
    r = spi.xfer2([1, (0x08 + adc_channel) << 4, 0])  # 
    adc_out = ((r[1] & 0x03) << 8) + r[2]     #
    return adc_out

def readDO(mv_value, temp_c):
    CAL1_V = 1600
    CAL1_T = 25
    CAL2_V = 1300
    CAL2_T = 15
    if TWO_CALIBRATION == 0:
        V_saturation = CAL1_V + 35 * temp_c - CAL1_T * 35
    else:
        V_saturation = (temp_c - CAL2_T) * (CAL1_V - CAL2_V) / (CAL1_T - CAL2_T) + CAL2_V
    
    return mv_value * DO_Table[temp_c] / V_saturation


if __name__ == "__main__":
    while True:

        temperature = round(temp.read_temp())
        ADC_value = readadc(DO_Channel)
        ADC_voltage = ADC_value * 3.3 / 1024

        print("Temperature : %d" %temperature)
        print("MCP3008 read value : %d" %ADC_value)
        print("ADC_voltage = %.2lf" %ADC_voltage)
        print(readDO(ADC_voltage, temperature), " mg/L")
    
        time.sleep(20)



