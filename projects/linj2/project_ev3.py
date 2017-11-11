import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()

def follow_the_line(robot, black_level):
    while True:
        if robot.color_sensor.reflected_light_intensity == black_level:
            robot.forward(300, 300)
        if robot.color_sensor.reflected_light_intensity >= black_level:
            robot.right(300,300)
    time.sleep(0.1)

main()