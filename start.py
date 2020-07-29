from PyQt5.QtWidgets import QMainWindow,QApplication,QPushButton,QProgressBar,QLabel,QVBoxLayout,QHBoxLayout,QGroupBox,QDialog,QGridLayout
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import pygame

import cv2
import numpy as np
import os

import DetectChars
import DetectPlates
import PossiblePlate
import FireDatabase

SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

licPlateNumber="N/A"
status=0

def main():
    imgOriginalScene  = cv2.imread("LicPlateImages/1.jpg")
#    imgOriginalScene = cv2.resize(imgOriginalScene,(1400,1230))	
    if imgOriginalScene is None:
        print("\nerror: image not read from file \n\n")
        os.system("pause")
        return

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)

#    cv2.imshow("imgOriginalScene", imgOriginalScene)

    if len(listOfPossiblePlates) == 0:
        print("\nno license plates were detected\n")
    else:

        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)
        licPlate = listOfPossiblePlates[0]

#        cv2.imshow("imgPlate", licPlate.imgPlate)
#        cv2.imshow("imgThresh", licPlate.imgThresh)

        if len(licPlate.strChars) == 0:
            print("\nno characters were detected\n\n")
            return

        global licPlateNumber
        licPlateNumber = finalPolish(licPlate.strChars)
        print("\nlicense plate read from image = " + licPlateNumber + "\n")
        print("----------------------------------------")



        cv2.imwrite("imgOriginalScene.png", imgOriginalScene)
        databaseconstant = FireDatabase.retrieve(licPlateNumber)
        if(databaseconstant==None):
            print("The Vehicle has not been booked for any parking space in this parking station: ACCESS DENIED")
        else:
            eoe = FireDatabase.checkforentryorexit(licPlateNumber)
            if(eoe==None):
                print("The Vehicle has not been booked for any parking space in this parking station: ACCESS DENIED")
                global status
                status=-1
            elif(eoe=='entry'):
                print("**********Access Granted**********")
                status=1
            elif(eoe=='exit'):
                print('**********Drive Safely**********')
                status=0
    return
def finalPolish(number):
    lst = []
    string = number
    if(len(number)<=4):
        string = 'BAA' + number
        finalPolish(string)
    if (len(number)==7):
        for i in range(7):
            lst.append(number[i])
        for i in range(3):
            if(ord(lst[i])>=65 and ord(lst[i])<=90):
                continue
            elif (lst[i] == '4'):
                lst[i]='A'
            elif lst[i] == '8':
                lst[i]='B'
            elif(lst[i]=='1'):
                lst[i]='L'
            elif(lst[i]=='6'):
                lst[i]='B'
            
            else:
                continue
        for i in range(3,7):
            if(ord(lst[i])>=48 and ord(lst[i])<=57):
                continue
            elif (lst[i]=='G'):
                lst[i]='0'
            elif(lst[i]=='A'):
                lst[i]='1'
            elif(lst[i]=='H'):
                lst[i]='1'
            elif(lst[i]=='C'):
                lst[i]='6'

            else:
                continue
        string=''.join(lst)
        print(string)
    return string


pygame.init()
pygame.mixer.music.load('sound/music.mp3')
pygame.mixer.music.play(-1)

