import os
import glob
import time

# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')

w1_device_dir = '/sys/bus/w1/devices/'
w1_data_dir = glob.glob(w1_device_dir + '28*')[0]
w1_device_file = w1_data_dir + '/w1_slave'


def read_temp_raw():
   f = open(w1_device_file, 'r')
   lines = f.readlines()
   f.close()
   return lines


"""
저장된 내용은 다음 예시와 같은 구조를 가진다.
be 01 55 00 7f ff 0c 10 1f : crc=1f YES
be 01 55 00 7f ff 0c 10 1f t=27875

내용을 readlines()하여 저장한 lines의 첫 줄 마지막 YES = 데이터 수신 완료
lines의 두 번째 줄 t= 다음의 데이터가 온도 값 (27875 = 27.875)
"""
 
def read_temp():
   lines = read_temp_raw()

   while lines[0].strip()[-3:] != 'YES':
      time.sleep(1.0)
      lines = read_temp_raw()

   equals_pos = lines[1].find('t=')

   if equals_pos != -1:
      temp_string = lines[1][equals_pos+2:]
      temp_c = float(temp_string) / 1000.0
      return temp_c
    


if __name__ == "__main__":
    while True:
       print("CEL temperature =%.2f" %read_temp())
       time.sleep(20)
