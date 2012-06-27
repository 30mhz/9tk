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

import traceback, subprocess
from subprocess import Popen

class BashCmd:

    def __init__(self, cmdArgs):
        self.cmdArgs = cmdArgs

    def execute(self):
        out_list = []
        try:
            p = Popen(self.cmdArgs, stdout=subprocess.PIPE)
            for line in p.stdout:
                out_list.append(line)
            p.wait()
            self.output = "".join(out_list)
            self.returnCode = p.returncode
        except Exception as e:
            print("ERROR - Problem running {0}: {1}".format(self.cmdArgs, e))
            print traceback.format_exc()

    def __repr__(self):
        return "\nReturn code: {0}\nOutput: {1}".format(self.returnCode, self.output)

    def isOk(self):
        if self.returnCode == 0:
            return True
        else:
            return False
