import traceback

from urllib2 import urlopen
import json

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
