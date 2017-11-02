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
        right_motor.run_forever(speed_sp= -(right_speed))


    def left(self, left_speed, right_speed):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        assert left_motor.connected
        assert right_motor.connected

        left_motor.run_forever(speed_sp=-int(left_speed))
        right_motor.run_forever(speed_sp=right_speed)

    def backward(self,left_speed, right_speed):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        assert left_motor.connected
        assert right_motor.connected

        left_motor.run_forever(speed_sp=-int(left_speed))
        right_motor.run_forever(speed_sp=-int(right_speed))