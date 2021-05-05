from djitellopy import tello
import cv2
import threading
import keyboard
import time
import sqlite3 as lite
import sys

def VideoFeed():
    while True:
        img = tello.get_frame_read().frame
        cv2.imshow("Live Stream", img)
        cv2.waitKey(1)

        if(keyboard.is_pressed('r') == True):
            tello.streamoff()
            sendToDB("streamoff")
            break

    cv2.destroyAllWindows()

def Controls(speed):
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
            tello.land()
            sendToDB("land")
            break

        tello.send_rc_control(a,b,c,d)
        sendToDB("rc {} {} {} {}".format(a,b,c,d))
        time.sleep(0.1)

def loggingToDB():
    DB_NAME = "mydatabase4.db"
    con = lite.connect(DB_NAME)
    cur = con.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS DroneData(Time DATETIME DEFAULT CURRENT_TIMESTAMP, Temperature INT, Height INT);
    CREATE TABLE IF NOT EXISTS Commands(Time DATETIME DEFAULT CURRENT_TIMESTAMP, Command TEXT);
    """)
    while True:
        height = tello.get_height()
        temp = tello.get_highest_temperature()

        cur.execute("INSERT INTO DroneData(Temperature, Height) VALUES (?, ?)",(temp, height))
        con.commit()
        time.sleep(1)

def sendToDB(insertThis):
    DB_NAME = "mydatabase4.db"
    con = lite.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("INSERT INTO Commands(Command) VALUES (?)",(insertThis,))
    con.commit()

tello = tello.Tello()
tello.connect()

tello.streamon()
sendToDB("streamon")
tello.takeoff()
sendToDB("takeoff")

videoThread = threading.Thread(target=VideoFeed)
videoThread.start()
controlThread = threading.Thread(target=Controls, args=(50,))
controlThread.start()
loggingThread = threading.Thread(target=loggingToDB)
loggingThread.start()
