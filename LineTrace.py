from ultralytics import YOLO
import threading
import socket
import time
import struct
import numpy as np
import cv2


# YOLO 모델 로드 (신호등 인식용)
model = YOLO('traffic_red_green.pt')
# 라즈베리 파이의 호스트와 포트 설정
HOST_RPI = '172.30.1.54'
PORT = 8080

# 이전 명령을 저장하는 변수 초기화
prev_command = 100

# 프레임을 처리하여 노란색 라인을 인식하는 함수
def LineTrace_frame(frame):
    global prev_command
    # 프레임의 높이와 너비를 설정하고 관심 영역(ROI) 설정
    height, width, _ = frame.shape
    roi_height = height // 8
    roi_top = height - roi_height
    roi = frame[roi_top:, :]
    # BGR을 HSV 색상 공간으로 변환
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # 노란색의 하한과 상한 설정
    lower_yellow = np.array([20, 100, 100], dtype=np.uint8)
    upper_yellow = np.array([30, 255, 255], dtype=np.uint8)
    # 노란색 물체를 탐지하기 위한 마스크 생성
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    # 마스크를 사용하여 노이즈 제거
    kernel = np.ones((3, 3), np.uint8)
    yellow_mask = cv2.erode(yellow_mask, kernel, iterations=2)
    yellow_mask = cv2.dilate(yellow_mask, kernel, iterations=1)
    
    cv2.imshow('ROI', roi)  # ROI 이미지 출력
    cv2.imshow('MASK', yellow_mask)  # 마스크 이미지 출력

    # 노란색 물체의 윤곽선 찾기
    contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    direction = 100
    if contours:
        # 가장 큰 윤곽선 찾기
        max_contour = max(contours, key=cv2.contourArea)
        # 가장 큰 윤곽선의 중심점 찾기
        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            # 노란색 물체의 위치에 따라 로봇 동작 결정
            if cx < width // 3:
                if prev_command != 2:
                    direction = 2
            elif cx > width // 3 * 2:
                # 이전 명령이 오른쪽 회전이 아니면 오른쪽 회전
                if prev_command != 3:
                    direction = 3
            elif cx >= width // 3 and cx <= width // 3 * 2:
                if prev_command != 0:
                    direction = 0
            else:
                if prev_command != "NOTHING":
                    direction = "NOTHING"
    # 이전 명령을 저장
    prev_command = direction

# 소켓 생성 및 연결
client_cam = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_cam.connect((HOST_RPI, PORT))

# 카메라 스레드 함수
def camMain():
    global prev_command
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, img = cap.read()
        results = model(img)
        annotated_frame = results[0].plot()
        # 신호등이 인식될 경우
        if len(results[0].boxes.data) > 0:
            max_confidence_obj = max(results[0].boxes.data, key=lambda x: x[4])
            color = int(max_confidence_obj[5].item())

            # YOLO에서의 빨간색 신호등 값 송신
            color_byte = struct.pack('!B', color)
            client_cam.sendall(color_byte)
            
        # 신호등 인식이 안될 경우
        else:
            LineTrace_frame(img)
            print(prev_command)
            
            # 라인트레이싱에 따른 좌우전진 명령 송신
            color_byte = struct.pack('!B', prev_command)
            client_cam.sendall(color_byte)
            
        cv2.imshow('FRAME', annotated_frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        time.sleep(0.1)

    cv2.destroyAllWindows()

# 카메라 스레드 시작
camThread = threading.Thread(target=camMain)
camThread.start()
