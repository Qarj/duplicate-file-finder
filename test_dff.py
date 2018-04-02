#!/usr/bin/env python3
version="0.0.1"

import unittest
from dff import dff, clear_stdout, set_verbose_output, set_output_immediately

# self.assertTrue(exp)
# self.assertEqual(a,b)
# self.assertContains(response, 'must supply test_name')
# self.assertRegex(response.content.decode('utf-8'), 'Test Passed: True')
# self.assertNotRegex(response.content.decode('utf-8'), 'delete id test')

def one_time_setup():
    set_verbose_output(True)
    set_output_immediately(False)

class Testdff(unittest.TestCase):

    def setUp(self):
        clear_stdout()
        pass
       
    def tearDown(self):
        pass

    def test_verbose_output_enabled(self):
        response = dff('test/empty')
        self.assertRegex (response, 'Started searching in')

    def test_find_small_file_duplicate(self):
        response = dff('test/one_small_duplicate')
        self.assertRegex (response, 'bbb.txt is a duplicate of test/one_small_duplicate/aaa.txt')

if __name__ == '__main__':
    one_time_setup()
    unittest.main()
