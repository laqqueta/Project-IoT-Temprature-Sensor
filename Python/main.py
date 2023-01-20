import sys
import time
import paho.mqtt.client as mqtt
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QWidget,
    QLCDNumber,
    QApplication,
    QPushButton,
    QLabel,
    QGridLayout,
    QMessageBox)


class RoomTemperature(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.data = DataThread()

        lcdLabel1 = QLabel("Temprature")
        lcdLabel2 = QLabel("Humidity")
        lcd1 = QLCDNumber()
        lcd2 = QLCDNumber()
        buttonExit = QPushButton("Exit")
        buttonConnect = QPushButton("Connect to Broker")

        lcd1.setDigitCount(5)
        lcd2.setDigitCount(5)

        layout = QGridLayout()
        layout.addWidget(buttonConnect, 1, 0, 1, 2)
        layout.addWidget(lcdLabel1, 2, 0)
        layout.addWidget(lcd1, 3, 0)
        layout.addWidget(lcdLabel2, 2, 1)
        layout.addWidget(lcd2, 3, 1)
        layout.addWidget(buttonExit, 4, 0, 1, 2)

        buttonConnect.clicked.connect(self.data.connect_to_broker)
        buttonExit.clicked.connect(self.exit_program)
        self.data.temprature.connect(lcd1.display)
        self.data.humidity.connect(lcd2.display)

        self.setLayout(layout)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Kitchen Temperature')
        self.setWindowIcon(QtGui.QIcon('logo.jpg'))
        self.data.start()
        self.show()

    def exit_program(self):
        self.data.disconnect_from_broker()
        self.close()


class DataThread(QThread):
    temprature = pyqtSignal(object)
    humidity = pyqtSignal(object)

    broker_address = "192.168.18.173"
    port = 1883
    user = "mbkm"
    password = "mbkm"

    client = mqtt.Client("Subscribe : Gamzv (Python)")

    def on_message(self, client, userdata, message):
        msg = str(message.payload.decode("utf-8")).split(":")

        self.temprature.emit(msg[0])
        self.humidity.emit(msg[1])

    def on_connect(self, client, userdata, flags, rc):
        msg = QMessageBox()

        msg.setWindowTitle("Status")
        msg.setText("Connected to Broker")
        msg.setIcon(QMessageBox.Information)
        show = msg.exec_()

    def connect_to_broker(self):
        self.client.username_pw_set(self.user, password=self.password)
        self.client.connect(self.broker_address, self.port)
        self.client.subscribe("device/room/kitchen/")
        self.client.loop_start()

    def disconnect_from_broker(self):
        self.client.disconnect()

    def run(self):
        time.sleep(1)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = RoomTemperature()

    sys.exit(app.exec_())