import serial
import time
import keyboard
import tkinter as tk
from threading import Thread

# Key mappings for each servo
key_mappings = {
    'Servo 1': ('a', 'z'),
    'Servo 2': ('q', 'w'),
    'Servo 3': ('e', 'r'),
    'Servo 4': ('t', 'y'),
    'Servo 5': ('u', 'i'),
    'Servo 6': ('o', 'p'),
    'Servo 7': ('s', 'd'),
}

# Initial servo positions
servo_positions = {
    'Servo 1': 90,
    'Servo 2': 90,
    'Servo 3': 90,
    'Servo 4': 90,
    'Servo 5': 90,
    'Servo 6': 90,
    'Servo 7': 90,
    'Servo 8': 90,
    'Servo 9': 90,
    'Servo 10': 90,
    'Servo 11': 90,
    'Servo 12': 90,
}

# Store position labels for each servo
position_labels = {}

# Global variables
claw_open = False
arduino = None
root = None


# Function to create and show the key-mapping GUI
def show_key_mappings():
    global root
    root = tk.Tk()
    root.title("Servo Control Key Mappings and Claw Control")

    row = 0
    for servo, keys in key_mappings.items():
        servo_label = tk.Label(root, text=f"{servo}:", font=('Helvetica', 14, 'bold'))
        servo_label.grid(row=row, column=0, padx=10, pady=5, sticky='e')

        key_label = tk.Label(root, text=f"Up: {keys[0].upper()}, Down: {keys[1].upper()}", font=('Helvetica', 14))
        key_label.grid(row=row, column=1, padx=10, pady=5, sticky='w')

        position_label = tk.Label(root, text=f"Position: {servo_positions[servo]}°", font=('Helvetica', 14))
        position_label.grid(row=row, column=2, padx=10, pady=5, sticky='w')

        position_labels[servo] = position_label

        row += 1

    claw_label = tk.Label(root, text="Claw Control:", font=('Helvetica', 14, 'bold'))
    claw_label.grid(row=row, column=0, padx=10, pady=5, sticky='e')

    claw_button = tk.Button(root, text="Toggle Claw", font=('Helvetica', 14), command=toggle_claw)
    claw_button.grid(row=row, column=1, padx=10, pady=5, sticky='w')

    root.after(1000, request_positions)
    root.mainloop()


# Function to toggle claw servos
def toggle_claw():
    global claw_open
    claw_open = not claw_open
    command = '1' if claw_open else '0'
    if arduino:
        arduino.write(command.encode())
        print(f"Claw {'open' if claw_open else 'closed'}")


# Function to handle servo control
def control_servos():
    global arduino
    try:
        while True:
            if arduino:
                response = arduino.readline().decode(errors='ignore').strip()
                if "Servos stopped" in response:
                    print("Safety triggered: Servos stopped due to obstacle detection.")
                    continue

            for servo, keys in key_mappings.items():
                if keyboard.is_pressed(keys[0]):
                    if arduino:
                        arduino.write(keys[0].encode())
                        print(f"{keys[0]} pressed")
                    time.sleep(0.05)  # Delay to prevent flooding the serial with messages
                elif keyboard.is_pressed(keys[1]):
                    if arduino:
                        arduino.write(keys[1].encode())
                        print(f"{keys[1]} pressed")
                    time.sleep(0.05)
            if keyboard.is_pressed('Esc'):
                print("Exiting...")
                break

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def request_positions():
    global arduino
    try:
        if arduino:
            arduino.write(b'P')  # Send position request command
            response = arduino.readline().decode(errors='ignore').strip()
            print(f"Received response: {response}")  # Debugging information
            if response.startswith("P:"):
                positions = response[2:].split(',')
                if len(positions) == 12:  # Ensure correct number of positions received
                    for i, (servo, label) in enumerate(position_labels.items()):
                        label.config(text=f"Position: {positions[i]}°")
                else:
                    print("Incorrect number of positions received")

    except Exception as e:
        print(f"Failed to request positions: {e}")

    root.after(1000, request_positions)  # Request positions every second


def initialize_serial():
    global arduino
    try:
        arduino = serial.Serial('COM5', 9600, timeout=1)  # Use COM5 for your Arduino
        time.sleep(2)  # Wait for the serial connection to initialize
        print("Serial connection established")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Initialize serial connection
initialize_serial()

# Run the key-mapping GUI in a separate thread
thread = Thread(target=show_key_mappings)
thread.start()

# Run the servo control function
control_servos()
