import cv2
import numpy as np
import json

COCO_FILE_PATH = 'coco_json/annot_template_coco.json'
file = open(COCO_FILE_PATH)
data = json.load(file)
seg = data["annotations"][0]["segmentation"][0]
print(type(seg[0]))
print(type(seg))


# img = cv2.imread("cable_47.png")
# gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# resize = cv2.resize(gray_img, (20,20))
# # print(resize)
# canny = cv2.Canny(resize,50,100)
# print(canny)
# if (canny>10).any():
#     print("++++++++++++++")
# blur_can = cv2.GaussianBlur(canny, (3, 3), 0)
# # print(blur_can)

# # canny = float(canny)
# # canny = canny.astype(float)
# # print(canny)
# resize = resize - canny*20/255
# resize[resize<0] = 0
# resize = resize.astype(np.uint8)
# # print(resize)
# # print(type(resize[0,0]))
# contours, hierarchy = cv2.findContours(resize, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
