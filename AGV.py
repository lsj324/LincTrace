import socket
import struct
import cv2
import pickle
import threading
from pymycobot.myagv import MyAgv

# AGV 초기화
agv = MyAgv("/dev/ttyAMA2", 115200)

# 초기 색상 설정
color = 1

# 모터 초기화 함수
def initMotor():   
    print("init")

# AGV를 전진시키는 함수
def goForward():
    print("goForward")
    agv.go_ahead1(1)

# AGV를 왼쪽으로 회전시키는 함수
def Left():
    print("left")
    agv.counterclockwise_rotation1(1)

# AGV를 오른쪽으로 회전시키는 함수
def Right():
    print("right")
    agv.clockwise_rotation1(1)

# AGV를 정지시키는 함수
def stopMotor():
    print("stopMotor")
    agv.stop()


# 모터 초기화 실행
initMotor()

# 서버 설정
HOST = '172.30.1.54'
PORT = 8080

# 소켓 생성
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# 호스트와 포트를 바인딩
server.bind((HOST, PORT))
print('Socket bind complete')

# 소켓을 리스닝 모드로 설정
server.listen(10)
print('Socket now listening')

# 클라이언트의 연결을 수락
server_cam, addr = server.accept()
print('New Client.')

# 종료 플래그
flag_exit = False

# 모터 제어 메인 함수
def mot_main():
    global flag_exit, color
    while True:
        if color == 0:
            goForward()
        elif color == 1.0:
            stopMotor()
        elif color == 2.0:
            Left()
        elif color == 3.0:
            Right()
        else:
            continue

        if flag_exit:
            print("exit")
            break

# 모터 제어 스레드 시작
motThread = threading.Thread(target=mot_main)
motThread.start()

try:
    while True:
        # 클라이언트로부터 명령을 수신
        cmd_byte = server_cam.recv(1)
        cmd = struct.unpack('!B', cmd_byte)

        if cmd[0] == 13:
            color_byte = server_cam.recv(1)
            color = struct.unpack('!B', color_byte)[0]
        elif cmd[0] == 14:
            color_byte = server_cam.recv(1)
            color = struct.unpack('!B', color_byte)[0]
        
except KeyboardInterrupt:
    pass
except ConnectionResetError:
    pass
except BrokenPipeError:
    pass
except Exception as e:
    print(f"Error: {e}")

# 종료 플래그 설정 및 스레드 종료 대기
flag_exit = True
motThread.join()
    
# 소켓 닫기
server_cam.close()
server.close()
