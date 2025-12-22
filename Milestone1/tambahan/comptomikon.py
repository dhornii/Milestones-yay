import serial
import time

PORT = "/dev/ttyUSB0"
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

def map_numbers(number):
    if(number <= 100):
        return (number - 100) * (180)
    else:
        return 0

def move_servo(angle):
    str_angle = f'{angle}\n'
    ser.write(str_angle.encode())

try:
    while True:
        if (ser.in_waiting > 0):
            line = ser.readline().decode('utf-8', errors='replace').strip()
            print(line)

            if(line != "Timeout!"):
                angle = map_numbers(int(line))
                move_servo(angle)
                time.sleep(2)

except KeyboardInterrupt:
    print("Keluar ...")
finally:
    ser.close()