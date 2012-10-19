# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from .state import Ok
import logging


class Summary:

    def ok(self, results):
        return str(results.first_significant())

    def problem(self, results):
        return str(results.first_significant())

    def verbose(self, results):
        for state in reversed(sorted(results.by_state.keys())):
            if state == Ok:
                continue
            for result in results.by_state[state]:
                logging.info('%s: %s', state, result)
