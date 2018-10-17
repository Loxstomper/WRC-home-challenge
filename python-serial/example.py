import cv2 as cv
import numpy as np

black = np.uint8([[[0,0,0 ]]])
hsv_black = cv.cvtColor(black,cv.COLOR_BGR2HSV)
print( hsv_black )