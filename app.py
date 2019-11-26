#!/usr/bin/python3
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPlainTextEdit
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi
#api
import re,requests,json,uuid

def validateKey(mac,serial,key):
    try:
        API = "https://bugpredator.herokuapp.com/validate"
        data  = {
            'mac' : mac,
            'serial' : serial,
            'key' : key
        }
        r = requests.post(url=API,json=data)
        response = json.loads(r.text)
        print(response)
        if(response['status'] == 'valid'):
            return True
        return False
    except :
        print("error")
        return False

class LicenseValidation(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('./assets/app.ui',self)
        # self.mac_id = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        self.mac_id = str(uuid.getnode())
        self.MachIdCopy.setText(self.mac_id)
        self.NextPage.setEnabled(False)
        pixmap = QPixmap('./assets/chatboxlogo.jpg')
        self.Chatbox.setGeometry(QtCore.QRect(80,0,500, 175))
        self.Chatbox.setPixmap(pixmap)
        self.setWindowTitle('Licensing Page')
        self.ConfirmButton.clicked.connect(self.on_license_clicked)
    @pyqtSlot()
    def on_license_clicked(self):
        print(self.mac_id)
        mac = self.mac_id
        serial = self.SerialNo.text()
        key = self.InputLicense.text()
        status = validateKey(mac,serial,key)
        if(status):
            self.Status.setText("Activated")
        else:
            self.Status.setText("Invalid")            
        self.Status.setFont(QtGui.QFont('SansSerif', 16))
        # self.MachIdCopy.setReadOnly(True)
        self.NextPage.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = LicenseValidation()
    widget.show()
    sys.exit(app.exec_())