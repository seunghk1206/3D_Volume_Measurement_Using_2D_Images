import cv2
import numpy as np

img = cv2.imread("./project_4/processed_img/processed1.png")

img[0][0] = ['\0', '\0', '\0']
print(img[0][0])
while True:
    cv2.imshow("A", img)
    if cv2.waitKey(1) == 27:
        break