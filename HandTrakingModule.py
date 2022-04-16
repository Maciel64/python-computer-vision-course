from cmath import pi
from sre_constants import SUCCESS
import cv2, time
import mediapipe as mp


class HandDetector () :
    
    def __init__ (self, mode=False, maxHands=2, complexity=1, detectionCon=0.5, trackCon=0.5) :
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils


    def findHands (self, img, draw = True) :
        
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks :

            for handLmk in self.results.multi_hand_landmarks :
                
                if draw :
                    self.mpDraw.draw_landmarks(img, handLmk, self.mpHands.HAND_CONNECTIONS)
        
        return img

    
    def findPosition (self, img, handNumber=0, draw=True) :

        lmList = []

        if self.results.multi_hand_landmarks :
            hand = self.results.multi_hand_landmarks[handNumber]

            for id, lm in enumerate(hand.landmark) :
                
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                lmList.append([id, cx, cy])

                if draw :
                    cv2.putText(img, str(int(id)), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)

        return lmList


def main () :
    previousTime = 0
    currentTime = 0

    cap = cv2.VideoCapture(0)

    detector = HandDetector()

    while True :

        success, img = cap.read()

        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0 :
            pass
            # print(lmList)
    
        currentTime = time.time()
        fps = 1/(currentTime - previousTime)
        previousTime = currentTime
        

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)



if __name__ == "__main__" :
    main()