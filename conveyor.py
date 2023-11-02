import serial

def send_message(message):
    # Define the serial port and baud rate
    serial_port = '/dev/cu.usbmodem101'
    baud_rate = 9600  # Make sure it matches the Arduino's baud rate


    # Open the serial connection
    # ser = serial.Serial(serial_port, baud_rate, timeout=1)
    # print(f"Serial port {serial_port} opened successfully.")

    ser = serial.Serial(serial_port, baud_rate, timeout=1)

    try:
        # Send a message to the Arduino
        ser.write(message.encode())
        print(f"Sent: {message}")

        # Close the serial connection
    except serial.SerialException as e:
        print(f"Error opening the serial port: {e}")

    print("Serial port closed.")
    ser.close()

if __name__ == "__main__":
    send_message("g")