# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from .state import Ok
import logging


class Summary:

    def ok(self, results):
        return str(results.first_significant)

    def problem(self, results):
        return str(results.first_significant)

    def verbose(self, results):
        for result in results:
            if result.state == Ok:
                continue
            logging.info('%s: %s', result.state, result)
