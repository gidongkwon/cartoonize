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

def edge(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 80, 120)
    # dot_removed = cv2.morphologyEx(edged, cv2.MORPH_OPEN, None)
    dilated = cv2.dilate(edged, np.ones((3, 3), np.uint8), iterations=1)
    return dilated

def segment_color(img, cluster_n, epochs, accuracy):
    data = np.float32(img)
    data = data.reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, epochs, accuracy)
    _, labels, centers = cv2.kmeans(data, cluster_n, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    result = centers[labels.flatten()]
    result = result.reshape(img.shape)

    return result

while True:
    # 이미지 불러오기
    original_img = cv2.imread(os.path.join(image_dir, image_files[current_image]))

    gaussian_blurred_img = cv2.GaussianBlur(original_img, (5, 5), 1.4)
    edge_img = cv2.bitwise_not(edge(gaussian_blurred_img))
    edge_img = cv2.cvtColor(edge_img, cv2.COLOR_GRAY2RGB)
    segmented_img = segment_color(original_img, 8, 5, 0.03)
    blurred_img = cv2.bilateralFilter(segmented_img, 8, 200, 200)
    
    # cartoon = cv2.bitwise_and(blurred_img, blurred_img, mask=edge_img)
    cartoon = cv2.bitwise_and(blurred_img, edge_img)

    # 이미지 크기 조정
    height, width = cartoon.shape[:2]
    if width > max_width or height > max_height:
        scale = min(max_width / width, max_height / height)
        cartoon = cv2.resize(cartoon, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        original_img = cv2.resize(original_img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        edge_img = cv2.resize(edge_img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    # 이미지 보여주기
    cv2.imshow('Cartoon Image', np.hstack((original_img, cartoon, edge_img)))

    # 키보드 입력 처리
    key = cv2.waitKey(0)
    if key == 27:  # Esc 키
        break
    elif key == ord('-'):
        current_image = (current_image - 1) % len(image_files)
    elif key == ord('='):
        current_image = (current_image + 1) % len(image_files)