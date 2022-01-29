import numpy as np
import cv2 as cv
import time
from djitellopy import Tello 



dogi = Tello()
dogi.connect()
dogi.streamon()


prev_frame_time  = 0
# cap = cv.VideoCapture("http://192.168.1.20:8080/video")
# cap = cv.VideoCapture(0)


font = cv.FONT_HERSHEY_SIMPLEX 
cascade = cv.CascadeClassifier("haarFace.xml")



fbRange = [6200,6800]
pid = [0.6, 0.6, 0]
pError = 0
w, h = 360, 240


def findFace(img):
    gray = cv.cvtColor(img , cv.COLOR_BGR2GRAY)
    face_rect = cascade.detectMultiScale(gray , scaleFactor = 1.2 , minNeighbors = 8)

    facelistC = []
    facelistArea = []


    for(x,y,w,h) in face_rect:
        cv.rectangle(img , (x,y) , (x+w , y+h) , (0,255,0), thickness=2)
        cx = x + w // 2
        cy = y + h // 2

        area = w * h
        
        cv.circle(img,(cx,cy), 5, (0,255,0), cv.FILLED)
        facelistC.append([cx,cy])
        facelistArea.append(area)
    if len(facelistArea) != 0:
        i = facelistArea.index(max(facelistArea))
        return img, [facelistC[i], facelistArea[i]]
    else:
        return img, [[0,0],0]


def trackFace(me,info, w, pid, pError):
    area = info[1]
    x,y = info[0]
    fb = 0  

    error = x - w//2
    speed = pid[0]*error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))
   
    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    if area > fbRange[1]:
        fb =- 20
    elif area < fbRange[0] and area != 0:
        fb = 20

    if x == 0:
        speed = 0
        error = 0



    me.send_rc_control(0, fb, 0, speed)
    return error


while(True):
    # ret, img = cap.read()
    ##############
    frame = dogi.get_frame_read()
    img = frame.frame
    img = cv.resize(img,(w,h))
    img, info = findFace(img)
    pError = trackFace(dogi,info, w, pid, pError)
    # print("Area", info[1])

    ###################
    new_frame_time = time.time() 
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time  
    cv.putText(img, str(int(fps)), (7, 70), font, 3, (100, 255, 0), 3, cv.LINE_AA) 

    cv.imshow("detected face" , img)
    if cv.waitKey(1) & 0xFF == ord('w'):
        dogi.takeoff()

    if cv.waitKey(1) & 0xFF == ord('q'):
        dogi.land()
        dogi.streamoff()
        break




# cap.release()
cv.destroyAllWindows()