import cv2

img = cv2.imread('Template_Matching_Original_Image.jpg',0)
img2 = img.copy()
template = cv2.imread('Template_Matching_Template_Image.jpg', 0)
w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
methodName = 'cv2.TM_CCOEFF_NORMED'

img = img2.copy()
method = eval(methodName)

# Apply template Matching
res = cv2.matchTemplate(img,template,method)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)

