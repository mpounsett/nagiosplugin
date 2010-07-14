# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import optparse


class PluginOptionParser(optparse.OptionParser):

    def exit(self, status=0, msg=None):
        pass
