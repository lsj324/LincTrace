
![DALL·E 2024-06-20 14 31 01 - A detailed illustration of a line follower robot navigating along a black line on a white surface  The robot is small, with wheels and sensors positio](https://github.com/lsj324/LincTrace/assets/170494075/755556ca-d286-4a7c-9387-3c03b27007b1)


**목표**

- YOLO로 신호등을 인식하여 빨간불에는 멈추고 파란불에 움직이는 라인트레이서 개발

**팀원**

- 총 5명(YOLO 학습 및 라인트레이서 개발)

**기여한 부분**

- 라인트레이서 개발
    - opnCV로 노란색 라인을 검출하여 객체의 중심점 계산
    - 객체 중심점과 카메라 이미지의 중심점의 위치차에 따라 좌, 우, 전진으로 모터 제어
- 노트북과 AGV의 통신 개발
    - 노트북에서 YOLO와 라인트레이서로 처리된 값을 TCP 통신으로 AGV에 전달

**트러블 슈팅**

- **문제 배경**
    - AGV내의 라즈베리파이로 YOLO와 라인트레이서 기능을 실시간으로 처리하는데 딜레이가 생김
    - AGV가 원하는대로 움직이지 않거나 모터가 멈추지 않는 문제가 발생
- **해결 방법**
    - 노트북에서 YOLO, 라인트레이서 기능을 실행하여 처리된 값을 TCP통신을 통해  AGV로 전달하여 모터를 제어
    - 딜레이 없이 AGV가 정상적으로 작동

**성과**

- 노트북 웹캠을 이용하여 신호등의 빨간불과 바닥의 노란줄을 인식하여 myAGV로 명령을 전달, 자율주행을 수행함

**시기**

- 2024.03.27 ~ 2024.04.16 (3주간)****

**실행영상**


https://github.com/lsj324/LincTrace/assets/170494075/3202673b-8e7f-4d68-8a9b-2cc9b120b983

