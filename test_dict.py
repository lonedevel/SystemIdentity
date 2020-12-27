from subprocess import Popen, PIPE, call
import os


class StatusUtility(object):
    status_data = {
        'hostname': {'name': "Host Name",
                     'cmd': r"uname -n", 'icon':'🖥'},
        'username': {'name': "User Name",
                     'cmd': r"whoami", 'icon':'👨🏻'},
        'uptime': {'name': "Uptime",
                   'cmd': r"uptime | sed 's/.*up \([^,]*\), .*/\1/'", 'icon':'⬆'},
        'ipaddr': {'name': "IPv4 Address",
                   'cmd': r"ifconfig | grep inet | grep -v inet6 | cut -d\" \" -f2 | tail -n1", 'icon':'🌐'},
        'os': {'name': "Operating System",
               'cmd': r"echo `sw_vers -productName` `sw_vers -productVersion`", 'icon': '💿'},
    }

    def get_data(self, metric):
        entry = self.status_data[metric]
        name = entry['name']
        cmd = entry['cmd']
        icon = entry['icon']
        value = Popen(['/bin/bash', '-c', cmd], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
        return (name, value, icon)


su = StatusUtility()
print (su.get_data('hostname'))
print (su.get_data('uptime'))

