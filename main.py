import cv2
import time
import glob
import os
from sendmail import send_email
from threading import Thread

# Video Capture

video = cv2.VideoCapture(0)
time.sleep(1)

count = 0
firstframe = None
statuslist = []

def cleanfolder():
     print('Clean Folder started')
     images = glob.glob('images/*.png')
     for image in images:
          os.remove(image)
     print('Clean folder func ended')


while True:
    status = 0
    check, frame = video.read()
    
    # Conversion of video to grayscale to save data (PREPROCESSING)

    grayframes = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayframes_gau = cv2.GaussianBlur(grayframes, (21,21), 0)
    

    if firstframe is None:
        firstframe = grayframes_gau
    framesdiff = cv2.absdiff(firstframe, grayframes_gau)

    threshframe = cv2.threshold(framesdiff, 90, 255, cv2.THRESH_BINARY)[1]
    dilframe = cv2.dilate(threshframe, None, iterations=2)
    
    # Drawing rectangle around new object in frame

    contours, check = cv2.findContours(dilframe, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rect = cv2.rectangle(frame, pt1=(x, y), pt2=(x+w, y+h), color=(0, 255, 0), thickness= 3)

# Sending email when object exits the view

        if rect.any():
            status = 1

            # Taking middle picture of the time obj is in frame

            cv2.imwrite(f'images/{count}.png', frame)
            count = count+1
            all_img = glob.glob('images/*.png')
            index = int(len(all_img)/2)
            sentimg = all_img[index]

    statuslist.append(status)
    statuslist = statuslist[-2:]     

    # Threading for Email and Clean functions

    if statuslist[0] == 1 and statuslist[1] == 0:
            emailthread = Thread(target=send_email, args=(sentimg, ))
            emailthread.daemon = True
            cleanthread = Thread(target=cleanfolder)
            cleanthread.daemon = True

            emailthread.start()
            cleanthread.start()

    print(statuslist)
            

    cv2.imshow('Vid', frame)
    # Quitting the program

    key = cv2.waitKey(1)

    if key== ord('q'):
        break

video.release()


