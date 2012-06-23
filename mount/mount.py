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

import sys
import subprocess
from subprocess import Popen

def main(argv):
    action = argv[-1]
    if (action != "mount" and action != "umount"):
        print "ERROR - '{0}' is not an accepted action".format(action)
        usage()
        sys.exit()

    arguments = sys.argv[1:len(sys.argv) - 1]

    if (len(arguments) % 2 != 0):
        print "ERROR - '{0}' doesn't appear to have a mountpoint for each volume".format(sys.argv[1:])
        usage()
        sys.exit()
    else:
        numberOfVolumes = len(arguments) / 2
        #loop over volumes, for each one create mountpoint and execute action
        count=0
        while (count < numberOfVolumes):
            device = arguments[count]
            mountpoint = arguments[count + numberOfVolumes]
            mp = Mountpoint(device, mountpoint)
            if (action == "mount"):
                mp.mount()
            else:
                mp.unmount()
            count = count + 1

def usage():
    print """\nMount or unmount a given list of volumes to their respective mountpoints\n
    usage: mount_init.py <volumes> <mountpoints> [mount|umount]
    """



class Mountpoint:
    def __init__(self, device, mountpoint):
        self.device = device
        self.mountpoint = mountpoint

    def __del__(self):
        pass

    def mount(self):
        """Mount the device to a specific location"""
        d = self.device
        mp = self.mountpoint
        print("Mounting {0} @ {1} ...".format(d, mp))

        Popen(["mkdir", mp], stdout=subprocess.PIPE).wait()
        Popen(["mount", "-t", "xfs", "-o", "defaults", d, mp], stdout=subprocess.PIPE).wait()

        #cmd = ['/run/myscript', '--arg', 'value']
        #p = subProcess.Popen(cmd, stdout=subprocess.PIPE)
        #for line in p.stdout:
        #    print line
        #p.wait()
        #print p.returncode


    def unmount(self):
        """Umount the specific location"""
        mp = self.mountpoint
        print("Umounting {0} ...".format(mp))

        Popen(["umount", "-t", "xfs", mp], stdout=subprocess.PIPE).wait()



if __name__ == '__main__':
    main(sys.argv[1:])