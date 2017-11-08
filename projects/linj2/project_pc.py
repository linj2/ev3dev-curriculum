import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=1)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=1)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=3)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=3)


    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=2)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: forward(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: forward(mqtt_client, left_speed_entry, right_speed_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=1)
    # left_button and '<Left>' key
    left_button['command'] = lambda: left(mqtt_client,left_speed_entry, right_speed_entry)
    root.bind('<Left>', lambda event: left(mqtt_client,left_speed_entry, right_speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=2)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=3)
    # right_button and '<Right>' key
    right_button['command'] = lambda: right(mqtt_client,left_speed_entry, right_speed_entry)
    root.bind('<Right>', lambda event: right(mqtt_client,left_speed_entry, right_speed_entry))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=2)
    # back_button and '<Down>' key
    back_button['command'] = lambda: backward(mqtt_client,left_speed_entry, right_speed_entry)
    root.bind('<Down>', lambda event: backward(mqtt_client,left_speed_entry, right_speed_entry))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=1)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=1)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=3)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=3)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    speak_label = ttk.Label(main_frame, text="things you want robot to speak: ")
    speak_label.grid(row=7, column=0)
    speak_entry = ttk.Entry(main_frame, width=20)
    speak_entry.insert(0, "Hello World")
    speak_entry.grid(row=7, column=1, columnspan=2)

    speak_radio_button = ttk.Radiobutton(main_frame, text = "speak the sentence", value=1)
    speak_radio_button.grid(row=8, column = 0)

    play_radio_button = ttk.Radiobutton(main_frame, text= "play the music", value=2)
    play_radio_button.grid(row=9,column = 0)

    play_button = ttk.Button(main_frame, text="Speak/Play")
    play_button.grid(row=9, column=1)
    play_button['command'] = lambda: play_or_speak(mqtt_client, speak_radio_button, speak_entry, play_radio_button)

    root.mainloop()

def play_or_speak(mqtt_client,speak_radio_button, speak_entry, play_radio_button):
    mqtt_client.send_message("play_or_speak", [speak_radio_button, speak_entry.get(), play_radio_button])

def forward(mqtt_client, left_speed_entry, right_speed_entry):
    print('drive foward')
    mqtt_client.send_message("forward",[int(left_speed_entry.get()),int(right_speed_entry.get())])

def backward(mqtt_client, left_speed_entry, right_speed_entry):
    print('drive backward')
    mqtt_client.send_message("backward",[int(left_speed_entry.get()),int(right_speed_entry.get())])

def left(mqtt_client, left_speed_entry, right_speed_entry):
    print('turn left')
    mqtt_client.send_message("left",[int(left_speed_entry.get()), int(right_speed_entry.get())])

def right(mqtt_client, left_speed_entry, right_speed_entry):
    print('turn right')
    mqtt_client.send_message("right",[int(left_speed_entry.get()),int(right_speed_entry.get())])

def stop(mqtt_client):
    print('stop')
    mqtt_client.send_message("stop")


# Arm command callbacks
def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")

def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")

# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shut_down")
        mqtt_client.send_message("shut_down")
    mqtt_client.close()
    exit()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()