import ev3dev.ev3 as ev3
import time

import robot_controller as robo

COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]
# This list is just a helper list if you ever want the string (for printing or speaking) from a color value.


class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""

    def __init__(self):
        self.running = True


def main():
    print("--------------------------------------------")
    print("Stop at Red Lines")
    print("--------------------------------------------")
    ev3.Sound.speak("Robot is Driving").wait()
    print("Press Back to exit this program.")

    robot = robo.Snatch3r()
    dc = DataContainer()

    # For our standard shutdown button.
    btn = ev3.Button()
    touch_sensor = ev3.TouchSensor()
    # call
    stop_at_red(True, robot, ev3.ColorSensor.COLOR_RED)
    touch_sensor.is_pressed = lambda state: handle_shutdown(state, dc)

    while dc.running:
        btn.process()
        time.sleep(0.01)

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()


# ----------------------------------------------------------------------
# Event handlers
# ----------------------------------------------------------------------
def stop_at_red(button_state, robot, color_to_seek):
    """
    Testing if the robot touched red line
    """
    if button_state:
        ev3.Sound.speak("Do not touch" + COLOR_NAMES[color_to_seek]).wait()

        while not robot.color_sensor.color == color_to_seek:
            robot.forward(300, 300)
            if robot.color_sensor.color == color_to_seek:
                robot.stop()
                break
        time.sleep(0.5)

        ev3.Sound.speak("Touched" + COLOR_NAMES[color_to_seek]+" You failed the test. Please retake the driving test").wait()

def handle_shutdown(button_state, dc):
    """Exit the program."""
    if button_state:
        dc.running = False


main()