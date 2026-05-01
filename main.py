from hbridge import MotorDriver, DriveTrain
from machine import Pin, Timer, SPI
from time import sleep
from imager import *
import gc

# --- Setup Motors ---
motor1 = MotorDriver(21, 20, 17)
motor2 = MotorDriver(18, 19, 16)
driver = DriveTrain(motor1, motor2, 14, 15)

TARGET_BALL = 0
NO_BALL = 1
DRIVE_FORWARD = 2
STOP = 3
driver_state = STOP


# --- Ball capture flag ---
capture_due = False

def set_capture_flag(timer):
    global capture_due
    capture_due = True

captureTimer = Timer(mode=Timer.PERIODIC, period=1000, callback=set_capture_flag)
nx = None
while True:
    if driver_state == TARGET_BALL:
        driver.steer(nx, 8000)
    elif driver_state == NO_BALL:
        driver.turnCW(8000)
    elif driver_state == DRIVE_FORWARD:
        driver.drive(0,8000)
    elif driver_state == STOP:
        driver.stop()
    if capture_due:
#         print("taking impag")
        capture_due = False
        nx = capture()
        if nx:
            driver_state = TARGET_BALL
        else:
            driver_state = STOP
    
    gc.collect()
