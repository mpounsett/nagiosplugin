#!python

"""Hello world Nagios check."""

import nagiosplugin


class World(nagiosplugin.Resource):

    def probe(self):
        return [nagiosplugin.Metric('world', True, context='null')]


def main():
    check = nagiosplugin.Check(World())
    check.main()


if __name__ == '__main__':
    main()
