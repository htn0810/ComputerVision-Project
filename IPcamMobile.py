import cv2
import numpy as np
from yoloDetect import YoloDetect

points = []


def handle_left_click(event, x, y, flags, points):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])
detect = False

def draw_polygon (frame, points):
    for point in points:
        frame = cv2.circle( frame, (point[0], point[1]), 5, (0,0,255), -1)

    frame = cv2.polylines(frame, [np.int32(points)], False, (255,0, 0), thickness=2)
    return frame

class MobileCamera:
    def getVideo(self, camera):
        self.camera = camera
        cap = cv2.VideoCapture(self.camera)
        while True:
            ret, frame = cap.read()
            frame = draw_polygon(frame, points)
            model = YoloDetect()
            if detect:
                frame = model.detect(frame=frame, points=points)
            # cv2.imshow("mobile cam", frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('d'):
                points.append(points[0])
                detect = True
            cv2.imshow("Intrusion Warning", frame)

            cv2.setMouseCallback('Intrusion Warning', handle_left_click, points)

        cap.release()

        cv2.destroyAllWindows()


cam = MobileCamera()
cam.getVideo("https://192.168.1.5:8080/video")