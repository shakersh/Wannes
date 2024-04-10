from time import sleep
from python_carbon import Carbon
from app.core import Constants
from app.util.Dump import Dump
from app.util.Helper import Helper
from gpiozero import Robot

class Move:
    def __init__(self):
        self.robot = Robot(left=(Constants.IN4, Constants.IN3),
                       right=(Constants.IN2, Constants.IN1))
    def forward(self, meters):
        acceleration = Constants.speed / 16
        end_at = Carbon.now().addSeconds(meters)
        is_avoiding = False

        speed = 0
        Dump.dd('forwarding')

        if self.was_moving():
            speed = self.robot.value.left_motor
        
        while Carbon.now().lessThan(end_at):
            if speed < Constants.speed:
                speed = min([speed + acceleration, Constants.speed])
            self.robot.forward(speed)
            if self.has_block():
                self.stop()
                is_avoiding = True
                Dump.dd('stop while moving, blocker very close: Up: ' + str(self.distance_up()) + ', Down: '+ str(self.distance_down))
                break

            sleep(0.05)

        return is_avoiding

    def curve(self, position, last_move=None):
        acceleration = Constants.speed / 16
        speed = Constants.initial_speed
        Dump.dd('curving..')
        
        if last_move == 'curve':
            speed = max(abs(self.robot.value.left_motor), abs(self.robot.value.right_motor))

        if speed < Constants.speed:
            speed = min([speed + acceleration, Constants.speed])

        curve_left = curve_right = 0
        factor = 0
        if position:
            factor = min(abs(position - Constants.face_center) * Constants.curve_unit, 1)

        if position < Constants.face_center:
            curve_left = factor
        if position > Constants.face_center:
            curve_right = factor

        Dump.dd("curve_right=" + str(curve_right) + "  | curve_left=" + str(curve_left))
        self.robot.forward(speed, curve_left=curve_left, curve_right=curve_right)
        sleep(0.1)

    def left(self, speed=0):
        if self.was_moving():
            self.stop()

        if not speed:
            speed = Constants.turning_speed

        self.robot.left(speed)

    def right(self, speed=0):
        if self.was_moving():
            self.stop()

        if not speed:
            speed = Constants.turning_speed
        self.robot.right(speed)

    def stop(self):
        Dump.dd('stopping')
        deceleration = Constants.speed / 6
        speed = 0

        if self.was_moving():
            speed = self.robot.value.left_motor
            
        while speed > 0:
            speed = max([speed - deceleration, 0])
            self.robot.forward(speed)
            sleep(0.05)

        self.robot.stop()

    def backward(self, meters, speed=0):
        if self.was_moving():
            self.stop()

        if not speed:
            speed = Constants.turning_speed

        self.robot.backward(speed)

    def looking(self, meters, side='right', speed=0):
        if self.was_moving():
            self.stop()

        if not speed:
            speed = Constants.turning_speed

        if side == 'right':
            self.robot.right(speed)
        else:
            self.robot.left(speed)
        sleep(meters)
    
    def was_moving(self):
        if self.robot.value.left_motor and self.robot.value.right_motor and self.robot.value.left_motor == self.robot.value.right_motor:
            return True
        
        return False
        
    def clear(self):
        self.robot.close()

    def distance_up(self):
        Dump.dd('distance_up: ' + str(Constants.sensor_up.distance * 100))
        return int(Constants.sensor_up.distance * 100)
        
    def distance_down(self):
        Dump.dd('distance_down: ' + str(Constants.sensor_down.distance * 100))
        return int(Constants.sensor_down.distance * 100)

    def has_block(self):
        return self.distance_up() <= Constants.blocker_distance or self.distance_down() <= Constants.blocker_distance

    def reach(self):
        return self.distance_up() <= Constants.min_blocker_distance or self.distance_down() <= Constants.min_blocker_distance

    def right_blocker(self):
        Dump.dd('right_blocker: ' + str(Constants.sensor_right.distance * 100))
        return int(Constants.sensor_right.distance * 100) <= Constants.blocker_distance

    def left_blocker(self):
        Dump.dd('left_blocker: ' + str(Constants.sensor_left.distance * 100))
        return int(Constants.sensor_left.distance * 100) <= Constants.blocker_distance
