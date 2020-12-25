# !/usr/local/bin/python3
# coding=utf-8

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from subprocess import Popen, PIPE, call
import os


class StatusUtility(object):
    def get_hostname(self):
        hostname = Popen(['uname', '-n'], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
        (key, value) = ('🖥', hostname)
        return f'{key} {value}'

    def get_user(self):
        user = os.getenv('USER')
        (key, value) = ('👨🏻', user)
        return f'{key} {value}'

    def get_uptime(self):
        cmd = r"uptime | sed 's/.*up \([^,]*\), .*/\1/'"
        uptime=Popen(['/bin/bash', '-c', cmd], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
        (key, value) = ('⬆️', uptime)
        return f'{key} {value}'

    def get_ip(self):
        cmd = "ifconfig | grep inet | grep -v inet6 | cut -d\" \" -f2 | tail -n1"
        ip = Popen(['/bin/bash', '-c', cmd], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
        (key, value) = ('🌐', ip)
        return f'{key} {value}'


class SystemInfoWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(SystemInfoWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        #windowRectangle = self.frameGeometry()
        self.move(0, 0)

        su = StatusUtility()

        self.setWindowTitle("System Info")
        layout = QGridLayout()

        (hostname_label, hostname_value) = (QLabel("Hostname:"), QLabel(su.get_hostname()))
        (username_label, username_value) = (QLabel("Username:"), QLabel(su.get_user()))
        (uptime_label, uptime_value) = (QLabel("Uptime:"), QLabel(su.get_uptime()))
        (ip_label, ip_value) = (QLabel("IP Address:"), QLabel(su.get_ip()))

        hostname_label.setFont(QFont('Arial', 14, QFont.Bold))
        username_label.setFont(QFont('Arial', 14, QFont.Bold))
        uptime_label.setFont(QFont('Arial', 14, QFont.Bold))
        ip_label.setFont(QFont('Arial', 14, QFont.Bold))

        hostname_value.setFont(QFont('Menlo', 14, QFont.Bold))
        username_value.setFont(QFont('Menlo', 14, QFont.Bold))
        uptime_value.setFont(QFont('Menlo', 14, QFont.Bold))
        ip_value.setFont(QFont('Menlo', 14, QFont.Bold))

        layout.addWidget(hostname_label, 0, 0)
        layout.addWidget(hostname_value, 0, 1)
        layout.addWidget(username_label, 1, 0)
        layout.addWidget(username_value, 1, 1)
        layout.addWidget(uptime_label, 2, 0)
        layout.addWidget(uptime_value, 2, 1)
        layout.addWidget(ip_label, 3, 0)
        layout.addWidget(ip_value, 3, 1)

        self.setLayout(layout)


def showPanel(state):
    if state:
        window.show()
    else:
        window.hide()

app = QApplication([])
#app.setQuitOnLastWindowClosed(False)

# Create the icon
icon = QIcon("brain.png")
su = StatusUtility()

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# Create the menu
menu = QMenu()

panel_action = QAction("Show panel")
panel_action.setCheckable(True)
panel_action.triggered.connect(showPanel)
menu.addAction(panel_action)
menu.addSeparator()
menu.addAction(su.get_hostname())
menu.addAction(su.get_user())
menu.addAction(su.get_uptime())
menu.addAction(su.get_ip())

# Add a Quit option to the menu.
quit = QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)

# Add the menu to the tray
tray.setContextMenu(menu)

window = SystemInfoWindow()


app.exec_()