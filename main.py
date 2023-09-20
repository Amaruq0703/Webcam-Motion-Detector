import cv2
import time

# Video Capture

video = cv2.VideoCapture(0)
time.sleep(1)

while True:
    check, frame = video.read()
    
    # Conversion of video to grayscale to save data (PREPROCESSING)

    grayframes = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayframes_gau = cv2.GaussianBlur(grayframes, (21,21), 0)
    cv2.imshow('Vid', grayframes_gau)

    # Quitting the program

    key = cv2.waitKey(1)

    if key== ord('q'):
        break


