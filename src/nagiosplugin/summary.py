# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from .state import Ok


class Summary(object):

    def ok(self, results):
        return str(results[0])

    def problem(self, results):
        try:
            return str(results.first_significant)
        except IndexError:
            return 'no check results'

    def verbose(self, results):
        msgs = []
        for result in results:
            if result.state == Ok:
                continue
            msgs.append('{}: {}'.format(result.state, result))
        return msgs
