#!/usr/bin/env python3
version="0.0.2"

import sys, argparse, math, hashlib, os

stdout = ''
verbose_output = None
output_immediately = None

def clear_stdout():
    global stdout
    stdout = ''

def set_verbose_output(v):
    global verbose_output
    verbose_output = v

def set_output_immediately(o):
    global output_immediately
    output_immediately = o

def md5_full(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def md5_snip(file_path):
    verbose('...calculating md5 snippet of ' + file_path)
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
            f.close()
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

def dff(path):
    verbose('Started searching in ' + path)

    snip = dict()
    full = dict()
    for file_name in os.listdir(path):
        verbose('Processing file ' + file_name)
        current_file_snip_hash = md5_snip(path + '/' + file_name)
        if (current_file_snip_hash in snip):

            # Put the snip file in the full dictionary also
            current_file_full_hash = md5_full(path + '/' + file_name)
            snip_file_full_hash = md5_full(snip[current_file_snip_hash])
            full[snip_file_full_hash] = snip[current_file_snip_hash]

            if (current_file_full_hash in full):
                output(path + '/' + file_name + ' is a duplicate of ' + snip[current_file_snip_hash])
            else:
                verbose('...first 4096 bytes are the same, but files are different')
        else:
            snip[current_file_snip_hash] = path + '/' + file_name

    return stdout

parser = argparse.ArgumentParser(description='Find duplicate files in target path and sub folders.')
parser.add_argument('--path', dest='path', required=False, action='store', help='Target path')
parser.add_argument('--version', action='version', version=version)
parser.add_argument('--verbose', action='store_true', dest='verbose', default=False, help='Will output extra info on logic')
parser.add_argument('--delayed', action='store_true', dest='output_delayed', default=False, help='Will display stdout at end instead of immediately')

args = parser.parse_args()
set_verbose_output(args.verbose)
set_output_immediately(not args.output_delayed)

clear_stdout()

if (args.path):
    print('Finding duplicate files at', args.path)
    dff(args.path)
    if (not output_immediately):
        print('\nResults...\n')
        print(stdout)
    sys.exit()
