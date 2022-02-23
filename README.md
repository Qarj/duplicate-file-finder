# duplicate-file-finder 0.10.0

[![GitHub Super-Linter](https://github.com/Qarj/duplicate-file-finder/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)
![Tests](https://github.com/Qarj/duplicate-file-finder/workflows/Tests/badge.svg)

Very quickly find files with duplicate content, and optionally delete duplicates.

This Python 3 script first checks all file sizes at the target path tree.
Files are added to a list where the file size is common with one or more other files.

Then the script computes the Blake2 64 byte hash of the first 4096 bytes of a file (NTFS default sector size) and stores it.

Only if another file is found with the same Blake2 hash snippet, the full Blake2 of both files is computed to confirm duplicate.

This double Blake2 compute strategy makes it extremely unlikely that two files will be declared identical when they are not.

Zero byte files are ignored, but counted.

File symlinks to nowhere are ignored, but counted.

All files in the specified path, and all subfolders, are evaluated. Folder symlinks are not followed.

## Usage

These examples assume `dff` has been added to your `PATH` - see below for installation instructions.

List duplicates:

```sh
dff --path test/one_small_duplicate
```

Or to search from current folder:

```sh
dff --path .
```

Pretend to delete dupes, does not delete anything:

```sh
dff --path test/duplicate_across_folders --delete --trial
```

Really delete duplicates - careful !!! - deletes read only files too:

```sh
dff.py --path test/duplicate_across_folders --delete
```

Delete the file with the shorter file name rather than always the file currently being processed:

```sh
dff.py --path test/duplicate_across_folders --delete --shorter
```

When using this option, some multiple duplicates of a file might be missed. In that case you'll need to run
the script again. A message at script completion will tell you if this is the case.

This option is recommended for where you have photos and have taken the trouble to give a meaningful description
to the photo content - you'll want to keep the longer file name rather than just the basic automatically given name.

## Debian / Ubuntu Installation

Clone project then add to path using symbolic link

```sh
cd ~
sudo git clone https://github.com/Qarj/duplicate-file-finder
cd duplicate-file-finder
chmod +x dff.py
sudo ln -sf $HOME/git/duplicate-file-finder/dff.py /usr/local/bin/dff
```

Check working

```sh
dff --help
```

## Windows Installation

Copy `dff.py` to `C:\Windows` then you can run it from anywhere as `dff.py`.

## Run the unit tests

Unit tests must be run with the project folder as the current folder.

Linux

```
python test_dff.py
```

Windows

```
test_dff.py
```
