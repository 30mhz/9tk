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

import  urllib2

from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import RegionInfo

class EIP:
    def __init__(self, instanceId, eip):
        self.instanceId = instanceId
        self.eip = eip

    @classmethod
    def mock(cls, instanceId, eip):
        return cls(instanceId, eip)

    @classmethod
    def fromAmazon(cls, config):
        url = "http://169.254.169.254/latest/"
        try:
            instanceId = urllib2.urlopen(url + "meta-data/instance-id").read()
            region = urllib2.urlopen(url + "meta-data/placement/availability-zone").read()
            region_info = RegionInfo(name=region, endpoint="ec2.{0}.amazonaws.com".format(region))

            # TODO we use IAM EC2 role to get the credentials transparently

            key = userdata['access_key_id']
            access = userdata['secret_access_key']
            ec2 = EC2Connection(key, access, region=region_info)
            eip = ec2.get_all_addresses(config.data['eip']['ip'])[0]
            return cls(instanceId, eip)
        except Exception as e:
            print e
            exit("We couldn't get instance information.")


    def associate(self):
        result = False
        eip = self.eip
        if eip.instance_id == "":
            result = eip.associate(self.instanceId)
            if result:
                print "EIP {0} is now associated to instance {1}".format(eip, self.instanceId)
            else:
                print "ERROR - There was a problem while associating EIP {0} to instance {1}".format(eip, self.instanceId)
        else:
            # if the elastic IP is already taken, then don't do anything
            print "WARN - EIP {0} is already in use by instance {1}".format(eip, eip.instance_id)
        return result

    def disassociate(self):
        result = False
        eip = self.eip
        associated_instance_id = eip.instance_id
        if associated_instance_id == "":
            print "EIP is already free, doing nothing"
        elif associated_instance_id != self.instanceId:
            print "WARN - EIP {0} is associated to another instance {1} - doing nothing".format(eip, associated_instance_id)
        else:
            # the EIP is associated to this instance, disassociate it
            result = eip.disassociate()
            if result:
                print "EIP {0} has been disassociated".format(eip)
            else:
                print "ERROR - There was a problem while dissociating EIP {0} to instance {1}".format(eip, self.instanceId)
        return result