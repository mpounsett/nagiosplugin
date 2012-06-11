# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin
import nagiosplugin.state


class HelloWorldCheck(nagiosplugin.Check):

    name = 'World'
    version = '1.0'

    def obtain_data(self):
        self.world = True

    def states(self):
        if self.world:
            return [nagiosplugin.state.Ok()]


main = nagiosplugin.Controller(HelloWorldCheck)
