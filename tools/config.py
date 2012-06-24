import urllib2

class Config:

    def __init__(self, config):
        """Initialize Config"""
        self.data = config


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
            data = urllib2.urlopen(url + "user-data").read()
            return cls(data)
        except Exception as e:
            print e
            exit("ERROR - We couldn't get user-data.")
