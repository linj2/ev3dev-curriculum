import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

def main():
    robot = robo.Snatch3r()
    white_level = 45
    yellow_level = 70
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    check_the_test(robot, white_level, yellow_level)
    robot.loop_forever()

def check_the_test(robot, white_level, yellow_level):
    while True:
        if robot.color_sensor.reflected_light_intensity <= white_level:
            robot.stop()
            ev3.Sound.speak("Test Failed")
        if robot.ir_sensor.proximity == 0:
            robot.stop()
            ev3.Sound.beep().wait()
            time.sleep(1)
            robot.arm_up()
            robot.turn_degrees(60,200)
            robot.arm_down()
            robot.turn_degrees(-60,200)
        if robot.color_sensor.reflected_light_intensity >= yellow_level:
            robot.stop()
            ev3.Sound.beep().wait()
            break
    time.sleep(0.1)
    print("Pass the test")
    ev3.Sound.speak("Pass the test")

main()