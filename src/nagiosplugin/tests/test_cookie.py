# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.cookie import Cookie
import unittest
import tempfile
import os


class CookieTest(unittest.TestCase):

    def setUp(self):
        self.tf = tempfile.NamedTemporaryFile(prefix='cookietest_')

    def tearDown(self):
        self.tf.close()

    def test_get_default_value_if_empty(self):
        with Cookie(self.tf.name) as c:
            self.assertEqual('default value', c.get('key', 'default value'))

    def test_get_file_contents(self):
        with open(self.tf.name, 'w') as f:
            f.write('{"hello": "world"}')
        with Cookie(self.tf.name) as c:
            self.assertEqual('world', c['hello'])

    def test_get_without_open_should_raise_keyerror(self):
        c = Cookie(self.tf.name)
        with self.assertRaises(KeyError):
            c['foo']

    def test_set_should_write_content(self):
        with Cookie(self.tf.name) as c:
            c['inode'] = 188219
        with open(self.tf.name) as f:
            self.assertEqual('{\n "inode": 188219\n}', f.read())

    def test_should_not_commit_on_exception(self):
        try:
            with Cookie(self.tf.name) as c:
                c['foo'] = True
                raise RuntimeError()
        except RuntimeError:
            pass
        with open(self.tf.name) as f:
            self.assertEqual('', f.read())

    def test_should_not_create_file_unless_value_set(self):
        with Cookie(self.tf.name + '.new') as c:
            pass
        self.assertFalse(os.path.exists(self.tf.name + '.new'))

    def test_double_close_raises_no_exception(self):
        with Cookie(self.tf.name) as c:
            c.close()
        self.assertTrue(True)
