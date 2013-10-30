#!/usr/bin/env python

import sys
import shlex
import subprocess
import gtk
import appindicator

CHECK_FREQUENCY = 5


class CheckVpnc:
    def __init__(self):
        self.ind = appindicator.Indicator(
            "example-simple-client",
            "channel-insecure-symbolic",
            appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon("channel-secure-symbolic")
        self.menu_setup()
        self.ind.set_menu(self.menu)

    def main(self):
        self.check_status()
        gtk.timeout_add(CHECK_FREQUENCY * 1000, self.check_status)
        gtk.main()

    def quit(self, widget):
        sys.exit(0)

    def menu_setup(self):
        self.menu = gtk.Menu()
        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def check_process(self):
        cmd_ps = subprocess.Popen(shlex.split('ps aux'),
                                  stdout=subprocess.PIPE)
        cmd_grep = subprocess.Popen(shlex.split('grep [v]pnc-connect'),
                                    stdin=cmd_ps.stdout,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        cmd_ps.stdout.close()
        cmd_grep.communicate()
        return cmd_grep.returncode

    def check_interface(self):
        cmd_ifconfig = subprocess.Popen("ifconfig",
                                        stdout=subprocess.PIPE)
        cmd_grep = subprocess.Popen(shlex.split('grep [t]un0'),
                                    stdin=cmd_ifconfig.stdout,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        cmd_ifconfig.stdout.close()
        cmd_grep.communicate()
        return cmd_grep.returncode

    def check_status(self):
        if self.check_process() == 0 and self.check_interface() == 0:
            self.ind.set_status(appindicator.STATUS_ATTENTION)
        else:
            self.ind.set_status(appindicator.STATUS_ACTIVE)
        return True

if __name__ == "__main__":
    indicator = CheckVpnc()
    indicator.main()
