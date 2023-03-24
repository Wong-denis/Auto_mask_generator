from multiprocessing import Process, Queue
import cv2

def image_save(taskqueue, width, height, fps):

    # 指定影片編碼
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #fourcc = cv2.VideoWriter_fourcc(*'H264')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # 建立 VideoWriter 物件
    writer = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

    while True:
        # 從工作佇列取得影像
        image = taskqueue.get()

        # 若沒有影像則終止迴圈
        if image is None: break

        # 儲存影像
        writer.write(image)

    # 釋放資源
    writer.release()

if __name__ == '__main__':

    # 開啟 RTSP 串流
    vidCap = cv2.VideoCapture('rtsp://ipcam.stream:8554/bars')
    if vidCap.isOpened()

    # 取得影像的尺寸大小
    width = int(vidCap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidCap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 取得影格率
    fps = vidCap.get(cv2.CAP_PROP_FPS)

    # 建立工作佇列
    taskqueue = Queue()

    # 建立並執行工作行程
    proc = Process(target=image_save, args=(taskqueue, width, height, fps))
    proc.start()

    # 計數器
    frame_counter = 0

    # 總錄製幀數（10 秒鐘）
    total_frames = fps * 10

    while frame_counter < total_frames:
        # 從 RTSP 串流讀取一張影像
        ret, image = vidCap.read()

        if ret:
            # 將影像放入工作佇列
            taskqueue.put(image)
            frame_counter += 1
        else:
            # 若沒有影像跳出迴圈
            break

    # 傳入 None 終止工作行程
    taskqueue.put(None)

    # 等待工作行程結束
    proc.join()

    # 釋放資源
    vidCap.release()