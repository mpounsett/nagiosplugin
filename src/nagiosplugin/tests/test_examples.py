# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

import pkg_resources
import re
import subprocess
import sys
import unittest
import os.path as p

base_path = p.normpath(p.join(p.dirname(p.abspath(__file__)), '..', '..'))


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
            proc = subprocess.Popen([
                sys.executable, pkg_resources.resource_filename(
                    'examples', program), '-v'], stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, env={'PYTHONPATH': base_path})
            out, err = proc.communicate()
            self.assertEqual(err.decode(), '')
            self.assertTrue(re.match(regexp, out.decode()) is not None,
                            '"{}" does not match "{}"'.format(
                                out.decode(), regexp))
            self.assertEqual(0, proc.returncode)
