import serial
import time
import threading

# Global variable to store serial responses
response_data = []

def read_serial_data(ser):
    """Function to continuously read incoming serial data."""
    global response_data
    while True:
        # Read a line from the serial port (non-blocking)
        line = ser.readline().decode().strip()
        if line:  # Only print if there is data
            print(f"Received (from interrupt or async): {line}")
            response_data.append(line)  # Store response if needed

def main():
    # Set up serial port parameters
    port = "/dev/ttyACM0"  # Update with your serial port
    baud_rate = 115200      # Update with your desired baud rate

    try:
        # Initialize serial connection
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Connected to {port} at {baud_rate} baud.")

        # Start a separate thread to read serial data continuously
        serial_thread = threading.Thread(target=read_serial_data, args=(ser,))
        serial_thread.daemon = True  # Make the thread a daemon, so it stops when the main program ends
        serial_thread.start()

        while True:
            # Get user input to send over serial
            user_input = input("Enter a string to send (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                print("Exiting...")
                break

            # Send data to the serial port
            if user_input.lower() == '1':
                ser.write('SVHDDSTAT00ALLSV'.encode())
                print("Data sent, waiting for response...")

            # Allow some time for the device to respond
            time.sleep(1)

            # Read the response from the serial port (will be handled asynchronously in the background)
            print("Waiting for response...")
            if response_data:
                print("Stored responses:")
                for line in response_data:
                    print(f"Response: {line}")
                # Clear the response data after displaying
                response_data.clear()

    except serial.SerialException as e:
        print(f"Error: {e}")

    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    main()
