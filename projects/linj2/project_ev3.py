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
    speed=300
    black_level=0
    while not robot.touch_sensor.is_pressed:
        x = robot.pixy.value(1)
        y = robot.pixy.value(2)
        print("(X, Y) = ({},{})".format(x, y))
        if (x > 0 and y > 0) and robot.ir_sensor.proximity < 10:
            ev3.Sound.speak("Happy")
            time.sleep(0.5)
            robot.backward(mqtt_client, speed, speed)
            robot.stop()
            robot.arm_up()
            robot.left(mqtt_client, speed, speed)
            back=speed*2
            robot.right(mqtt_client, back, back)
            robot.left(mqtt_client, back, back)
            robot.right(mqtt_client, speed, speed)
            robot.forward(mqtt_client, back, back)
        elif robot.ir_sensor.proximity<10:
            robot.turn_degrees(mqtt_client,300,900)
            robot.drive_inches(mqtt_client,3,900)
            robot.turn_degrees(mqtt_client,-300,900)
            robot.drive_inches(mqtt_client,-3,900)

        if robot.color_sensor.reflected_light_intensity == black_level:
            follow_the_line(robot, black_level)



        time.sleep(0.1)

    robot.loop_forever()

def follow_the_line(robot, black_level):
    while True:
        if robot.color_sensor.reflected_light_intensity == black_level:
            robot.forward(300, 300)
        if robot.color_sensor.reflected_light_intensity >= black_level:
            robot.right(300,300)

main()