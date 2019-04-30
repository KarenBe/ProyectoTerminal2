import cv2
import time
from videocaptureasync import VideoCaptureAsync

def test(n_frames=500, width=1280, height=720, asyncr=False):
    if asyncr:
        cap = VideoCaptureAsync(0)
        print("If async")
    else:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    if asyncr:
        cap.start()
    t0 = time.time()
    i = 0
    while i < n_frames:
        _, frame = cap.read()
        cv2.imshow('Frame', frame)
        cv2.waitKey(1) & 0xFF
        i += 1
        print('[i] Frames per second: {:.2f}, asyncr={}'.format(n_frames / (time.time() - t0), asyncr))
    #if asyncr:
     #   cap.stop()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    test(n_frames=20, width=1280, height=720, asyncr=True)