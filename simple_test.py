import serial

ser = serial.Serial("/dev/ttyUSB0",115200,timeout=10)
print(ser)
ser.write('abcdefg'.encode())
data = ser.read(7)
print(data)
if ('abcdefg'.encode() in data):
    print('test pass')
