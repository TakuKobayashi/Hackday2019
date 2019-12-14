# coding:utf-8

import serial

# 受信
def recieve():
  ser = serial.Serial('/dev/tty.usbserial-1430', 19200, timeout=None)
  line = ser.readline()
  print(line)
  return line

# 送信
def send(message="F\n"):
  ser = serial.Serial('/dev/tty.usbserial-1430', 19200, timeout=None)
  result = ser.write(message.encode())
  print(result)
  ser.close()
  return "ok"