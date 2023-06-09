from threading import Thread
import cv2

class VideoStreamWidget(object):
    def __init__(self, src=0):
        # Create a VideoCapture object
        self.capture = cv2.VideoCapture(src)

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def show_frame(self):
        # Display frames in main program
        if self.status:
            self.frame = self.maintain_aspect_ratio_resize(self.frame, width=600)
            cv2.imshow('IP Camera Video Streaming', self.frame)
    def catch_fram(self,i):
        if self.status:
            self.frame = self.maintain_aspect_ratio_resize(self.frame, width=600)
            cv2.imwrite(f'feat_match{i}.jpg', self.frame)


    # Resizes a image and maintains aspect ratio
    def maintain_aspect_ratio_resize(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        # Grab the image size and initialize dimensions
        dim = None
        (h, w) = image.shape[:2]

        # Return original image if no need to resize
        if width is None and height is None:
            return image

        # We are resizing height if width is none
        if width is None:
            # Calculate the ratio of the height and construct the dimensions
            r = height / float(h)
            dim = (int(w * r), height)
        # We are resizing width if height is none
        else:
            # Calculate the ratio of the 0idth and construct the dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # Return the resized image
        return cv2.resize(image, dim, interpolation=inter)

if __name__ == '__main__':
    # stream_link = 'rtsp://192.168.0.150:554/type=1&id=1'
    # stream_link = 'rtsp://admin:INFRACHEN123@192.168.0.250:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif'
    # stream_link = 'feat_match/test2023-01-04-15-58-34.mp4'
    # stream_link = 'rtsp://admin:INFRACHEN123@192.168.0.250/Streaming/Channels/101'
    stream_link = 'rtsp://admin:qsc12345@192.168.0.179'
    video_stream_widget = VideoStreamWidget(stream_link)
    i = 0
    while True:
        try:
            video_stream_widget.show_frame()
            if cv2.waitKey(1) & 0xFF == ord('c'):
                video_stream_widget.catch_fram(i)    
            # Press Q on keyboard to stop recording
            if cv2.waitKey(1) & 0xFF == ord('q'):
                video_stream_widget.capture.release()
                cv2.destroyAllWindows()
                break
        except AttributeError:
            pass
        i +=1