import traceback
import subprocess
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
