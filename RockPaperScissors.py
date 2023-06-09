import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

def Scissor():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    detector = HandDetector(maxHands=1)

    timer = 0
    stateResult = False
    startGame = False
    scores = [0, 0]  # [AI, Player]


    while True:
        imgBG = cv2.imread("Resources/BG.png")
        success, img = cap.read()

        imgScaled = cv2.resize(img,(0,0),None,0.64583,0.64583)
        imgScaled = imgScaled[:,58:355]

        # Find Hands
        hands, img = detector.findHands(imgScaled)  # with draw

        if startGame:

            if stateResult is False:
                timer = time.time() - initialTime
                cv2.putText(imgBG, str(int(timer)), (446,335), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

                if timer>3:
                    stateResult = True
                    timer = 0

                    if hands:
                        hand = hands[0]
                        fingers = detector.fingersUp(hand)
                        print(fingers)
                        if fingers == [0,0,0,0,0]:
                            playerMove = 1
                        if fingers == [1,1,1,1,1]:
                            playerMove = 2
                        if fingers == [0,1,1,0,0]:
                            playerMove = 3

                        randomNumber = random.randint(1,3)
                        imgAI = cv2.imread(f'Resources/{randomNumber}.png',cv2.IMREAD_UNCHANGED)
                        imgBG = cvzone.overlayPNG(imgBG, imgAI, (70, 175))

                        # Player wins
                        if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                            scores[1] += 1

                        # AI wins
                        if (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3) or \
                            (playerMove == 3 and randomNumber == 1):
                            scores[0] += 1

                        print(playerMove)


        imgBG[176:486,594:891] = imgScaled

        if stateResult:
            imgBG = cvzone.overlayPNG(imgBG, imgAI, (70, 175))

        cv2.putText(imgBG, str(scores[0]), (307, 161), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
        cv2.putText(imgBG, str(scores[1]), (833, 161), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)

        # cv2.imshow("Image",img)
        cv2.imshow("BG",imgBG)
        # cv2.imshow("Scaled",imgScaled)


        key = cv2.waitKey(1)
        if key == ord('s'):
            startGame = True
            initialTime = time.time()
            stateResult = False

        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

