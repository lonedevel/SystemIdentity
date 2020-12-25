import rumps
from subprocess import Popen, PIPE, call
import os

class StatusUtility(object):
    def get_hostname(self):
        hostname = Popen(['uname', '-n'], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
        (key, value) = ('Hostname', hostname)
        return value

    def get_user(self):
        user = os.getenv('USER')
        (key, value) = ('👨🏻', user)
        return f'{key}: {value}'

    def get_uptime(self):
        cmd = r"uptime | sed 's/.*up \([^,]*\), .*/\1/'"
        uptime=Popen(['/bin/bash', '-c', cmd], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
        (key, value) = ('⬆️', uptime)
        return f'{key}: {value}'

    def get_ip(self):
        cmd = "ifconfig | grep inet | grep -v inet6 | cut -d\" \" -f2 | tail -n1"
        ip = Popen(['/bin/bash', '-c', cmd], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
        (key, value) = ('🌐', ip)
        return f'{key}: {value}'

class SystemIdentity(object):
    def __init__(self):
        su = StatusUtility()
        self.app = rumps.App("SystemId", "ℹ️")
        self.app.title = "ℹ️ " + su.get_hostname()
        self.open_panel_button = rumps.MenuItem(title="Show Panel", callback=self.manage_floating_window)
        self.user_button = rumps.MenuItem(title=su.get_user())
        self.uptime_button = rumps.MenuItem(title=su.get_uptime())
        self.ip_button = rumps.MenuItem(title=su.get_ip())
        self.app.menu = [self.open_panel_button, None, self.user_button, self.uptime_button, self.ip_button, None]

    def manage_floating_window(self, sender):
        if sender.title.lower().startswith('show'):
            os.system("open /Applications/Helium.app")
            sender.title = "Hide Panel"
        else:
            os.system("""osascript -e 'quit app "Helium"'""")
            sender.title = "Show Panel"

    def run(self):
        self.app.run()


if __name__ == "__main__":
    app = SystemIdentity()
    app.run()




