import serial
import time

def main():
    # Set up serial port parameters
    port = "/dev/ttyUSB0"  # Update with your serial port
    baud_rate = 115200       # Update with your desired baud rate

    try:
        # Initialize serial connection
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Connected to {port} at {baud_rate} baud.")

        while True:
            # Get user input to send over serial
            user_input = input("Enter a string to send (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                print("Exiting...")
                break

            # Send data to the serial port
            ser.write(user_input.encode())
            print("Data sent, waiting for response...")

            # Give the device some time to respond
            time.sleep(1)

            # Read the response from the serial port
            response = ser.readline().decode().strip()
            print(f"Response: {response}")

    except serial.SerialException as e:
        print(f"Error: {e}")

    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    main()
