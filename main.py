import cv2
import time
from sendmail import send_email

# Video Capture

video = cv2.VideoCapture(0)
time.sleep(1)


firstframe = None
statuslist = []
while True:
    status = 0
    check, frame = video.read()
    
    # Conversion of video to grayscale to save data (PREPROCESSING)

    grayframes = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayframes_gau = cv2.GaussianBlur(grayframes, (21,21), 0)
    

    if firstframe is None:
        firstframe = grayframes_gau
    framesdiff = cv2.absdiff(firstframe, grayframes_gau)

    threshframe = cv2.threshold(framesdiff, 50, 255, cv2.THRESH_BINARY)[1]
    dilframe = cv2.dilate(threshframe, None, iterations=2)
    
    # Drawing rectangle around new object in frame

    contours, check = cv2.findContours(dilframe, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) < 7000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rect = cv2.rectangle(frame, pt1=(x, y), pt2=(x+w, y+h), color=(0, 255, 0), thickness= 3)

# Sending email when object exits the view

        if rect.any():
            status = 1

    statuslist.append(status)
    statuslist = statuslist[-2:]     

    if statuslist[0] == 1 and statuslist[1] == 0:
            send_email('Subject: Object Detected')

    print(statuslist)
            

    cv2.imshow('Vid', frame)
    # Quitting the program

    key = cv2.waitKey(1)

    if key== ord('q'):
        break


