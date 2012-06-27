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

import pystache

from bashcmd import BashCmd

class Initd:

    INITD_TEMPLATE = "./initd.mustache"
    INITD_DIR = "/etc/init.d/"

    def __init__(self, name):
        self.name = name
        self.path = self.INITD_DIR + self.name

    def install(self, renderArgs):
        result = False

        #render initd template
        initdContent = pystache.render(open(self.INITD_TEMPLATE, "r").read(), renderArgs)

        # write initd file
        open(self.path, "w").write(initdContent)

        # change permission
        chmod = BashCmd(["/bin/chmod", "700", self.path])
        chmod.execute()
        if chmod.isOk():
            #update-rc.d install initd
            updaterc = BashCmd(["/usr/sbin/update-rc.d", self.name, "defaults"])
            updaterc.execute()
            if updaterc.isOk():
                result = True
                print "{0} installed correctly".format(self.path)
            else:
                print "ERROR - Problem installing {0}, {1}".format(self.path, updaterc)
        else:
            print "ERROR - Problem setting permission on {0}, {1}".format(self.path, chmod)
        return result

    def uninstall(self):
        result = False

        # remove initd file
        rm = BashCmd(["/bin/rm", self.path])
        rm.execute()
        if rm.isOk():
            #update-rc.d remove initd
            updaterc = BashCmd(["/usr/sbin/update-rc.d", self.name, "remove"])
            updaterc.execute()
            if updaterc.isOk():
                result = True
                print "{0} uninstalled correctly".format(self.path)
            else:
                print "ERROR - Problem uninstalling {0}, {1}".format(self.path, updaterc)
        else:
            print "ERROR - Problem deleting {0}, {1}".format(self.path, rm)
        return result