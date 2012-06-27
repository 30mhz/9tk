# Copyright (C) 2011, 2012 9apps B.V.
#
# This file is part of 9apps ToolKit.
#
# 9apps Tools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# 9apps Tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with 9apps ToolKit. If not, see <http://www.gnu.org/licenses/>.

import cmd

from tools.config import Config
from tools.eip import EIP
from tools.backup import Backup
from tools.volume import Volume

class ToolKit(cmd.Cmd):

    CONFIG = Config.fromAmazon()

    ##########################################################################################

    def help_display(self):
        print "\n".join(["display", "Display user-data associated with this EC2 instance"])

    def do_display(self, line):
        print self.CONFIG

    ##########################################################################################

    EIP_COMMANDS = ["associate", "disassociate", "install", "uninstall"]

    def help_eip(self):
        print "\n".join(["eip {0}".format(self.EIP_COMMANDS), "Associate or disassociate EIP configured in user-data.\
                                                              It can install as well an initd that provision the EIP at boot time."])

    def complete_eip(self, text, line, begidx, endidx):
        if not text:
            completions = self.EIP_COMMANDS[:]
        else:
            completions = [ f
                            for f in self.EIP_COMMANDS
                            if f.startswith(text)
                            ]
        return completions

    def do_eip(self, cmd):
        eip = EIP(self.CONFIG)
        getattr(eip, cmd)()

    ##########################################################################################

    def help_backup(self):
        print "\n".join(["backup", "Setup backup as configured in user-data"])

    def do_backup(self, line):
        backup = Backup(self.CONFIG)
        backup.setup()

    ##########################################################################################

    VOLUME_COMMANDS = ["mount", "umount", "install", "uninstall"]

    def help_volume(self):
        print "\n".join(["volume", "Mount or umount a given list of volumes to their respective mountpoints.\
                                   It can install as well an initd that provision the volume at boot time."])

    def complete_volume(self, text, line, begidx, endidx):
        if not text:
            completions = self.VOLUME_COMMANDS[:]
        else:
            completions = [ f
                            for f in self.VOLUME_COMMANDS
                            if f.startswith(text)
                            ]
        return completions

    def do_volume(self, cmd):
        volume = Volume(self.CONFIG)
        getattr(volume, cmd)()

    ##########################################################################################

    def do_EOF(self, line):
        print "Exit"
        return True

    def emptyline(self):
        return ""

if __name__ == "__main__":
    ToolKit().cmdloop("\nWelcome to the 9apps ToolKit CLI.\n")