b"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time
import random

class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    def __init__(self):
        self.touch_sensor = ev3.TouchSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        assert self.touch_sensor
        assert self.pixy
        assert self.color_sensor
        assert self.ir_sensor
        assert self.arm_motor.connected

    def drive_inches(self,distance,speed):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        left_motor.run_to_rel_pos(position_sp=distance * 90, speed_sp=speed,
                                  stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        right_motor.run_to_rel_pos(position_sp=distance * 90, speed_sp=speed,
                                   stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self,degrees,speed):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        left_motor.run_to_rel_pos(position_sp=(-degrees)*5, speed_sp=speed,
                                  stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        right_motor.run_to_rel_pos(position_sp=degrees*5, speed_sp=speed,
                                   stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        right_motor.wait_while(ev3.Motor.STATE_RUNNING)
    # DONE: Implement the Snatch3r class as needed when working the sandox exercises
    # (and delete these comments)


    def arm_calibration(self):


        touch_sensor = ev3.TouchSensor()
        assert touch_sensor

        self.arm_motor.run_forever(speed_sp=900)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
            if touch_sensor.is_pressed:
                break
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep()

        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

        self.arm_motor.position = 0

    def arm_up(self):
        touch_sensor = ev3.TouchSensor()
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        assert arm_motor.connected
        assert touch_sensor
        arm_motor.run_to_rel_pos(position_sp=14.2 * 360, speed_sp=900)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
            if touch_sensor.is_pressed:
                break
        arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep()

    def arm_down(self):
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        assert arm_motor.connected
        arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()


    def shutdown(self):
        btn = ev3.Button()
        while btn.backspace:
            ev3.Leds.set_color(ev3.Leds.LEFT,ev3.Leds.GREEN)
            ev3.Leds.set_color(ev3.Leds.RIGHT,ev3.Leds.GREEN)
            ev3.Sound.speak('goodbye').wait()
            print('goodbye')

    def loop_forever(self):

        self.running = True
        while self.running:
            time.sleep(0.1)

    def forward(self,left_speed,right_speed):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        assert left_motor.connected
        assert right_motor.connected

        left_motor.run_forever(speed_sp = left_speed)
        right_motor.run_forever(speed_sp = right_speed)

    def stop(self):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        assert left_motor.connected
        assert right_motor.connected
        left_motor.stop(stop_action = 'brake')
        right_motor.stop(stop_action = 'brake')

    def shut_down(self):
        # Modify a variable that will allow the loop_forever method to end. Additionally stop motors and set LEDs green.
        # The most important part of this method is given here, but you should add a bit more to stop motors, etc.
        self.running = False

    def right(self, left_speed, right_speed):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        assert left_motor.connected
        assert right_motor.connected

        left_motor.run_forever(speed_sp=left_speed)
        right_motor.run_forever(speed_sp= -right_speed)


    def left(self, left_speed, right_speed):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        assert left_motor.connected
        assert right_motor.connected

        left_motor.run_forever(speed_sp=-left_speed)
        right_motor.run_forever(speed_sp=right_speed)

    def backward(self,left_speed, right_speed):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        assert left_motor.connected
        assert right_motor.connected

        left_motor.run_forever(speed_sp=-left_speed)
        right_motor.run_forever(speed_sp=-right_speed)


    def seek_beacon(self,robot):
        beacon_seeker = ev3.BeaconSeeker(channel=1)

        forward_speed = 300
        turn_speed = 100

        while not robot.touch_sensor.is_pressed:
            # The touch sensor can be used to abort the attempt (sometimes handy during testing)


            current_heading = beacon_seeker.heading  # use the beacon_seeker heading
            current_distance = beacon_seeker.distance  # use the beacon_seeker distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                robot.right(turn_speed,turn_speed)
            else:


                # Here is some code to help get you started
                if math.fabs(current_heading) < 2:
                    if current_distance == 0:
                        robot.drive_inches(2.5, 300)
                        robot.stop()
                        return True
                    # Close enough of a heading to move forward
                    print("On the right heading. Distance: ", current_distance)
                    # You add more!
                    if current_distance > 0:
                        robot.forward(forward_speed, forward_speed)

                if 2 < math.fabs(current_heading) < 10:
                    if current_heading < 0:
                        robot.left(turn_speed, turn_speed)

                    if current_heading > 0:
                        robot.right(turn_speed, turn_speed)
                if math.fabs(current_heading) > 10:
                    robot.right(turn_speed,turn_speed)
                    print('Heading too far off')

        time.sleep(0.2)


    def way_finding(self,speed):
        ev3.Sound.speak('looking for a path')
        while True:

            if self.touch_sensor.is_pressed:
                break
            if self.ir_sensor.proximity >= 15:
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
                self.forward(speed,speed)
                if self.ir_sensor.proximity < 15:
                    self.stop()
                    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
                    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
                    ev3.Sound.speak("path is blocked")
                    self.turn_degrees(90,speed)

                    ev3.Sound.speak('path is clear')
                    continue
        self.stop()
        ev3.Sound.speak('stop looking for a path')
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)

    def play_or_speak(self, var, speak_entry):
        if var == 2:
            ev3.Sound.speak(speak_entry)
        if var == 3:
            ev3.Sound.play("/home/robot/csse120/assets/sounds/juhuatai_pcm.wav").wait()
        if var == 4:
            ev3.Sound.beep().wait()

    def action_block(self, left, right):
        if self.ir_sensor.proximity < 10:
            ev3.Sound.beep().wait()
            self.arm_up()
            self.drive_inches(-3, right)
            self.turn_degrees(random.randrange(0, 90)*-1, right)
            self.turn_degrees(random.randrange(0, 90), right)
            self.turn_degrees(random.randrange(0, 90, 5)*-1, right)
            self.turn_degrees(random.randrange(0, 90, 5), right)
            self.drive_inches(3, right)
            self.arm_down()
            self.stop()
            ev3.Sound.beep().wait()
