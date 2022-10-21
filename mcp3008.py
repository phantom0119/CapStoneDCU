import spidev, time

spi = spidev.SpiDev()
spi.open(0,0)

spi.max_speed_hz = 1350000

def analog_read(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_out = ((r[1]&3) << 8) + r[2]
    return adc_out


if __name__ == "__main__":
    while True:
        reading = analog_read(0)
        voltage = reading * 3.3 / 1024
        print("Reading = %d \ tVoltage = %f" %(reading, voltage))
        time.sleep(3)