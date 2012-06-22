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

import  sys
import  urllib2

from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import RegionInfo

# parameters:
# - elastic ip
# - "start"/"stop"

try:
    url = "http://169.254.169.254/latest/"
    #userdata = json.load(urllib2.urlopen(url + "user-data"))
    instance_id = urllib2.urlopen(url + "meta-data/instance-id").read()
    region = urllib2.urlopen(url + "meta-data/placement/availability-zone").read()[:-1]
except Exception as e:
    print e
    exit("We couldn't get user-data or other meta-data...")

if __name__ == '__main__':
    region_info = RegionInfo(name=region, endpoint="ec2.{0}.amazonaws.com".format(region))
    # we use IAM EC2 role to get the credentials transparently
    ec2 = EC2Connection(region=region_info)

    address = ec2.get_all_addresses(sys.argv[1])[0]

if sys.argv[2] == "start":
    if address.instance_id == "":
        address.associate(instance_id)
        print "Elastic IP (" + address + ") is now associated"
    else:
        # if the elastic IP is already taken, then don't do anything
        print "WARN - Elastic IP is already in use by instance: " + address.instance_id

if sys.argv[2] == "stop":
    associated_instance_id = address.instance_id
    if associated_instance_id == "":
        print "Elastic IP is already free, doing nothing"
    elif associated_instance_id != instance_id:
        print "WARN - Elastic IP is associated to another instance (" + associated_instance_id + ") - doing nothing"
    else:
        # the EIP is associated to this instance, disassociate it
        address.disassociate()
        print "Elastic IP has been disassociated"
