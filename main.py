import cv2
import numpy as np
import os

# 이미지 폴더 경로
image_dir = './images'

# 이미지 파일 목록 가져오기
image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))]

# 이미지 파일이 없으면 종료
if not image_files:
    print('이미지 파일이 없습니다.')
    exit()

# 현재 이미지 인덱스
current_image = 0

# 창의 최대 크기 설정
max_width = 1280
max_height = 720

while True:
    # 이미지 불러오기
    img = cv2.imread(os.path.join(image_dir, image_files[current_image]))

    # 그레이스케일 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 가우시안 블러 적용
    gray = cv2.GaussianBlur(gray, (0, 0), 2)

    # 적응형 이진화 적용
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # 컬러 이미지에 윤곽선 적용
    color = cv2.bitwise_and(img, img, mask=cv2.bitwise_not(edges))
    # color = cv2.bilateralFilter(color, -1, 20.0, 7.0)

    # 윤곽선에 컬러 적용
    edges_color = cv2.bitwise_and(img, img, mask=edges)

    # 최종 합성
    cartoon = cv2.bitwise_or(color, edges_color)

    # 이미지 크기 조정
    height, width = cartoon.shape[:2]
    if width > max_width or height > max_height:
        scale = min(max_width / width, max_height / height)
        cartoon = cv2.resize(cartoon, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    # 이미지 보여주기
    cv2.imshow('Cartoon Image', np.hstack((img, cartoon)))

    # 키보드 입력 처리
    key = cv2.waitKey(0)
    if key == 27:  # Esc 키
        break
    elif key == ord('-'):
        current_image = (current_image - 1) % len(image_files)
    elif key == ord('='):
        current_image = (current_image + 1) % len(image_files)