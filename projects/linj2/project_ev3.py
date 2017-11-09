import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"

    while not robot.touch_sensor.is_pressed:

        width = robot.pixy.value(3)
        if width > 0:
            ev3.Sound.beep().wait(1.0)
        print("(X, Y) = ({},{}))   Width = {} Height = {}".format(robot.pixy.value(1), robot.pixy.value(2),
                                                                  robot.pixy.value(3), robot.pixy.value(4)))

        time.sleep(0.1)

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()
    robot.loop_forever()
main()