class Window(QMainWindow,QLabel):
    def __init__(self):
        super().__init__()
        self.title="Automated Parking System"
        self.icon="win.ico"
        self.InitWindow()
        

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.setStyleSheet("QMainWindow{background-image:url(image/bg.jpg)}")
        self.setFixedSize(1024,768)
        self.UIcomponents()
        self.show()

    def UIcomponents(self):
        startbtn=QPushButton("START",self)
        startbtn.move(450,160)
        startbtn.setFixedSize(150,50)
        startbtn.setIcon(QtGui.QIcon("image/start.ico"))
        startbtn.setStyleSheet("QPushButton{color:white;background-color:brown;border-radius:25px;border: 8px solid white;font: bold}"
        "QPushButton:pressed{color:black;background-color:green}")
        startbtn.clicked.connect(self.start)

        recordbtn=QPushButton("LATEST RECORD",self)
        recordbtn.move(450,260)
        recordbtn.setFixedSize(150,50)
        recordbtn.setIcon(QtGui.QIcon("image/record.ico"))
        recordbtn.setStyleSheet("QPushButton{color:white;background-color:brown;border-radius:25px;border: 8px solid white;font: bold}"
        "QPushButton:pressed{color:black;background-color:green}")
        recordbtn.clicked.connect(self.record)

        feedbackbtn=QPushButton("CHECK BOOKINGS",self)
        feedbackbtn.move(450,360)
        feedbackbtn.setFixedSize(150,50)
        feedbackbtn.setIcon(QtGui.QIcon("image/bookings.png"))
        feedbackbtn.setStyleSheet("QPushButton{color:white;background-color:brown;border-radius:25px;border: 8px solid white;font: bold}"
        "QPushButton:pressed{color:black;background-color:green}")
        feedbackbtn.clicked.connect(self.bookings)

        teambtn=QPushButton("PROJECT TEAM",self)
        teambtn.move(450,460)
        teambtn.setFixedSize(150,50)
        teambtn.setIcon(QtGui.QIcon("image/team.png"))
        teambtn.setStyleSheet("QPushButton{color:white;background-color:brown;border-radius:25px;border: 8px solid white;font: bold}"
        "QPushButton:pressed{color:black;background-color:green}")

        exitbtn=QPushButton("EXIT",self)
        exitbtn.move(450,560)
        exitbtn.setFixedSize(150,50)
        exitbtn.clicked.connect(self.close)
        exitbtn.setIcon(QtGui.QIcon("image/exit.png"))
        exitbtn.setStyleSheet("QPushButton{color:white;background-color:brown;border-radius:25px;border: 8px solid white;font: bold}"
        "QPushButton:pressed{color:black;background-color:green}")

        mutebtn=QPushButton("",self)
        mutebtn.setIcon(QtGui.QIcon("image/mute.png"))
        mutebtn.move(980,670)
        mutebtn.setFixedSize(35,30)
        mutebtn.clicked.connect(self.off)
        mutebtn.setStyleSheet("QPushButton{color:white;background-color:white;border-radius:25px;border: none}"
        "QPushButton:pressed{color:black;background-color:green}")

        musicbtn=QPushButton("",self)
        musicbtn.setIcon(QtGui.QIcon("image/music.png"))
        musicbtn.move(10,670)
        musicbtn.setFixedSize(35,30)
        musicbtn.clicked.connect(self.on)
        musicbtn.setStyleSheet("QPushButton{color:white;background-color:white;border-radius:25px;border: none}"
        "QPushButton:pressed{color:black;background-color:green}")

    def start(self):
        self.progress = QProgressBar(self)
        self.progress.setGeometry(345, 300, 400, 100)
        self.progress.setStyleSheet("QProgressBar{color:white;font-size:30px}")
        self.completed = 0
        self.progress.show()

        while self.completed < 50:
            self.completed += 0.0001
            self.progress.setValue(self.completed)
            self.progress.show()
        
        main()
        
        while self.completed < 100:
            self.completed += 0.0001
            self.progress.setValue(self.completed)
            self.progress.show()
        
        self.progress.hide()
        self.m=Message()
        self.m.show()
        
    def close(self):
        sys.exit()
    
    def bookings(self):
        self.f=Feedback()
        self.f.show()
    
    def off(self):
        pygame.mixer.music.stop()
    
    def on(self):
        pygame.mixer.music.play()
    
    def record(self):
        self.r=Records()
        self.r.show()
        #print(licPlateNumber)
        
class Records(QLabel,QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("image/record.ico"))
        self.setWindowTitle("Latest Record")
        self.setFixedSize(400,100)
        vbox=QVBoxLayout()
        record=QLabel("Latest Number Plate : "+ licPlateNumber)
        record.setFont(QtGui.QFont("Sanserif",18))
        vbox.addWidget(record)
        self.setLayout(vbox)
            
class Feedback(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Feedback")
        self.setWindowIcon(QtGui.QIcon("image/feedback.png"))
        self.setGeometry(500,400,400,100)
        self.setStyleSheet("QDialog{}")
        self.createlayout()
        vbox=QVBoxLayout()
        vbox.addWidget(self.groupBox)
        self.setLayout(vbox)
    
    def createlayout(self):
        self.groupBox=QGroupBox("How was your experience ?")
        gridlayout=QGridLayout()

        badbtn=QPushButton("Bad",self)
        badbtn.setMinimumHeight(40)
        badbtn.clicked.connect(exit)
        gridlayout.addWidget(badbtn,0,0)

        satisfybtn=QPushButton("Satisfying",self)
        satisfybtn.setMinimumHeight(40)
        satisfybtn.clicked.connect(exit)
        gridlayout.addWidget(satisfybtn,0,1)

        goodbtn=QPushButton("Good",self)
        goodbtn.setMinimumHeight(40)
        goodbtn.clicked.connect(exit)
        gridlayout.addWidget(goodbtn,1,0)

        exgood=QPushButton("Extremely Good",self)
        exgood.setMinimumHeight(40)
        exgood.clicked.connect(exit)
        gridlayout.addWidget(exgood,1,1)

        self.groupBox.setLayout(gridlayout)

class Message(QLabel,QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("image/alert.ico"))
        self.setWindowTitle("Alert")
        self.setFixedSize(400,100)
        vbox=QVBoxLayout()
        global status
        if(status==1):
            record=QLabel("*******Access Granted*******")
        elif(status==0):
            record=QLabel("*********Drive Safely*********")
            global licPlateNumber
            licPlateNumber="N/A"
        elif(status==-1):
            record=QLabel("Denied:Unbooked Vehicle")
            licPlateNumber="N/A"
        
        record.setFont(QtGui.QFont("Sanserif",18))

        vbox.addWidget(record)
        self.setLayout(vbox)

App=QApplication(sys.argv)
window=Window()
sys.exit(App.exec())
