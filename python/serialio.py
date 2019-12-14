import serial

# 受信
def recieve():
  ser = serial.Serial('/dev/tty.', 9600, timeout=None)
  line = ser.readline()
  print(line)
  return line

# 送信
def send(message='test'):
  ser = serial.Serial('/dev/tty.', 9600, timeout=None)
  ser.write(message)
  ser.close()