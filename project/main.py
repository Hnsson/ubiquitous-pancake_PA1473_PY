#!/usr/bin/env pybricks-micropython
import sys
import __init__
from pybricks import robotics
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor, TouchSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.messaging import BluetoothMailboxClient, TextMailbox, LogicMailbox, NumericMailbox
import time

ev3 = EV3Brick()

positive_direction = Direction.COUNTERCLOCKWISE
crane_positive_direction = Direction.CLOCKWISE
gears = [12, 20]
craneGears = [16, 36]

Left_drive=Motor(Port.C, positive_direction, gears) 
Right_drive=Motor(Port.B, positive_direction, gears)
Crane_motor=Motor(Port.A, crane_positive_direction, craneGears)

Front_button=TouchSensor(Port.S1)

Light_sensor=ColorSensor(Port.S3)

Ultrasonic_sensor=UltrasonicSensor(Port.S4)

robot = DriveBase(Left_drive, Right_drive, wheel_diameter = 47, axle_track = 128)

# Constants
COLOR_BLUE = 2
COLOR_GREEN = 3
COLOR_YELLOW = 4
COLOR_RED = 5
COLOR_BROWN = 7
COLLISION_DISTANCE = 300
SPEED_MULTIPLIER = 0.4
TURN_MULTIPLIER = 3.2

DRIVE_SPEED = 50
PROPORTIONAL_GAIN = 0.6
DEFAULT_RANGE = range(50, 70)
currentColor = Color.GREEN


def isColliding(distance:int = COLLISION_DISTANCE):
    # print(Ultrasonic_sensor.distance())
    return bool(Ultrasonic_sensor.distance() <= distance)

def collision():
    colliding = isColliding()
    while colliding:
        robot.stop()

# Välj en destination. Den kör på vägen beroende på vilken den är. Sedan när den är i rondellen kör den hela tiden tills den hittar destination och
# sedan går över till navRoad för destination.


def roundabout(destination):
    GREEN = 24
    WHITE = 85
    threshold = (GREEN + WHITE) / 2

    while currentColor == Color.GREEN:
        collision()

        # Calculate the deviation from the threshold.§
        deviation = Light_sensor.reflection() - threshold

        # Calculate the turn rate.
        turn_rate = PROPORTIONAL_GAIN * deviation

        # Set the drive base speed and turn rate.
        robot.drive(DRIVE_SPEED, turn_rate)

        # You can wait for a short time or do other things in this loop.
        wait(10)

        #Kanske kolla mailbox som man skickar till och sedan ändrar currentColor för att gå  till anting findBlueWarehouse eller röd
        if Light_sensor.color() == destination:
            robot.stop()



def get_turn_rate():
    optimal = range(50, 70)
    drive = Light_sensor.reflection()
    #alltid svänga höger

    threshold = (13 + 84) / 2
    # Calculate the deviation from the threshold.
    deviation = Light_sensor.reflection() - threshold

    if drive in optimal:
        turn_rate = PROPORTIONAL_GAIN * deviation * 1
        return turn_rate
    else:
        turn_rate = PROPORTIONAL_GAIN * deviation * -1
        return turn_rate


# Crane_motor.run_angle(180, 120, then=Stop.HOLD, wait=True)
currentDestination = []
currentDestination.append(Color.RED)

def get_speed(turn_rate: int) -> int:
   default_speed = (100 * SPEED_MULTIPLIER)
   speed = default_speed - turn_rate * (turn_rate / default_speed)
   return speed if speed > 10 else 10

def navRoad(road):
    robot.drive(get_speed(get_turn_rate()), get_turn_rate())
    wait(10)

def main():
    while True:
        print("yo")
        navRoad(Light_sensor.color())

        if currentDestination[len(currentDestination)-1] == Color.GREEN:
            roundabout()

        wait(10)

if __name__ == '__main__':
    sys.exit(main())