import os

import cv2

camera_index = 4
camera_device = '/dev/video4'

cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)
if not cap.isOpened():
    cap.release()
    cap = cv2.VideoCapture(camera_index)
if not cap.isOpened():
    cap.release()
    cap = cv2.VideoCapture(camera_device)
cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Camera', 1280, 720)
photo_count = 0

os.makedirs('./photos', exist_ok=True)

if not cap.isOpened():
    print(f'无法打开摄像头: {camera_device}')
    raise SystemExit(1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print(f'无法读取摄像头画面: {camera_device}')
        break

    cv2.imshow('Camera', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        image_path = f'./photos/calibration_image{photo_count}.jpg'
        if cv2.imwrite(image_path, frame):
            print(f'已保存图片: {image_path}')
        else:
            print(f'保存失败: {image_path}')
        photo_count += 1

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()