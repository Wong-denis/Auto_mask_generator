from multiprocessing import Process, Queue
import cv2
from datetime import datetime
import numpy as np

def image_save(taskqueue, width, height, fps, frames_per_file):

    # 指定影片編碼
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #fourcc = cv2.VideoWriter_fourcc(*'H264')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    writer = None

    while True:
        # 從工作佇列取得影像
        image, frame_counter = taskqueue.get()

        # 若沒有影像則終止迴圈
        if image is None: break

        if frame_counter % frames_per_file == 0:
            
            if writer: writer.release()

            # 建立 VideoWriter 物件（以數字編號）
            # index = int(frame_counter // frames_per_file)
            # writer = cv2.VideoWriter(f'output-{index}.mp4', fourcc, fps, (width, height))

            # 建立 VideoWriter 物件（以時間命名）
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
            writer = cv2.VideoWriter(f'rtsp_video/test{timestamp}.mp4', fourcc, fps, (width, height))

    #     儲存影像
        writer.write(image)

    # 釋放資源
    writer.release()

if __name__ == '__main__':
    # pause for 1 seconds
    cv2.waitKey(2000)

    # 開啟 RTSP 串流
    # rtsp://:@192.168.0.177:9554/live?channel=0&subtype=0
    # rtsp://admin:INFRACHEN123@192.168.0.17/Streaming/Channels/101
    # vidCap = cv2.VideoCapture('rtsp://admin:INFRACHEN123@192.168.0.17/Streaming/Channels/101')
    # rtsp://192.168.0.200:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif
    # rtsp://admin:INFRACHEN123@192.168.0.250:554/live?channel=0&subtype=0
    # rtsp://admin:INFRACHEN123@192.168.0.250/Streaming/Channels/101
    vidCap = cv2.VideoCapture('rtsp://admin:qsc12345@192.168.0.179')
    # vidCap = cv2.VideoCapture('cable_video/real-test-2022-12-21-17-34-35.mp4')
    # 取得影像的尺寸大小
    width = int(vidCap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidCap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 取得影格率
    # fps = vidCap.get(cv2.CAP_PROP_FPS)
    fps = 30

    # 建立工作佇列
    taskqueue = Queue()

    # 計數器
    frame_counter = 0

    # 總錄製幀數（30 秒鐘）
    total_frames = fps * 16

    # 每個檔案的幀數（10 秒鐘）
    frames_per_file = fps * 8

    # 建立並執行工作行程
    proc = Process(target=image_save, args=(taskqueue, width, height, fps, frames_per_file))
    proc.start()
    print("start recording!!!")
    while frame_counter < total_frames:
        # 從 RTSP 串流讀取一張影像
        ret, image = vidCap.read()

        if ret:
            # image = cv2.resize(image,(360,360), interpolation=cv2.INTER_AREA)

            # 將影像放入工作佇列
            taskqueue.put((image, frame_counter))
            
            cv2.imshow("window",image)
            cv2.waitKey(20)
        
            frame_counter += 1
        else:
            # 若沒有影像跳出迴圈
            break

    # 傳入 None 終止工作行程
    taskqueue.put((None, None))

    # 等待工作行程結束
    proc.join()

    # 釋放資源
    vidCap.release()