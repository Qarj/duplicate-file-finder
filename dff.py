#!/usr/bin/env python3
version="0.0.7"

import sys, argparse, math, hashlib, os, stat

# Flags
verbose_output = None
output_immediately = None
trial_delete = None

# Globals
stdout = ''
megabytes_scanned = 0

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

def md5_full(file_path):
    global megabytes_scanned
    verbose('...calculating md5 full of ' + file_path)
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(BYTES_TO_SCAN), b""):
            hash_md5.update(chunk)
            megabytes_scanned += SCAN_SIZE_MB
    return hash_md5.hexdigest()

def md5_snip(file_path):
    global megabytes_scanned
    verbose('...calculating md5 snippet of ' + file_path)
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(BYTES_TO_SCAN), b""):
            hash_md5.update(chunk)
            f.close()
            megabytes_scanned += SCAN_SIZE_MB
            return hash_md5.hexdigest()

def verbose(out):
    if (verbose_output):
        return output(out)
    return

def output(out):
    global stdout
    if (output_immediately):
        print(out, flush=True)
    else:
        stdout += out + "\n"

def output_without_newline(out):
    global stdout
    if (output_immediately):
        print(out, end='', flush=True)
    else:
        stdout += out

def dff(path, delete=False):
    verbose('Started searching in ' + path)

    snip = dict()
    full = dict()

    duplicate_count = 0
    file_count = 0

    for root, dirs, files in os.walk(path):
        files.sort()
        for file_name in files:
            file_count += 1
            file_relative_path = os.path.join(root,file_name)
            verbose('Processing file ' + file_relative_path)
            current_file_snip_hash = md5_snip(file_relative_path)
            if (current_file_snip_hash in snip):

                # Put the snip file in the full dictionary also
                current_file_full_hash = md5_full(file_relative_path)
                snip_file_full_hash = md5_full(snip[current_file_snip_hash])
                #verbose(current_file_full_hash + ' ||| ' + snip_file_full_hash)

                full[snip_file_full_hash] = snip[current_file_snip_hash]
                #verbose('snip[current_file_snip_hash] ' + snip[current_file_snip_hash])

                if (current_file_full_hash in full):
                    if (delete):
                        delete_message = 'deleted ... '
                        if (not trial_delete):
                            os.chmod(file_relative_path, stat.S_IWRITE)
                            os.remove(file_relative_path)
                    else:
                        delete_message = '            '
                    output(delete_message + file_relative_path + '\n is dupe of ' + snip[current_file_snip_hash] + '\n')
                    if (file_relative_path == snip[current_file_snip_hash]):
                        output('\n\nCAUTION -- files have same full path -- WTF?!\n\n')
                    duplicate_count += 1
                else:
                    verbose('...first 4096 bytes are the same, but files are different')
            else:
                snip[current_file_snip_hash] = file_relative_path

    output('\n' + str(duplicate_count) + ' duplicate files found, ' + str(file_count) + ' files and ' + str(megabytes_scanned) + ' megabytes scanned')

    return stdout

def walk(path):
    snip = dict()
    full = dict()

    file_count = 0

    for root, dirs, files in os.walk(path):
        files.sort()
        for file_name in files:
            file_relative_path = os.path.join(root,file_name)
            output('File:' + file_relative_path)
            file_count += 1
    
    print (file_count, 'files')

    return stdout


parser = argparse.ArgumentParser(description='Find duplicate files in target path and sub folders.')
parser.add_argument('--path', dest='path', required=False, action='store', help='Target path')
parser.add_argument('--version', action='version', version=version)
parser.add_argument('--verbose', action='store_true', dest='verbose', default=False, help='Will output extra info on logic')
parser.add_argument('--delayed', action='store_true', dest='output_delayed', default=False, help='Will display stdout at end instead of immediately')
parser.add_argument('--delete', action='store_true', dest='delete', default=False, help='Deletes any duplicate files found')
parser.add_argument('--trial', action='store_true', dest='trial_delete', default=False, help='Displays files to delete without actually deleting them - use with --delete')
parser.add_argument('--walk', action='store_true', dest='walk', default=False, help='Walks the target')

args = parser.parse_args()
set_verbose_output(args.verbose)
set_output_immediately(not args.output_delayed)
set_trial_delete(args.trial_delete)

if (args.walk):
    print('Walking....')
    walk(args.path)
    sys.exit()

if (args.path):
    print('\nFinding duplicate files at', args.path, '\n')
    dff(args.path, args.delete)
    if (not output_immediately):
        print('\nResults...\n')
        print(stdout)
    sys.exit()
