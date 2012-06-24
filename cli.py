import cmd

from tools.config import Config

class ToolKit(cmd.Cmd):
    """Simple command processor example."""

    # display (user-data)

    def do_display(self, line):
        config = Config.fromAmazon()
        print config.data

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
    ToolKit().cmdloop("\nWelcome to the 9apps ToolKit cli.\n")