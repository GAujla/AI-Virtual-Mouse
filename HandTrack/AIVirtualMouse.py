import cv2
import numpy as np
import HandTrackModule as htm
import time
import autopy
import pyautogui



wCam, hCam = 640, 480
frameR = 100
smoothening = 5

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
plocX, plocY = 0,0
clocX, clocY = 0,0

detector = htm.handDetector(maxHands=1)
wScr, hScr = 1280, 800
print(wScr, hScr)

while True:
    # 1. Find HandLandMarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # 2. Get the tip of the index and middle fingers
    if len(lmList)!=0:
        x1, y1 = lmList[8][1:]
        #x2, y2 = lmList[12][1:]

        x5, y5 = lmList[4][1:]

        #print(x1, y1, x2, y2)
        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)
        # 4. Only Index Finger : Moving Mode
        if fingers[1] == 1:
        # 5. Convert Coordinates

            x3 = np.interp(x1, (frameR,wCam-frameR),(0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
        # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

        # 7. Move Mouse
            autopy.mouse.move(wScr-clocX,clocY)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocX, plocY = clocX, clocY
        # 8. Both Index and middle fingers are up : Clicking Node
        if fingers[1] == 1 and fingers[2] == 1:
            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8,12,img)

            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)

                pyautogui.leftClick()

                #autopy.mouse.click()
        if fingers[1] == 1 and fingers[4] == 1:
            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8,20,img)

            if length < 100:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)

                pyautogui.rightClick()







    # 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0),3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)

