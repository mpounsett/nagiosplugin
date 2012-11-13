# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

import pkg_resources
import re
import subprocess
import sys
import unittest
import os.path as p


class ExamplesTest(unittest.TestCase):
    base = p.normpath(p.join(p.dirname(p.abspath(__file__)), '..', '..'))

    def _run_example(self, program, regexp):
        proc = subprocess.Popen([
            sys.executable, pkg_resources.resource_filename(
                'nagiosplugin.examples', program), '-v'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env={'PYTHONPATH': self.base})
        out, err = proc.communicate()
        self.assertEqual(err.decode(), '')
        self.assertTrue(re.match(regexp, out.decode()) is not None,
                        '"{}" does not match "{}"'.format(
                            out.decode(), regexp))
        self.assertEqual(0, proc.returncode)

    def test_check_load(self):
        self._run_example('check_load.py', """\
LOAD OK - loadavg is [0-9., ]+
| load15=[0-9.]+;;;0 load1=[0-9.]+;;;0 load5=[0-9.]+;;;0
""")

    def test_check_users(self):
        self._run_example('check_users.py', """\
USERS OK - \\d+ users logged in
users: .*
| total=\\d+;;;0 unique=\\d+;;;0
""")

    def test_check_world(self):
        self._run_example('check_world.py', '^WORLD OK$')
