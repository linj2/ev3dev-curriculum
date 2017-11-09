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
    forward_button['command'] = lambda: forward(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: forward(mqtt_client, left_speed_entry, right_speed_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=1)
    left_button['command'] = lambda: left(mqtt_client,left_speed_entry, right_speed_entry)
    root.bind('<Left>', lambda event: left(mqtt_client,left_speed_entry, right_speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=2)
    stop_button['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=3)
    right_button['command'] = lambda: right(mqtt_client,left_speed_entry, right_speed_entry)
    root.bind('<Right>', lambda event: right(mqtt_client,left_speed_entry, right_speed_entry))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=2)
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

    # Robot speaks what human input.
    speak_label = ttk.Label(main_frame, text="things you want robot to speak: ")
    speak_label.grid(row=7, column=0)
    speak_entry = ttk.Entry(main_frame, width=20)
    speak_entry.insert(0, "Hello World") # set default to Hello World!
    speak_entry.grid(row=7, column=1, columnspan=2)

    var = ttk.IntVar()
    # do nothing
    nothing_rb = ttk.Radiobutton(main_frame, text="be quiet", variable=var, value=1,
                                         command = lambda: radiobutton_option(var))
    nothing_rb.grid(row=8, column=0)
    # speak
    speak_radio_button = ttk.Radiobutton(main_frame, text="speak the sentence", variable=var, value=2,
                                         command = lambda: radiobutton_option(var))
    speak_radio_button.grid(row=9, column = 0)
    # play music
    play_radio_button = ttk.Radiobutton(main_frame, text="play the music", variable=var, value=3,
                                        command=lambda: radiobutton_option(var))
    play_radio_button.grid(row=10,column = 0)
    # beep
    beep_radio_button = ttk.Radiobutton(main_frame, text="beep", variable=var, value=4,
                                           command=lambda: radiobutton_option(var))
    beep_radio_button.grid(row=11,column =0)

    root.mainloop()

def radiobutton_option(mqtt_client, var,speak_entry):
    mqtt_client.send_message("play_or_speak", [var, speak_entry.get()])

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