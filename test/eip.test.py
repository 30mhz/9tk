import unittest
import mock

from boto.ec2.address import Address

from eip import EIP

class EIPTest(unittest.TestCase):
    example = "../config/userdata.txt"

    def test_eip(self):
        address = Address()
        connection = mock.Mock()
        connection.get_status = True
        connection.associate_address = mock.Mock()
        address.connection = connection
        address.instance_id = ""

        expectedInstanceId="instance-id"
        eip = EIP.mock(expectedInstanceId, address)
        self.assertEqual(eip.associate(), True)


    #def dummy_urlopen(url):
    #    ...
    #
    #eip.urllib2.urlopen = dummy_urlopen


if __name__ == '__main__':
    unittest.main()