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

from urllib2 import urlopen

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
            instanceId = urlopen(url + "meta-data/instance-id").read()
            region = urlopen(url + "meta-data/placement/availability-zone").read()[:-1]
            endpoint = "ec2.{0}.amazonaws.com".format(region)
            region_info = RegionInfo(name=region, endpoint=endpoint)
            print "Instance: {0} in Region: {1}".format(instanceId, region_info.endpoint)

            # we use IAM EC2 role to get the credentials transparently
            ec2 = EC2Connection(region=region_info)
            ip = config.data['eip']['ip']
            eip = ec2.get_all_addresses([ip])[0]
            print "Elastic IP: {0}".format(eip)
            return cls(instanceId, eip)
        except Exception as e:
            print("ERROR - We couldn't get instance information: {0}".format(e))
        finally:
            print traceback.format_exc()


    def associate(self):
        result = False
        eip = self.eip
        instanceId = self.instanceId
        try:
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
        finally:
            print traceback.format_exc()
        return result


    def disassociate(self):
        result = False
        eip = self.eip
        instanceId = self.instanceId
        associated_instance_id = eip.instance_id
        try:
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
        finally:
            print traceback.format_exc()
        return result


    def install(self):
        # TODO install initd
        return False


    def uninstall(self):
        # TODO uninstall initd
        return False