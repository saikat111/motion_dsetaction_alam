import cv2
import numpy as np
count = 0
from pyfirmata import Arduino
import  time
from playsound import playsound
board = Arduino("COM3")
cap = cv2.VideoCapture(0)
ret,frame1 =cap.read()
ret,frame2 =cap.read()
def arduin_o():
    board.digital[13].write(1)
    time.sleep(1)
    board.digital[13].write(0)
    


# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    diff = cv2.absdiff(frame1,frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur , 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours,_ = cv2.findContours(dilated, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        
        if cv2.contourArea(contour) <700:
            continue
        cv2.rectangle(frame1, (x,y), (x+y, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format('Movement'), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0,255) ,3)
        #when we need to count the frame
        count = count + 1
        print(count)
        if count>12:
            arduin_o()
            count = count - count
            playsound('alame.mp3')
            
    #cv2.drawContours(frame1,contours, -1, (0, 255, 0), 2)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()