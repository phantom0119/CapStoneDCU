import socket   # socket Connect
import spidev   # mcp3008 SPI 
import time     
import sensor_temP_DS18B20 as temp  
import sensor_DO as DO
import serial   
import pynmea2  # GPS NMEA

spi = spidev.SpiDev()       # SPI Device Instance(SPI )
spi.open(0, 0)              # open(spi_bus, device_channel). CS=0
spi.max_speed_hz= 1350000   # SPI speed (135000hz)

PH_CHANNEL = 0      # MCP3008 CH0
DO_CHANNEL = 1      # MCP3008 CH1
TURB_CHANNEL = 7    # MCP3008 CH7
OFFSET = 0.47       # pH 
TWO_CALIBRATION = 1         # DO 
GPS_PORT = "/dev/ttyS0"     # GPS 
BAUDRATE = 9600             # GPS baud rate

HOST = '192.168.3.4'  # (Ubuntu) localhost
PORT = 5538

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # 소켓 객체 생성(ipv4, TCP)  # 포트 사용 에러 해결
server.connect((HOST,PORT))

DO_Table = [14600, 14220, 13800, 13440, 13080, 12760, 12440, 12110, 11830, 11560,
    11290, 11040, 10760, 10540, 10310, 10060, 9860, 9640, 9470, 9270,
    9090, 8910, 8740, 8570, 8410, 8250, 8110, 7960, 7830, 7680,
    7560, 7430, 7300, 7170, 7060, 6940, 6840, 6720, 6600, 6520,
    6400, 6330, 6230, 6130, 6060, 5970, 5880, 5790]

# MCP3008 
def readadc(adc_channel):  
    if ((adc_channel > 7) or (adc_channel < 0)): 
        return -1
    r = spi.xfer2([1, (0x08 + adc_channel) << 4, 0]) 
    adc_out = ((r[1] & 0x03) << 8) + r[2]     
    return adc_out    


if __name__ == "__main__":
    while True:
        temperature = temp.read_temp()
        print("CEL temperature =%.2f" %temperature)
        time.sleep(2)

        mcp_Turb = readadc(TURB_CHANNEL)
        Turb_volt = mcp_Turb * (3.3 / 1024)
        print("MCP3008 read value(Turbidity) : %d" %mcp_Turb)
        print("Turbidity : %.1lf" %Turb_volt)
        time.sleep(2)
            
            # pH 데이터 수신
        mcp_pH = readadc(PH_CHANNEL)
        pH_volt = mcp_pH * (3.3 / 1024)
        pH_value = pH_volt * 3.5 + OFFSET
        print("MCP3008 read value(pH) = %d " %mcp_pH)
        print("pH Voltage = %.2lf " %pH_volt) 
        print (pH_value, "PH")
        time.sleep(2)
            
        # DO 데이터 수신
        mcp_DO = readadc(DO_CHANNEL)
        DO_volt = mcp_DO * (3.3 / 1024)
        print("MCP3008 read value(DO) : %d" %mcp_DO)
        print("DO voltage = %.2lf" %DO_volt)
        DO_value = DO.readDO(DO_volt, int(temperature))
        print(DO_value, " mg/L")
            
        data_table = str(temperature) + ',' + str(Turb_volt) + ',' +\
                     str(pH_value) + ',' + str(DO_value)
        
        server.send(data_table.encode())
        reply = server.recv(1024)
            
        if reply.decode() == 'received':
            print("data sending success!")

        time.sleep(600) 