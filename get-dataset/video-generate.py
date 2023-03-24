import cv2
import os
import time
from threading import Timer

# channel=1 for infray
# channel=0 for rgb
vcap = cv2.VideoCapture("cable_video/output-2022-11-16-17-09-27.mp4")
## rtsp://192.168.0.177:9554/live?channel=0&subtype=0
## rtsp://admin:148575@192.168.0.106:554/live/profile.0
## rtsp://admin:INFRACHEN123@192.168.0.17/Streaming/Channels/101
## rtsp://192.168.0.200:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif
cv2.namedWindow("test", cv2.WINDOW_)

width  = vcap.get(3)  # float `width`
height = vcap.get(4)  # float `height`
print(f'({width*0.6},{height*0.6})')

if (vcap.isOpened()== False): 
  print("Error opening video stream or file")
 
img_counter = 0
dirname = "./video_dataset"
total = 0 
# Read until video is completed
while(vcap.isOpened()):
    # Capture frame-by-frame
    ret, frame = vcap.read()
    if ret == True:
        # frame = cv2.resize(frame,(int(width*0.6),int(height*0.6)))
        # Display the resulting frame
        cv2.imshow('Frame',frame)
        cv2.waitKey(30)
    
        # Press Q on keyboard to  exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        elif cv2.waitKey(1) & 0xFF == 32:
            # SPACE pressed
            # total = 5
            # while total>0:
            #     print("{} second left".format(total))
            #     time.sleep(1)
            #     total -= 1
            # t = Timer(5 , show_image(vcap))
            # t.start()
            img_name = "cable_{}.png".format(img_counter)
            path = os.path.join(dirname, img_name)
            while os.path.isfile(path=path):
                img_counter += 1
                img_name = "cable_{}.png".format(img_counter)
                path = os.path.join(dirname, img_name)
            cv2.imwrite(path, frame)
            print("{} written!".format(img_name))
            img_counter += 1
            # print("take picture")
    # Break the loop
    else: 
        break
    total += 1
 
# When everything done, release the video capture object
vcap.release()
 
# Closes all the frames
cv2.destroyAllWindows()

# img_counter = 0
# dirname = "./video_dataset"
# print()
# def show_image(vcap):
#     ret, frame = vcap.read()
#     resize = cv2.resize(frame, (int(width*0.6),int(height*0.6)))
#     cv2.imshow("test", resize)
#     cv2.waitKey(30)
#     return ret, resize

# total = 0
# ret = True
# while ret:
#     total += 1
#     ret, resize = show_image(vcap)
#     k = cv2.waitKey(1)
    
#     if k%256 == 27:
#         # ESC pressed
#         print("Escape hit, closing...")
#         break
#     elif k%256 == 32:
#     # elif total % 180 == 0:
#         # SPACE pressed
#         # total = 5
#         # while total>0:
#         #     print("{} second left".format(total))
#         #     time.sleep(1)
#         #     total -= 1
#         # t = Timer(5 , show_image(vcap))
#         # t.start()
#         img_name = "cable_{}.png".format(img_counter)
#         path = os.path.join(dirname, img_name)
#         cv2.imwrite(path, resize)
#         print("{} written!".format(img_name))
#         img_counter += 1

# vcap.release()

# cv2.destroyAllWindows()