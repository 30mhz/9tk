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

import sys, traceback, time

from boto.ec2.connection import EC2Connection

from config import Config
from util.bashcmd import BashCmd
from util.initd import Initd

class Volume:
    def __init__(self, config):
        self.config = config
        try:
            # we use IAM EC2 role to get the credentials transparently
            self.ec2 = EC2Connection(region=config.regionInfo)
        except Exception as e:
            print("ERROR - Problem connecting to EC2: {0}".format(e))
            print traceback.format_exc()


    def mount(self):
        #loop through the volumes
        volumes = self.config.userData["volumes"]
        for volumeId in volumes:
            volume = self.ec2.get_all_volumes([volumeId])[0]
            print "Volume {0} status: {1}".format(volume.id, volume.status)

            device = volumes[volumeId]["device"]
            mountpoint = volumes[volumeId]["mountpoint"]

            # attach the volume to the instance in case is not in use
            if volume.status == "available":
                print "Attaching volume to device {0} ...".format(device)
                self.ec2.attach_volume(volume.id, self.config.instanceId, device)
                #wait untill the volume is attached
                volume.update()
                while volume.attachment_state() != "attached":
                    time.sleep(3)
                    volume.update()
                    print "volume status: {0}".format(volume.attachment_state())

            #HACK to make it work on Ubuntu 12.04
            dev = device.replace("/dev/s", "/dev/xv")

            # mount the volume to the mountpoint
            print "Mounting {0} @ {1} ...".format(dev, mountpoint)
            BashCmd([ "mkdir", "-p", mountpoint ]).execute()
            mount = BashCmd([ "mount", "-t", "xfs", "-o", "defaults", dev, mountpoint ])
            mount.execute()
            if mount.isOk():
                print "Mountpoint {0} ready".format(mountpoint)
            else:
                print "ERROR - Problem mounting {0}".format(mountpoint)


    def umount(self):
        #loop through the volumes
        volumes = self.config.userData["volumes"]
        for volumeId in volumes:
            volume = self.ec2.get_all_volumes([volumeId])[0]
            print "Volume {0} status: {1}".format(volume.id, volume.status)

            device = volumes[volumeId]["device"]
            mountpoint = volumes[volumeId]["mountpoint"]

            # umount the volume and detach the volume if is in use
            print("Umounting {0} ...".format(mountpoint))
            umount = BashCmd( ["umount", "-t", "xfs", mountpoint] )
            umount.execute()
            if umount.isOk():
                if volume.status == "in-use":
                    print "Detaching volume {0} ...".format(volume.id)
                    self.ec2.detach_volume(volume.id, self.config.instanceId, device)
                else:
                    print "Volume {0} already detached".format(volume.id)
            else:
                print "ERROR - Problem umounting {0}".format(mountpoint)


    INITD_NAME = "volume"

    def install_initd(self):
        renderArgs = {
            "provides" : "EC2 Volume provisioning",
            "short_description" : "Volume housekeeping",
            "description" : "Mount or umount a given list of volumes to their respective mountpoints",
            "py_script" : "volume.py",
            "start_args" : "mount",
            "stop_args" : "umount"
        }
        initd = Initd(self.INITD_NAME)
        return initd.install(renderArgs)


    def uninstall(self):
        initd = Initd(self.INITD_NAME)
        return initd.uninstall()


if __name__ == '__main__':
    config = Config.fromAmazon()
    backup = Volume(config)
    getattr(backup, sys.argv[1])()