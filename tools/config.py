from urllib2 import urlopen
import json

class Config:

    def __init__(self, config):
        """Initialize Config"""
        self.data = config

    def __repr__(self):
        return json.dumps(self.data, sort_keys=True, indent=4)

    @classmethod
    def fromFile(cls, filename):
        """Load user-data from file"""
        data = open(filename).readlines()
        return cls(data)

    @classmethod
    def fromAmazon(cls):
        """Load user-data from aws"""
        try:
            url = "http://169.254.169.254/latest/"
            data = json.load(urlopen(url + "user-data/", timeout=3))
            return cls(data)
        except Exception as e:
            print e
            exit("ERROR - We couldn't get user-data.")
