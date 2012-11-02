# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

import pkg_resources
import re
import subprocess
import sys
import unittest


class ExamplesTest(unittest.TestCase):

    def test_integration(self):
        for program, regexp in [
            ('check_load.py', """\
LOAD OK - loadavg is [0-9., ]+
| load15=[0-9.]+;;;0 load1=[0-9.]+;;;0 load5=[0-9.]+;;;0
"""),
            ('check_users.py', """\
USERS OK - \\d+ users logged in
users: .*
| total=\\d+;;;0 unique=\\d+;;;0
""")]:
            p = subprocess.Popen([
                sys.executable, pkg_resources.resource_filename(
                    'examples', program), '-v'], stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            out, err = p.communicate()
            self.assertTrue(re.match(regexp, out.decode()) is not None,
                            '"{}" does not match "{}"'.format(
                                out.decode(), regexp))
            self.assertEqual(err.decode(), '')
            self.assertEqual(0, p.returncode)
