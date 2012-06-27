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

import traceback, json

from urllib2 import urlopen
from boto.ec2.regioninfo import RegionInfo

class Config:

    def __init__(self, instanceId, regionInfo, userData):
        """Initialize Config"""
        self.instanceId = instanceId
        self.regionInfo = regionInfo
        self.userData = userData

    def __repr__(self):
        return "InstanceId: {0}\n{1}\nUserData: {2}".format(self.instanceId, self.regionInfo, json.dumps(self.userData, indent=4))

    @classmethod
    def fromFile(cls, filename):
        """Load user-data from file"""
        userData = open(filename).readlines()
        return cls("i-instanceId", "aws-region", userData)

    @classmethod
    def fromAmazon(cls):
        """Load meta-data and user-data using AWS"""
        try:
            url = "http://169.254.169.254/latest/"

            instanceId = urlopen(url + "meta-data/instance-id", timeout=1).read()
            region = urlopen(url + "meta-data/placement/availability-zone", timeout=1).read()[:-1]
            endpoint = "ec2.{0}.amazonaws.com".format(region)
            regionInfo = RegionInfo(name=region, endpoint=endpoint)

            userData = json.load(urlopen(url + "user-data/", timeout=1))

            return cls(instanceId, regionInfo, userData)
        except Exception as e:
            print("ERROR - Problem retrieving instance user-data or meta-data: {0}".format(e))
            print traceback.format_exc()
