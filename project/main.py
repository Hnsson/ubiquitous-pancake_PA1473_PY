#!/usr/bin/env pybricks-micropython
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
TURN_MULTIPLIER = 0.8
DRIVE_SPEED = 35
PROPORTIONAL_GAIN = 0.8
DEFAULT_RANGE = range(50, 70)
currentColor = Color.GREEN

GREEN = 12
BROWN = 20
PURPLE = range(10, 13)
RED = 82
BLUE = 13

currently_lifting = False

roundabout_color = Color.BROWN

def drawToScreen(x, y, text):
    ev3.screen.clear()
    ev3.screen.draw_text(x, y, text)

def collision(distance: int = COLLISION_DISTANCE):
    colliding = bool(Ultrasonic_sensor.distance() <= distance)
    while colliding:
        robot.stop()
        colliding = bool(Ultrasonic_sensor.distance() <= distance)

def emergency_mode():
    drawToScreen(40, 50, "EMERGENCY MODE")
    for i in range(10):
        ev3.speaker.say("help me")


def deliveryController():
    robot.straight(100)
    robot.turn(180)
    robot.straight(350)

    Crane_motor.run_angle(900, -45, then=Stop.HOLD, wait=True)

    robot.straight(-350)
    robot.trun(195)
    straight(200)


def wareHouseController(road):
    done_lifting = False
    while not done_lifting:

        if road == Color.BLUE:
            navRoad([Color.BLACK])
        if road == Color.RED:
            navRoad([Color.BLACK, Color.BROWN])

        if Front_button.pressed():
            done_lifting = safeLift()

    currently_lifting = True

    if road == Color.BLUE:
        robot.straight(-500)
        robot.turn(-360)
    if road == Color.RED:
        robot.straight(-600)
        robot.turn(-160)
        robot.straight(500)
    currentDestination.append(Color.GREEN)
    drawToScreen(20, 50, "DELIVERY")


def test_rate(optimal_colors):
    current_color = Light_sensor.color()
    if current_color in optimal_colors:
        return 3
    elif not current_color in optimal_colors and current_color != Color.WHITE:
        return 0
    else:
        return -1


def get_speed(turn_rate: int) -> int:
   default_speed = DRIVE_SPEED * 2
   speed = default_speed - turn_rate
   return 10 if speed > DRIVE_SPEED else 10


def navRoundabout(destination):
    drawToScreen(20, 50, "ROUNDABOUT")

    # Whilen under? kanske ta bort allt efter or
    while Light_sensor.color() != destination:
        print(Light_sensor.color())
        navRoad([destination, roundabout_color])

def navRoad(roads):
    drawToScreen(20, 50, "DESTINATION")
    turn_rate = PROPORTIONAL_GAIN * test_rate(roads) * 22

    robot.drive(get_speed(turn_rate), turn_rate)

    collision()
    wait(10)

def safeLift():
    drawToScreen(40, 50, "LIFTING")

    robot.stop()
    Crane_motor.run_angle(900, 45, then=Stop.HOLD, wait=True)

    return True


currentDestination = [roundabout_color, Color.GREEN, Color.RED]

while True:
    navRoad(currentDestination)   

    # # Color of roundabout
    # if Light_sensor.color() == Color.GREEN:
    #     # Destination color
    #     navRoundabout(currentDestination[-1])
    # else:
    #     # Allowed colors for roads
    #     navRoad([Color.BROWN, Color.GREEN, Color.RED, Color.BLUE])
    #     # navRoad([Color.BROWN, Color.BLUE, Color.GREEN])
    #     # navRoad([Color.BROWN, Color.RED, Color.BLUE, Color.GREEN, Color.PURPLE])

    if currently_lifting is True and not Front_button.pressed():
        emergency_mode()

    if Light_sensor.color() == Color.BLACK:
        if currentDestination[-1] == Color.GREEN:
            deliveryController()
        if currentDestination[-1] == Color.RED:
            wareHouseController(Color.RED)
        if currentDestination[-1] == Color.BLUE:
            wareHouseController(Color.BLUE)