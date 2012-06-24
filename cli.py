import cmd

from tools.config import Config
from tools.eip import EIP

class ToolKit(cmd.Cmd):
    """Simple command processor example."""

    def do_display(self, line):
        config = Config.fromAmazon()
        print config.data

    ###############

    EIP_COMMANDS = ["associate", "disassociate"]

    def help_eip(self):
        print '\n'.join(["eip {0}".format(self.EIP_COMMANDS), " Associate or disassociate EIP configured in user-data"])

    def complete_eip(self, text, line, begidx, endidx):
        if not text:
            completions = self.EIP_COMMANDS[:]
        else:
            completions = [ f
                            for f in self.EIP_COMMANDS
                            if f.startswith(text)
                            ]
        return completions

    def do_eip(self, cmd):
        config = Config.fromAmazon()
        eip = EIP.fromAmazon(config)
        if cmd == self.EIP_COMMANDS[0]:
            eip.associate()
        elif cmd == self.EIP_COMMANDS[1]:
            eip.disassociate()

    ###############

    # backup setup (or install)

    # eip associate, dissociate, install, uninstall

    # mount -, install, uninstall

    # umount

    def do_greet(self, person):
        if person:
            print "hi,", person
        else:
            print 'hi'

    def help_greet(self):
        print '\n'.join(['greet [person]', ' Greet the named person'])

    FRIENDS = [ 'Alice', 'Adam', 'Barbara', 'Bob' ]

    def complete_greet(self, text, line, begidx, endidx):
        if not text:
            completions = self.FRIENDS[:]
        else:
            completions = [ f
                            for f in self.FRIENDS
                            if f.startswith(text)
                            ]
        return completions


    def do_EOF(self, line):
        print "Exit"
        return True


    def postloop(self):
        print

if __name__ == '__main__':
    ToolKit().cmdloop("\nWelcome to the 9apps ToolKit CLI.\n")