import cv2
import numpy as np
from imutils.video import VideoStream
from yoloDetect import YoloDetect

# video = VideoStream(src=0).start()
# Chua cac diem nguoi dung chon de tao da giac
points = []

# new model Yolo
# model = YoloDetect()


def handle_left_click(event, x, y, flags, points):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])


def draw_polygon (frame, points):
    for point in points:
        frame = cv2.circle( frame, (point[0], point[1]), 5, (0,0,255), -1)

    frame = cv2.polylines(frame, [np.int32(points)], False, (255,0, 0), thickness=2)
    return frame

detect = False

# Đọc video
path = 'peopleOnRail.mp4'
cap = cv2.VideoCapture(path)

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
    # frame = video.read()
    # frame = cv2.flip(frame, 1)
    #     height, width, channels = frame.shape
    # model = YoloDetect()

    # Ve ploygon
        frame = draw_polygon(frame, points)
        model = YoloDetect()


        if detect:
            frame = model.detect(frame= frame, points= points)

    key = cv2.waitKey(5)
    if key == ord('q'):
        break
    elif key == ord('d'):
        points.append(points[0])
        detect = True

    # Hien anh ra man hinh
    cv2.imshow("Intrusion Warning", frame)

    cv2.setMouseCallback('Intrusion Warning', handle_left_click, points)

# video.stop()
cv2.destroyAllWindows()


# import cv2
# import numpy as np
# from imutils.video import VideoStream
# from yoloDetect import YoloDetect
#
# video = VideoStream(src=1).start()
# # Chua cac diem nguoi dung chon de tao da giac
# points = []
#
# # new model Yolo
# model = YoloDetect()
#
#
# def handle_left_click(event, x, y, flags, points):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         points.append([x, y])
#
#
# def draw_polygon (frame, points):
#     for point in points:
#         frame = cv2.circle( frame, (point[0], point[1]), 5, (0,0,255), -1)
#
#     frame = cv2.polylines(frame, [np.int32(points)], False, (255,0, 0), thickness=2)
#     return frame
#
# detect = False
#
# while True:
#     frame = video.read()
#     frame = cv2.flip(frame, 1)
#
#     # Ve ploygon
#     frame = draw_polygon(frame, points)
#     model = YoloDetect()
#
#     if detect:
#         frame = model.detect(frame= frame, points= points)
#
#     key = cv2.waitKey(1)
#     if key == ord('q'):
#         break
#     elif key == ord('d'):
#         points.append(points[0])
#         detect = True
#
#     # Hien anh ra man hinh
#     cv2.imshow("Intrusion Warning", frame)
#
#     cv2.setMouseCallback('Intrusion Warning', handle_left_click, points)
#
# video.stop()
# cv2.destroyAllWindows()
