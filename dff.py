#!/usr/bin/env python3.6
version="0.7.0"

import sys, argparse, math, hashlib, os, stat, time

# Flags
verbose_output = None
output_immediately = None
trial_delete = None
delete_shorter = None

# Globals
stdout = ''
megabytes_scanned = 0
failed_delete_count = 0

# Constants
BYTES_IN_A_MEGABYTE = 1048576
BYTES_TO_SCAN = 4096
SCAN_SIZE_MB = BYTES_TO_SCAN / BYTES_IN_A_MEGABYTE

def clear_globals_for_unittests():
    global stdout
    global megabytes_scanned
    stdout = ''
    megabytes_scanned = 0

def set_verbose_output(b):
    global verbose_output
    verbose_output = b

def set_output_immediately(b):
    global output_immediately
    output_immediately = b

def set_trial_delete(b):
    global trial_delete
    trial_delete = b

def set_delete_shorter(b):
    global delete_shorter
    delete_shorter = b

class fileFullHash:

    full = dict()

    def __init__(self):
        self.full.clear()

    def search_duplicate(self, snip_file_path, current_file_path):
        current_file_hash = self.hash_full(current_file_path)
        if (current_file_hash in self.full):
            return self.full[current_file_hash]

        snip_file_hash = self.hash_full(snip_file_path)
        self.full[snip_file_hash] = snip_file_path
        if (current_file_hash in self.full):
            return self.full[current_file_hash]

        self.full[current_file_hash] = current_file_path
        return False

    def hash_full(self, file_path):
        global megabytes_scanned
        verbose('...calculating full hash of ' + file_path)
        file_hash = hashlib.blake2b()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(BYTES_TO_SCAN), b""):
                file_hash.update(chunk)
                megabytes_scanned += SCAN_SIZE_MB
        return file_hash.hexdigest()


def hash_snip(file_path):
    global megabytes_scanned
    verbose('...calculating hash snippet of ' + file_path)
    snip_hash = hashlib.blake2b()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(BYTES_TO_SCAN), b""):
                snip_hash.update(chunk)
                f.close()
                megabytes_scanned += SCAN_SIZE_MB
                return snip_hash.hexdigest()
    except PermissionError:
        output ('PermissionError: '+file_path+'\n')
        return 'PermissionError:'+file_path

def verbose(out):
    if (verbose_output):
        return output(out)
    return

def output(out):
    global stdout
    if (output_immediately):
        unicode_output(out)
    else:
        stdout += out + "\n"

def unicode_output(out):
    # when printing directly to the windows console stdout, unicode errors tend to be ignored automatically
    # if the user redirects stdout to a file, unicode errors can occurr - this code outputs the best it can and flags errors in the output
    try:
        print(out, flush=True)
    except UnicodeEncodeError:
        try:
            print(out.encode('utf8').decode(sys.stdout.encoding))
        except UnicodeDecodeError:
            print(out.encode('utf8').decode(sys.stdout.encoding, errors='ignore')  + ' <-- UnicodeDecodeError')

def dff(path, delete_duplicates=False):
    output('\n' + time.strftime('%X : ') +  'Finding duplicate files at ' + path + '\n')
    start_time = time.time()

    snip = dict()
    full_hash = fileFullHash()

    duplicate_count = 0
    file_count = 0

    for root, dirs, files in os.walk(path):
        files.sort()
        for file_name in files:
            file_count += 1
            current_file_path = os.path.join(root,file_name)
            verbose('Processing file ' + current_file_path)
            current_file_snip_hash = hash_snip(current_file_path)
            if (current_file_snip_hash in snip):
                dupe_file_path = full_hash.search_duplicate(snip[current_file_snip_hash], current_file_path)
                if (dupe_file_path):
                    display_duplicate_and_optionally_delete(dupe_file_path, current_file_path, delete_duplicates)
                    duplicate_count += 1
                else:
                    verbose('...first 4096 bytes are the same, but files are different')
            else:
                snip[current_file_snip_hash] = current_file_path

    output('\n' + time.strftime('%X : ') + str(duplicate_count) + ' duplicate files found, ' + str(file_count) + ' files and ' + str(megabytes_scanned) + ' megabytes scanned in ' + str(round(time.time()-start_time, 3)) + ' seconds')

    if (failed_delete_count):
        output('\n' + 'failed to delete ' + str(failed_delete_count) + ' duplicates - rerun script')

    return stdout

def display_duplicate_and_optionally_delete(previously_hashed_file_path, current_file_path, delete_duplicates):

    current_file_message = '            '
    previously_hashed_file_message = ''
    if (delete_duplicates):
        previously_hashed_file_message, current_file_message = delete_duplicate_and_get_message(previously_hashed_file_path, current_file_path)

    output(current_file_message + current_file_path + '\n is dupe of ' + previously_hashed_file_path + previously_hashed_file_message + '\n')

def delete_duplicate_and_get_message(previously_hashed_file_path, current_file_path):

    delete_file_path = current_file_path
    previously_hashed_file_message = ''
    current_file_message = 'deleted ... '

    if (delete_shorter):
        if ( len(os.path.basename(previously_hashed_file_path)) < len(os.path.basename(current_file_path)) ):
            delete_file_path = previously_hashed_file_path
            previously_hashed_file_message = ' ... deleted'
            current_file_message = '            '

    if (not trial_delete):
        try:
            os.chmod(delete_file_path, stat.S_IWRITE)
            os.remove(delete_file_path)
        except FileNotFoundError:
            previously_hashed_file_message = ' ... already deleted' # only the previously hashed file could have been deleted - not the current file (unless user is deleting files outside of this script!)
            global failed_delete_count
            failed_delete_count += 1

    return previously_hashed_file_message, current_file_message

parser = argparse.ArgumentParser(description='Find duplicate files in target path and sub folders.')
parser.add_argument('--path', dest='path', required=False, action='store', help='Target path')
parser.add_argument('--version', action='version', version=version)
parser.add_argument('--verbose', action='store_true', dest='verbose', default=False, help='Will output extra info on logic')
parser.add_argument('--delayed', action='store_true', dest='output_delayed', default=False, help='Will display stdout at end instead of immediately')
parser.add_argument('--delete', action='store_true', dest='delete', default=False, help='Deletes any duplicate files found')
parser.add_argument('--trial', action='store_true', dest='trial_delete', default=False, help='Displays files to delete without actually deleting them - use with --delete')
parser.add_argument('--shorter', action='store_true', dest='delete_shorter', default=False, help='Deletes file with shorter name rather than always current file - use with --delete')

args = parser.parse_args()
set_verbose_output(args.verbose)
set_output_immediately(not args.output_delayed)
set_trial_delete(args.trial_delete)
set_delete_shorter(args.delete_shorter)

if (args.path):
    dff(args.path, args.delete)
    if (not output_immediately):
        print('\nResults...\n')
        unicode_output(stdout)
    sys.exit()
