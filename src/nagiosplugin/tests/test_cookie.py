# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

import os
import os.path
import unittest
from nagiosplugin.cookie import Cookie, store


class CookieTest(unittest.TestCase):

    def test_init_creates_file(self):
        c = Cookie('cookietest', '.')
        self.assert_(os.path.exists('cookietest'),
                     u"file 'cookietest' does not exist")
        os.unlink('cookietest')

    def test_dir(self):
        if not os.path.exists('testdir'):
            os.mkdir('testdir')
        c = Cookie('cookietest', 'testdir')
        self.assert_(os.path.exists('testdir/cookietest'),
                     u"file 'testdir/cookietest' does not exist")
        os.unlink('testdir/cookietest')
        os.rmdir('testdir')

    def test_dir_defaults_to_home(self):
        c = Cookie('cookietest')
        self.assertEqual(os.path.expanduser('~'),
                         os.path.dirname(c.filename))
        os.unlink(os.path.expanduser('~/cookietest'))

    def test_close_removes_file_if_no_value_set(self):
        try:
            os.unlink('cookietest')
        except OSError:
            pass
        c = Cookie('cookietest')
        c.close()
        self.failIf(os.path.exists('cookietest'),
                    u"file 'cookietest' does exist but shouldn't")

    def test_nonexistent_dir_should_fail(self):
        self.assertRaises(IOError, Cookie, 'cookietest', '/no/such/directory')


class CookieStoreTest(unittest.TestCase):

    def tearDown(self):
        try:
            os.unlink('cookietest')
        except OSError:
            pass

    def test_context(self):
        with store('cookietest') as c:
            self.assert_(isinstance(c, Cookie),
                         u'%r should be a Cookie instance' % c)

    def test_get(self):
        with file('cookietest', 'w') as f:
            print >>f, u'value'
        with store('cookietest', '.') as c:
            self.assertEqual(u'value\n', c.get())

    def test_get_defaultvalue(self):
        with store('cookietest', '.') as c:
            self.assertEqual(u'default\n', c.get('default\n'))

    def test_set(self):
        with store('cookietest', '.') as c:
            c.set('value1\n')
        self.assertEqual('value1\n', file('cookietest').read())

    def test_set_should_append_newline(self):
        with store('cookietest', '.') as c:
            c.set('value2')
        self.assertEqual('value2\n', file('cookietest').read())

    def test_setting_the_same_value_should_not_change_mtime(self):
        with file('cookietest', 'w') as f:
            print >>f, u'value3'
        before = os.stat('cookietest').st_mtime
        with store('cookietest', '.') as c:
            c.set(c.get())
        self.assertEqual(os.stat('cookietest').st_mtime, before)


def suite():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CookieTest)
    suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(CookieStoreTest))
    return suite


if __name__ == '__main__':
    unittest.main()
