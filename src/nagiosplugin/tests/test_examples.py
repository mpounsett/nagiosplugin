# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

import pkg_resources
import re
import subprocess
import sys
import os.path as p

try:
    import unittest2 as unittest
except ImportError:  # pragma: no cover
    import unittest


class ExamplesTest(unittest.TestCase):
    base = p.normpath(p.join(p.dirname(p.abspath(__file__)), '..', '..'))

    def _run_example(self, program, regexp):
        proc = subprocess.Popen([
            sys.executable, pkg_resources.resource_filename(
                'nagiosplugin.examples', program), '-v'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env={'PYTHONPATH': ':'.join(sys.path)})
        out, err = proc.communicate()
        self.assertEqual(err.decode(), '')
        self.assertTrue(re.match(regexp, out.decode()) is not None,
                        '"{0}" does not match "{1}"'.format(
                            out.decode(), regexp))
        self.assertEqual(0, proc.returncode)

    def test_check_load(self):
        if not sys.platform.startswith('linux'):  # pragma: no cover
            self.skipTest('requires Linux')
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
