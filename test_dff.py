#!/usr/bin/python3
import stat
import os
import shutil
import unittest
from dff import dff, clear_globals_for_unittests, set_verbose_output, set_output_immediately, set_trial_delete, set_delete_shorter
from stat import S_IREAD, S_IRGRP, S_IROTH
version = "0.9.0"


# self.assertTrue(exp)
# self.assertEqual(a,b)
# self.assertContains(response, 'must supply test_name')
# self.assertRegex(response.content.decode('utf-8'), 'Test Passed: True')
# self.assertNotRegex(response.content.decode('utf-8'), 'delete id test')


def one_time_setup():
    set_verbose_output(True)
    set_output_immediately(False)
    set_trial_delete(True)
    set_delete_shorter(False)


class Testdff(unittest.TestCase):

    def setUp(self):
        clear_globals_for_unittests()
        pass

    def tearDown(self):
        pass

    def test_verbose_output_enabled(self):
        response = dff('test/one_file')
        self.assertRegex(response, 'Checking size of file')

    def test_find_small_file_duplicate(self):
        response = dff('test/one_small_duplicate')
        self.assertRegex(response, 'calculating hash snippet')
        self.assertRegex(
            response, 'bbb.txt\n is dupe of test.one_small_duplicate.aaa.txt')

    def test_find_two_small_file_duplicates(self):
        response = dff('test/two_small_duplicates')
        self.assertRegex(
            response, 'bbb.txt\n is dupe of test.two_small_duplicates.aaa.txt')
        self.assertRegex(
            response, 'ccc.txt\n is dupe of test.two_small_duplicates.aaa.txt')
        self.assertNotRegex(response, 'aaa.txt\n is dupe of')

    def test_find_large_file_duplicate(self):
        response = dff('test/one_large_duplicate')
        self.assertRegex(
            response, 'big bbb.txt\n is dupe of test.one_large_duplicate.big aaa.txt')
        self.assertRegex(response, 'calculating full hash')
        self.assertNotRegex(response, 'big aaa.txt\n is dupe')

    def test_find_two_large_file_duplicates(self):
        response = dff('test/two_large_duplicates')
        self.assertRegex(
            response, 'big bbb.txt\n is dupe of test.two_large_duplicates.big aaa.txt')
        self.assertRegex(
            response, 'big ccc.txt\n is dupe of test.two_large_duplicates.big aaa.txt')
        self.assertNotRegex(response, 'big aaa.txt\n is dupe')

    def test_do_not_find_large_file_almost_duplicate(self):
        response = dff('test/one_large_almost_duplicate')
        self.assertNotRegex(response, 'is dupe of')
        self.assertRegex(response, 'but files are different')

    def test_do_not_find_many_large_files_almost_duplicate(self):
        response = dff('test/many_large_almost_duplicate')
        self.assertNotRegex(response, 'is dupe of')
        self.assertRegex(response, 'but files are different')

    def test_search_sub_folders(self):
        response = dff('test')
        self.assertRegex(response, 'is dupe of')
        self.assertRegex(response, 'but files are different')

    def test_duplicate_across_folders(self):
        response = dff('test/duplicate_across_folders')
        self.assertRegex(
            response, 'sub1.dupe.txt\n is dupe of test.duplicate_across_folders.master.txt')
        self.assertRegex(
            response, 'sub1.supersub.also_dupe.txt\n is dupe of test.duplicate_across_folders.master.txt')
        self.assertRegex(
            response, 'sub2.dupe.txt\n is dupe of test.duplicate_across_folders.master.txt')

    def test_show_count_of_duplicates(self):
        response = dff('test/duplicate_across_folders')
        self.assertRegex(response, '3 duplicate files found')

    def test_show_megabytes_scanned(self):
        response = dff('test/duplicate_across_folders')
        self.assertRegex(response, '0.046875 megabytes scanned')

    def test_delete_duplicates_trial(self):
        response = dff('test/duplicate_across_folders', True)
        self.assertRegex(
            response, 'deleted ... test.duplicate_across_folders.sub1.dupe.txt')
        self.assertRegex(
            response, 'deleted ... test.duplicate_across_folders.sub1.supersub.also_dupe.txt')
        self.assertRegex(
            response, 'deleted ... test.duplicate_across_folders.sub2.dupe.txt')

    def test_count_of_examined_files(self):
        response = dff('test/duplicate_across_folders')
        self.assertRegex(response, '4 files and')

    def test_delete_read_only_file(self):
        try:
            os.chmod('test/delete_unit_test/bbb.txt', stat.S_IWRITE)
        except FileNotFoundError:
            pass
        # Why is this so unreliable ???
        shutil.rmtree('test/delete_unit_test', ignore_errors=True)
        shutil.rmtree('test/delete_unit_test', ignore_errors=True)
        shutil.rmtree('test/delete_unit_test', ignore_errors=True)
        try:
            shutil.copytree('test/one_small_duplicate',
                            'test/delete_unit_test')
        except PermissionError:
            print('Got some really wierd permission error - try again')
            shutil.copytree('test/one_small_duplicate',
                            'test/delete_unit_test')
        os.chmod('test/delete_unit_test/bbb.txt', S_IREAD | S_IRGRP | S_IROTH)
        set_trial_delete(False)
        response = dff('test/delete_unit_test', True)
        set_trial_delete(True)
        self.assertRegex(response, 'deleted ... test.delete_unit_test.bbb.txt')

    def test_show_start_and_end_times(self):
        response = dff('test/duplicate_across_folders')
        self.assertRegex(response, '\d{2}:\d{2}:\d{2}')

    def test_show_run_time_in_seconds(self):
        response = dff('test/duplicate_across_folders')
        self.assertRegex(response, 'in \d+\.\d+ seconds')

    def test_delete_file_with_longest_name(self):
        shutil.rmtree('test/delete_filename_length', ignore_errors=True)
        shutil.rmtree('test/delete_filename_length', ignore_errors=True)
        shutil.rmtree('test/delete_filename_length', ignore_errors=True)
        shutil.copytree('test/filename_length', 'test/delete_filename_length')
        set_delete_shorter(True)
        set_trial_delete(False)
        response = dff('test/delete_filename_length', True)
        set_delete_shorter(False)
        set_trial_delete(True)
        self.assertRegex(
            response, 'deleted ... test.delete_filename_length.bbbb.txt')
        self.assertRegex(
            response, 'deleted ... test.delete_filename_length.cc.txt')
        self.assertRegex(response, 'aaaaaa.txt ... deleted')
        self.assertRegex(
            response, 'deleted ... test.delete_filename_length.ee.txt')
        self.assertRegex(response, 'aaaaaa.txt ... already deleted')
        self.assertRegex(
            response, 'failed to delete 1 duplicates - rerun script')

    def test_do_not_process_file_of_unique_byte_size(self):
        response = dff('test/different_file_sizes')
        self.assertNotRegex(response, 'Processing file')

    def test_files_with_non_unique_file_size_added_to_process_list(self):
        response = dff('test/one_large_almost_duplicate')
        self.assertRegex(response, 'big bbb.txt added to process list')
        self.assertRegex(response, 'big aaa.txt added to process list')
        self.assertRegex(response, 'has non unique')

    def test_known_duplicates_not_added_to_list_multiple_times(self):
        response = dff('test/two_small_duplicates')
        self.assertRegex(response, 'aaa.txt is a known size duplicate')
        self.assertRegex(response, 'aaa.txt added to process list')
        self.assertRegex(response, 'bbb.txt added to process list')
        self.assertRegex(response, 'ccc.txt added to process list')

    def test_ignore_zero_byte_files(self):
        response = dff('test/two_zero_byte_files')
        self.assertNotRegex(response, 'Processing file')
        self.assertNotRegex(response, 'is dupe of')


if __name__ == '__main__':
    one_time_setup()
    unittest.main()
