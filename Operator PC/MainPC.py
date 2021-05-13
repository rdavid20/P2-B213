from djitellopy import tello
import cv2
import threading
import keyboard
import time
import sqlite3 as lite
import sys

def VideoFeed():
    cv2.namedWindow('window')

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (600, 15)
    fontScale = 0.5
    color = (255, 255, 255)
    thickness = 1

    while True:
        img = tello.get_frame_read().frame
        img = cv2.resize(img, (720,480))
        string = 'Battery: {}%'.format(tello.get_battery())
        img = cv2.putText(img, string, org, font,
        				fontScale, color, thickness, cv2.LINE_AA)
        cv2.imshow("window", img)
        key = cv2.waitKey(3)
        if key == 27:
            break

        if(keyboard.is_pressed('r') == True):
            tello.streamoff()
            sendToDB("streamoff")
            break

    cv2.destroyAllWindows()
    quit()

def Controls(speed):
    landed = True
    while True:
        a = 0
        b = 0
        c = 0
        d = 0

        if(keyboard.is_pressed('w') == True):
            b+= speed

        if(keyboard.is_pressed('a') == True):
            a+= -speed

        if(keyboard.is_pressed('s') == True):
            b+= -speed

        if(keyboard.is_pressed('d') == True):
            a+= speed

        if(keyboard.is_pressed('up arrow') == True):
            c+= speed

        if(keyboard.is_pressed('down arrow') == True):
            c+= -speed

        if(keyboard.is_pressed('right arrow') == True):
            d+= speed

        if(keyboard.is_pressed('left arrow') == True):
            d+= -speed

        if(keyboard.is_pressed("space") == True):
            if(landed == False):
                try:
                    tello.land()
                    sendToDB("land")
                    landed = True
                    time.sleep(4)
                except:
                    print("Error: Landing failed")
            if(landed == True):
                try:
                    tello.takeoff()
                    sendToDB("takeoff")
                    landed = False
                except:
                    print("Error: Takeoff failed")

        if(landed == False):
            tello.send_rc_control(a,b,c,d)
            sendToDB("rc {} {} {} {}".format(a,b,c,d))
        time.sleep(0.1)

def createDB():
    DB_NAME = "mydatabase4.db"
    con = lite.connect(DB_NAME)
    cur = con.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS DroneData(Time DATETIME DEFAULT CURRENT_TIMESTAMP, Temperature INT, Height INT);
    CREATE TABLE IF NOT EXISTS Commands(Time DATETIME DEFAULT CURRENT_TIMESTAMP, Command TEXT);
    """)
    con.commit()
    con.close()

def loggingToDB():
    DB_NAME = "mydatabase4.db"
    con = lite.connect(DB_NAME)
    cur = con.cursor()
    while True:
        height = tello.get_height()
        temp = tello.get_highest_temperature()

        cur.execute("INSERT INTO DroneData(Temperature, Height) VALUES (?, ?)",(temp, height))
        con.commit()
        time.sleep(1)
    con.close()

def sendToDB(insertThis):
    DB_NAME = "mydatabase4.db"
    con = lite.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("INSERT INTO Commands(Command) VALUES (?)",(insertThis,))
    con.commit()
    con.close()

tello = tello.Tello()
tello.connect()
createDB()
tello.streamon()
sendToDB("streamon")

videoThread = threading.Thread(target=VideoFeed)
videoThread.start()
controlThread = threading.Thread(target=Controls, args=(50,))
controlThread.start()
loggingThread = threading.Thread(target=loggingToDB)
loggingThread.start()
