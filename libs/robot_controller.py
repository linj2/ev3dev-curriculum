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


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
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
    def drive_inches(self,inches_target, speed_deg_per_second):
        # Connect two large motors on output ports B and C
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        # Check that the motors are actually connected
        assert left_motor.connected
        assert right_motor.connected

        distance = 1  # Any value other than 0.
        while distance != 0:
            speed = int(input("Enter a speed for the motors (0 to 900 dps): "))
            distance = int(input("Enter a distance to drive (inches): "))
            left_motor.run_to_rel_pos(position_sp=distance * 360 / 4, speed_sp=speed,
                                      stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            right_motor.run_to_rel_pos(position_sp=distance * 360 / 4, speed_sp=speed,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            left_motor.wait_while(ev3.Motor.STATE_RUNNING)
            right_motor.wait_while(ev3.Motor.STATE_RUNNING)
            ev3.Sound.beep().wait()

        print("Goodbye!")
        ev3.Sound.speak("Goodbye").wait()

    def arm_calibration(self):
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        assert arm_motor.connected

        touch_sensor = ev3.TouchSensor()
        assert touch_sensor

        arm_motor.run_forever(speed_sp=900)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
            if touch_sensor.is_pressed:
                break
        arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep()

        arm_revolutions_for_full_range = 14.2 * 360
        arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

        arm_motor.position = 0

    def arm_up(self):
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        assert arm_motor.connected

        touch_sensor = ev3.TouchSensor()
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

        touch_sensor = ev3.TouchSensor()
        assert touch_sensor
        arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)
        arm_motor.wait_while(ev3.Motor.STATE_HOLDING)

        ev3.Sound.beep()
