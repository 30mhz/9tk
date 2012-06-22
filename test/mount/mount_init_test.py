import os
import unittest

from mount_init import Mountpoint

class TestMountpointSetup(unittest.TestCase):
    fstab = '/tmp/fstab-test'

    def setUp(self):
        """Setup test"""

    def test_fstab(self):
        """Test if the fstab is correctly generated"""
        d = 'TEST_DEVICE'
        m = 'TEST_MOUNTPOINT'
        mountpoint = Mountpoint(d, m)
        mountpoint.setup(self.fstab)
        #
        self.assertEqual(open(self.fstab, "r").read(), '{0} {1} xfs defaults,nobootwait 0 0\n'.format(d, m))

    def tearDown(self):
        """Tear down test"""
        try:
            os.remove(self.fstab)
        except os.error:
            pass


if __name__ == '__main__':
    unittest.main()