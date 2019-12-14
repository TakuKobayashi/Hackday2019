# coding:utf-8

import serial

class SerialIO:
    def __init__(self):
        self.ser = serial.Serial('/dev/tty.usbserial-1420', 19200, timeout=None)

    # 受信
    def recieve(self):
        line = self.ser.readline()
        print(line)
        return line

    # 送信
    def send(self, message="F\n"):
        result = self.ser.write(message.encode())
        print(result)
        return "ok"

    def close(self):
        self.ser.close()
