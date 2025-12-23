import time
import sys
import serial

PORT = "/dev/ttyUSB0"
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

def main():
    if len(sys.argv) < 2:
        return

    name = sys.argv[1]
    str_name = f'{name}\n'

    print('Input: ', name)
    ser.write(str_name.encode())

if __name__ == "__name__":
    main()