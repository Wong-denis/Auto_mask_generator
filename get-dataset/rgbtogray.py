import cv2
import os

print("hihi")
for filename in os.listdir("./dataset"):
    image = cv2.imread(filename)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    namelist = filename.split(".")
    new_name = namelist[0]+"_g."+namelist[1]
    