# duplicate-file-finder 0.10.0

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

These examples assume `dff.py` has been added to your `PATH` - see below for installation instructions.

List duplicates:

```
dff.py --path test/one_small_duplicate
```

Or to search from current folder:

```
dff.py --path .
```

Pretend to delete dupes, does not delete anything:

```
dff.py --path test/duplicate_across_folders --delete --trial
```

Really delete duplicates - careful !!! - deletes read only files too:

```
dff.py --path test/duplicate_across_folders --delete
```

Delete the file with the shorter file name rather than always the file currently being processed:

```
dff.py --path test/duplicate_across_folders --delete --shorter
```

When using this option, some multiple duplicates of a file might be missed. In that case you'll need to run
the script again. A message at script completion will tell you if this is the case.

This option is recommended for where you have photos and have taken the trouble to give a meaningful description
to the photo content - you'll want to keep the longer file name rather than just the basic automatically given name.

## Debian / Ubuntu Installation

```bash
cd /usr/local/bin
sudo git clone https://github.com/Qarj/duplicate-file-finder
cd duplicate-file-finder
sudo find . -type d -exec chmod a+rwx {} \;
sudo find . -type f -exec chmod a+rw {} \;
sudo chmod +x dff.py
sudo chmod +x test_dff.py
```

Now add to user path

```bash
gedit ~/.bashrc
```

Add this line to the bottom and save

```bash
export PATH="$PATH:/usr/local/bin/duplicate-file-finder"
```

Update path for current shell (or reboot!)

```bash
source ~/.bashrc
```

Now it will be possible to run it from anywhere

```bash
dff.py --help
```

## Debian / Ubuntu Quick Installation

Copy the contents of `dff.py` to the clipboard then

```bash
sudo nano /usr/local/bin/dff.py
```

SHIFT-INSERT to paste the text, save and exit then

```bash
sudo chmod +x /usr/local/bin/dff.py
```

## Windows Installation

Copy `dff.py` to `C:\Windows` then you can run it from anywhere.

## Run the unit tests

Unit tests must be run with the project folder as the current folder.

Linux

```
./test_dff.py
```

Windows

```
test_dff.py
```
