import serial
import time

PORT = "/dev/ttyUSB0"
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1) # buka serial 
time.sleep(2) # delay 2 detik

def move_servo(angle):
    str_angle = f'{angle}\n'        # ubah ke string
    ser.write(str_angle.encode())   # encode string lalu kirimkan ke serial

try:
    while True:
        angle = input("Input sudut gerakan: ")
        move_servo(angle)          # kirim informasi sudut ke serial
        time.sleep(2)              # delay lagi

except KeyboardInterrupt:
    print("Keluar ...")
finally:
    ser.close() # tutup serial kalau program sudah selesai