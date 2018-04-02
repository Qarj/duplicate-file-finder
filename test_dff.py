#!/usr/bin/env python3
version="0.0.5"

import unittest
from dff import dff, clear_globals_for_unittests, set_verbose_output, set_output_immediately, set_trial_delete

# self.assertTrue(exp)
# self.assertEqual(a,b)
# self.assertContains(response, 'must supply test_name')
# self.assertRegex(response.content.decode('utf-8'), 'Test Passed: True')
# self.assertNotRegex(response.content.decode('utf-8'), 'delete id test')

def one_time_setup():
    set_verbose_output(True)
    set_output_immediately(False)
    set_trial_delete(True)

class Testdff(unittest.TestCase):

    def setUp(self):
        clear_globals_for_unittests()
        pass
       
    def tearDown(self):
        pass

    def test_verbose_output_enabled(self):
        response = dff('test/one_file')
        self.assertRegex (response, 'Started searching in')

    def test_find_small_file_duplicate(self):
        response = dff('test/one_small_duplicate')
        self.assertRegex (response, 'calculating md5 snippet')
        self.assertRegex (response, 'bbb.txt is a duplicate of test.one_small_duplicate.aaa.txt')

    def test_find_two_small_file_duplicates(self):
        response = dff('test/two_small_duplicates')
        self.assertRegex (response, 'bbb.txt is a duplicate of test.two_small_duplicates.aaa.txt')
        self.assertRegex (response, 'ccc.txt is a duplicate of test.two_small_duplicates.aaa.txt')
        self.assertNotRegex (response, 'aaa.txt is a duplicate of')
   
    def test_find_large_file_duplicate(self):
        response = dff('test/one_large_duplicate')
        self.assertRegex (response, 'big bbb.txt is a duplicate of test.one_large_duplicate.big aaa.txt')
        self.assertRegex (response, 'calculating md5 full')
        self.assertNotRegex (response, 'big aaa.txt is a duplicate')

    def test_find_two_large_file_duplicates(self):
        response = dff('test/two_large_duplicates')
        self.assertRegex (response, 'big bbb.txt is a duplicate of test.two_large_duplicates.big aaa.txt')
        self.assertRegex (response, 'big ccc.txt is a duplicate of test.two_large_duplicates.big aaa.txt')
        self.assertNotRegex (response, 'big aaa.txt is a duplicate')

    def test_do_not_find_large_file_almost_duplicate(self):
        response = dff('test/one_large_almost_duplicate')
        self.assertNotRegex (response, 'is a duplicate of')
        self.assertRegex (response, 'but files are different')

    def test_do_not_find_many_large_files_almost_duplicate(self):
        response = dff('test/many_large_almost_duplicate')
        self.assertNotRegex (response, 'is a duplicate of')
        self.assertRegex (response, 'but files are different')

    def test_search_sub_folders(self):
        response = dff('test')
        self.assertRegex (response, 'is a duplicate of')
        self.assertRegex (response, 'but files are different')

    def test_duplicate_across_folders(self):
        response = dff('test/duplicate_across_folders')
        self.assertRegex (response, 'sub1.dupe.txt is a duplicate of test.duplicate_across_folders.master.txt')
        self.assertRegex (response, 'sub1.supersub.also_dupe.txt is a duplicate of test.duplicate_across_folders.master.txt')
        self.assertRegex (response, 'sub2.dupe.txt is a duplicate of test.duplicate_across_folders.master.txt')

    def test_show_count_of_duplicates(self):
        response = dff('test/duplicate_across_folders')
        self.assertRegex (response, '3 duplicate files found')

    def test_show_megabytes_scanned(self):
        response = dff('test/duplicate_across_folders')
        self.assertRegex (response, '0.0625 megabytes scanned')

    def test_delete_duplicates_trial(self):
        response = dff('test/duplicate_across_folders', True)
        self.assertRegex (response, 'deleted ... test.duplicate_across_folders.sub1.dupe.txt')
        self.assertRegex (response, 'deleted ... test.duplicate_across_folders.sub1.supersub.also_dupe.txt')
        self.assertRegex (response, 'deleted ... test.duplicate_across_folders.sub2.dupe.txt')

if __name__ == '__main__':
    one_time_setup()
    unittest.main()
