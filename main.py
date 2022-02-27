import cv2
from cvzone.HandTrackingModule import HandDetector

from pynput.keyboard import Controller

from time import sleep

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "0", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

detector = HandDetector(detectionCon=0.8)
keyboard = Controller()

def drawALL(img, buttonList):

    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 25, y + 65),
        cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    return img

class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    print(len(hands))
    img = drawALL(img, buttonList)

    if hands:
        hand1 = hands[0]
        lmList = hand1["lmList"]
        bbox = hand1["bbox"]
        print("inside if")

        if lmList:

            print("yes")

            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 25, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                    l, _, _ = detector.findDistance(lmList[8], lmList[12], img)
                    print(l)

                    if l < 40:

                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 25, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                        sleep(0.15)




        else:
            print("no")



    cv2.imshow("Image", img)
    cv2.waitKey(1)