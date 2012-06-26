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

import traceback
import sys
import pystache

from boto.ec2.connection import EC2Connection
from config import Config
from bashcmd import BashCmd

class EIP:
    def __init__(self, config):
        self.config = config
        try:
            # we use IAM EC2 role to get the credentials transparently
            ec2 = EC2Connection(region=config.regionInfo)
            ip = config.userData['eip']['ip']
            eip = ec2.get_all_addresses([ip])[0]
            print "Elastic IP: {0}".format(eip)

            self.eip = eip
        except Exception as e:
            print("ERROR - Problem retrieving the desired EIP: {0}".format(e))
            print traceback.format_exc()


    def associate(self):
        result = False
        eip = ""
        instanceId = ""
        try:
            eip = self.eip
            instanceId = self.config.instanceId
            if eip.instance_id == "":
                result = eip.associate(instanceId)

                if result:
                    print "{0} is now associated to instance {1}".format(eip, instanceId)
                else:
                    print "ERROR - Problem while associating {0} to instance {1}".format(eip, instanceId)
            else:
                # if the elastic IP is already taken, then don't do anything
                print "WARN - {0} is already in use by instance {1}".format(eip, eip.instance_id)
        except Exception as e:
            print("ERROR - We couldn't associate {0} to this instance {1}: {2}".format(eip, instanceId, e))
            print traceback.format_exc()
        return result


    def disassociate(self):
        result = False
        eip = ""
        instanceId = ""
        try:
            eip = self.eip
            instanceId = self.config.instanceId
            associated_instance_id = eip.instance_id
            if associated_instance_id == "":
                print "{0} is already free, doing nothing".format(eip)
            elif associated_instance_id != instanceId:
                print "WARN - {0} is associated to another instance {1} - doing nothing".format(eip,
                    associated_instance_id)
            else:
                # the EIP is associated to this instance, disassociate it
                result = eip.disassociate()

                if result:
                    print "{0} has been disassociated".format(eip)
                else:
                    print "ERROR - There was a problem while dissociating EIP {0} to instance {1}".format(eip,
                        instanceId)
        except Exception as e:
            print("ERROR - We couldn't disassociate {0} to this instance {1}: {2}".format(eip, instanceId, e))
            print traceback.format_exc()
        return result

    INITD_TEMPLATE = "templates/initd.mustache"

    initdPath = "/etc/init.d/"
    initdName = "eip"
    initdFile = initdPath + initdName


    def install_initd(self):
        result = False
        #render initd template
        renderArgs = {
            "provides" : "EC2 Elastic IP provisioning",
            "short_description" : "EIP housekeeping",
            "description" : "Associate and disassociate EIP to/from this instance",
            "py_script" : "eip.py",
            "start_args" : "associate",
            "stop_args" : "disassociate"
        }
        initdContent = pystache.render(open(self.INITD_TEMPLATE, "r").read(), renderArgs)

        # write initd file
        open(self.initdFile, "w").write(initdContent)

        # change permission and update-rc.d
        chmod = BashCmd(["/bin/chmod", "700", self.initdFile])
        chmod.execute()
        if chmod.isOk():
            updaterc = BashCmd(["/usr/sbin/update-rc.d", self.initdName, "defaults"])
            updaterc.execute()
            if updaterc.isOk():
                result = True
                print "{0} installed correctly".format(self.initdFile)
            else:
                print "ERROR - Problem installing {0}, {1}".format(self.initdFile, updaterc)
        else:
            print "ERROR - Problem setting permission on {0}, {1}".format(self.initdFile, chmod)
        return result


    def uninstall(self):
        result = False
        # remove initd file and update-rc.d
        rm = BashCmd(["/bin/rm", self.initdFile])
        rm.execute()
        if rm.isOk():
            updaterc = BashCmd(["/usr/sbin/update-rc.d", self.initdName, "remove"])
            updaterc.execute()
            if updaterc.isOk():
                result = True
                print "{0} uninstalled correctly".format(self.initdFile)
            else:
                print "ERROR - Problem uninstalling {0}, {1}".format(self.initdFile, updaterc)
        else:
            print "ERROR - Problem deleting {0}, {1}".format(self.initdFile, rm)
        return result


if __name__ == '__main__':
    config = Config.fromAmazon()
    eip = EIP(config)
    action = sys.argv[1]
    if action == "associate":
        eip.associate()
    elif action == "disassociate":
        eip.disassociate()