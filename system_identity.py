# !/usr/local/bin/python3
# coding=utf-8

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from subprocess import Popen, PIPE

class StatusUtility(object):
    status_data = {
        'hostname': {'name': "Host Name",
                     'cmd': r"uname -n", 'icon': '🖥'},
        'username': {'name': "User Name",
                     'cmd': r"whoami", 'icon': '👨🏻'},
        'uptime': {'name': "Uptime",
                   'cmd': r"uptime | sed 's/.*up \([^,]*\), .*/\1/'", 'icon': '⬆'},
        'ipaddr': {'name': "IPv4 Address",
                   'cmd': r"ifconfig | grep inet | grep -v inet6 | cut -d' ' -f2 | tail -n1", 'icon': '🌐'},
        'os': {'name': "Operating System",
               'cmd': r"echo `sw_vers -productName` `sw_vers -productVersion`", 'icon': '💿'},
        'cpu_name': {'name': "CPU Name",
                     'cmd': r"sysctl -n machdep.cpu.brand_string |awk '$1=$1' | sed 's/([A-Z]\{1,2\})//g'",
                     'icon': '⚙️'},
        'cpu_core': {'name': "CPU Cores",
                    'cmd': "sysctl -n hw.physicalcpu",
                     'icon': "🛠"},
        'cpu_thread': {'name': "CPU Threads",
                       'cmd': "sysctl -n hw.logicalcpu",
                       'icon': "🔩"}
    }

    def get_data(self, metric):
        entry = self.status_data[metric]
        name = entry['name']
        cmd = entry['cmd']
        glyph = entry['icon']
        value = Popen(['/bin/bash', '-c', cmd], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
        return name, value, glyph

    def get_keys(self):
        return self.status_data.keys()


class SystemInfoWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(SystemInfoWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        #windowRectangle = self.frameGeometry()
        self.move(0, 0)
        status_utility = StatusUtility()

        self.setWindowTitle("System Info")
        layout = QGridLayout()

        grid_row = 0
        for widget_entry in status_utility.get_keys():
            name_label = self.create_label(status_utility.get_data(widget_entry)[0] + ": ", 'name', layout, grid_row, 0)
            value_label = self.create_label(status_utility.get_data(widget_entry)[2] + " " +
                                            status_utility.get_data(widget_entry)[1], '', layout, grid_row, 1)
            grid_row += 1

        self.setLayout(layout)

    def create_label(self, name, type, layout, row, col):
        label = QLabel(name)

        if type == 'name':
            label.setFont(QFont('Arial', 14, QFont.Bold))
        else:
            label.setFont(QFont('Menlo', 14))

        layout.addWidget(label, row, col)

        return label


def showPanel(state):
    if state:
        window.show()
    else:
        window.hide()

app = QApplication([])

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

for widget_entry in su.get_keys():
    menu_text = su.get_data(widget_entry)[2].ljust(3) + \
                su.get_data(widget_entry)[1].rjust(25)
    menu.addAction(menu_text)

# Add a Quit option to the menu.
quit = QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)

# Add the menu to the tray
tray.setContextMenu(menu)

window = SystemInfoWindow()

app.exec_()
