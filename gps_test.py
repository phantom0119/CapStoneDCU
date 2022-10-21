import serial
import pynmea2
import time
# Before Start, sudo systemctl enable gpsd.socket
# sudo systemctl start gpsd.socket

GPS_PORT = "/dev/ttyS0"
BAUDRATE = 9600

while True:
    serial_gps = serial.Serial(GPS_PORT, BAUDRATE)
    #print(serial_gps)
    if serial_gps.readable():    
        data = serial_gps.readline()
        data_text = data.decode()
        #print(data.decode())
    else:
        print("error")
    
    if data_text[0:6] == "$GPRMC":
        location_data = pynmea2.parse(data_text)
        latitude_data = location_data.latitude
        longitude_data = location_data.longitude
        
        location = [latitude_data, longitude_data]
        print(f"Latitude = {location[0]}, Longitude = {location[1]}")

        time.sleep(20)