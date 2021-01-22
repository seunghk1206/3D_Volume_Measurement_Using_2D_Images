import math
import cv2
import numpy as np
from PIL import Image
def cornerDetection(file_name, quality):
    img = cv2.imread(file_name) 
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    corners = cv2.goodFeaturesToTrack(gray_img, 300, quality, 10) 
    corners = np.int0(corners) 
    #copyright, GeeksforGeeks @hachiman_20
    return corners
def unneededGrabCut(rotated, corners):
    return rotated
def imageRotation(directory, a, b):
    colorImage = Image.open(directory)
    slope = ((a[0]-b[0])/(a[1]-b[1]))
    angle = math.atan(slope)
    rotated = colorImage.rotate(angle)
    # Display the Original Image

    colorImage.show()

    # Display the Image rotated by 45 degrees

    rotated.show()
    print(cornerDetection(rotated, 0.07))
    return unneededGrabCut(rotated, cornerDetection(rotated, 0.07))

imageRotation("processed_img/processed25.png", [616, 69], [301, 75])