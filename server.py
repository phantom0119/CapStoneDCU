import socket
import pymysql    # MariaDB
import time

DEVICE = '202105191705'     # 수질 측정 장비 고유 번호
HOST = '192.168.3.4'         # 메인 서버(Server) IP 주소
PORT = 5538                 # 메인 서버에서 개방할 포트 번호

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # 소켓 객체 생성(ipv4, Byte Stream)
   # 일반 소켓 레벨 설정, 이미 사용 중인 주소&포트에 대해 바인드 허용
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
print("Socket creation complete!")

   # 서버 IP와 PORT 결합 확인 (예외처리 적용)
try:
	server.bind((HOST, PORT))      # 소켓 바인드
except socket.error:
	print("Bind failed")
	exit()

server.listen()                                  # 클라이언트 접속 허용
print("Socket waiting for client messages")
(client_socket, addr) = server.accept()         # 클라이언트가 접속하면 새로운 소켓 반환
print(f"client_socket connected = {addr}")

   # MariaDB에 연결하기 위한 주소 및 사용자 계정, 연결할 데이터베이스, 문자 포맷팅 값
connect_maria = pymysql.connect(host='127.0.0.1', user='hansuBot',\
    password='dfg09787', db='hansu', charset='utf8' )  

cur = connect_maria.cursor()  # MariaDB 커서 (SQL문 적용에 사용) 

   # 데이터베이스에 Sensor_Data 테이블이 존재하지 않는다면 sql을 통해 생성. (저장된 이후에는 적용 안 됨)
sql = 'CREATE TABLE IF NOT EXISTS Sensor_Data (time DATETIME, deviceNumber CHAR(12), Temperature DECIMAL(4, 2), Turbidity DECIMAL(4, 2), pH DECIMAL(4, 2), DO DECIMAL(4, 2))'

cur.execute(sql)            # 커서를 통한 sql 실행

connect_maria.commit()    # MariaDB에서 수행한 작업이나 SQL 반영




    # 클라이언트(라즈베리파이)와 연결 되었을 때 수행하는 과정
try:
	while True:
		data = client_socket.recv(1024)          # 클라이언트로부터 데이터 수신
		data = data.decode()	                 # 수신한 데이터 디코딩(decode)
		data_table = data.split(',')                # 쉼표(,)를 기준으로 구분하는 리스트 생성
		print("Sensor Data Received " + data)    # 예비 출력
		reply = 'received'
		client_socket.send(reply.encode())        # 클라이언트에 수신 완료 전달

		print("All Data Signal GOOD! Save DB...")
                   # 수집 시간 포맷(MariaDB의 Sensor_Data 테이블에 저장할 목적)
		local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())   
                   # Sensor_Data에 수질 데이터를 저장하는 SQL 
		sql = "INSERT INTO Sensor_Data VALUES('" + local_time + "','" + DEVICE + "','" + data_table[0] + "','" + data_table[1] + "','" + data_table[2] + "','" + data_table[3] +"')"
		print(sql)
		cur.execute(sql)             # sql 문 실행
		connect_maria.commit()     # 데이터베이스에 반영
		print("Send Success")
except KeyboardInterrupt:                   # 키보드 강제 종료 입력(ctrl+c, ctrl+z) 처리
	print("DB Server Stop to save")
	exit()
finally:                                      # 서버 연결 종료 시
	connect_maria.close()
	client_socket.close()
	server.close() 