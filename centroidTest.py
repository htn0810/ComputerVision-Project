import cv2
img = cv2.imread("shape.png")
width = int(img.shape[1]*0.6)
height = int(img.shape[0]*0.6)
img = cv2.resize(img,(width, height),interpolation=cv2.INTER_AREA)
index = 0
while True:
    img_blur = cv2.blur(img, (3,3))
    img_canny = cv2.Canny(img_blur, 100, 150)
    img_dil = cv2.dilate(img_canny, (7,7), iterations=1)
    cv2.imshow("CardCany", img_dil)

    contours, _ = cv2.findContours(img_dil, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >=300:
            index+=1
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x + w, y + h), (200, 0, 0), 2)
            centroid = (int(x+w/2), int(y+h/2))
            cv2.circle(img, centroid, 5, (0,0,255), -1)
    cv2.imshow("Card", img)
    key = cv2.waitKey(0)
    if key == ord("q"):
        break
cv2.destroyAllWindows()

