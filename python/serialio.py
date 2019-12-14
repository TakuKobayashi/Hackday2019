# coding:utf-8

import serial
import time

class SerialIO:
    def __init__(self):
        self.ser = self.connection()

    # 受信
    def recieve(self):
        if self.ser is None:
            self.ser = self.connection()
            time.sleep(2)
            if self.ser is None:
                return ""
        line = self.ser.readline()
        print(line)
        return line

    # 送信
    def send(self, message="F\n"):
        if self.ser is None:
            self.ser = self.connection()
            time.sleep(2)
            if self.ser is None:
                return ""
        result = self.ser.write(message.encode())
        print(result)
        return "ok"

    def close(self):
        if self.ser is not None:
            self.ser.close()

    def connection(self):
        try:
            ser = serial.Serial('/dev/tty.usbserial-1420', 19200, timeout=None)
            return ser
        except serial.serialutil.SerialException as e:
            print(e)
            return None
