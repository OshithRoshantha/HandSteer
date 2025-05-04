import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mpDrawing = mp.solutions.drawing_utils

screenWidth, screenHeight = pyautogui.size()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

centerRegion = 0.3  
movementThreshold = 0.2  

currentKey = None
lastKeyTime = time.time()
keyDelay = 0.2 

def isFist(handLandmarks):
    tips = [8, 12, 16, 20] 
    mcps = [5, 9, 13, 17]    
    
    closedFingers = 0
    for tip, base in zip(tips, mcps):
        if handLandmarks.landmark[tip].y > handLandmarks.landmark[base].y:
            closedFingers += 1
    
    return closedFingers >= 3  

def isOpenPalm(handLandmarks):
    tips = [8, 12, 16, 20]  
    mcps = [5, 9, 13, 17]     
    
    openFingers = 0
    for tip, base in zip(tips, mcps):
        if handLandmarks.landmark[tip].y < handLandmarks.landmark[base].y:
            openFingers += 1
    
    return openFingers >= 3  

def getHandPosition(handLandmarks, frameWidth):
    wristX = handLandmarks.landmark[0].x  
    normalizedX = (wristX - 0.5) * 2  
    return normalizedX

def pressKey(key):
    global currentKey, lastKeyTime
    
    if key != currentKey or (time.time() - lastKeyTime) > keyDelay:
        if currentKey:
            pyautogui.keyUp(currentKey)
        
        if key:
            pyautogui.keyDown(key)
        
        currentKey = key
        lastKeyTime = time.time()

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue
        
        frame = cv2.flip(frame, 1)
        frameRgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = hands.process(frameRgb)
        
        if results.multi_hand_landmarks:
            for handLandmarks in results.multi_hand_landmarks:
                mpDrawing.draw_landmarks(frame, handLandmarks, mpHands.HAND_CONNECTIONS)
                
                if isFist(handLandmarks):
                    pressKey('down')
                    cv2.putText(frame, "Brake", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                elif isOpenPalm(handLandmarks):
                    handPos = getHandPosition(handLandmarks, frame.shape[1])
                    
                    if abs(handPos) < centerRegion:
                        pressKey('up')
                        cv2.putText(frame, "Accelerate", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    elif handPos > movementThreshold:
                        pressKey('right')
                        cv2.putText(frame, "Steer Right", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    elif handPos < -movementThreshold:
                        pressKey('left')
                        cv2.putText(frame, "Steer Left", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                else:
                    pressKey(None)
        else:
            pressKey(None)
            cv2.putText(frame, "Ready? Show your hand to the camera!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv2.imshow('HandSteer', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    if currentKey:
        pyautogui.keyUp(currentKey)
