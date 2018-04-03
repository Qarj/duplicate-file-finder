# duplicate-file-finder

Very quickly find files with duplicate content, and optionally delete duplicates.

This Python 3 script computes the MD5 of the first 4096 bytes of a file (NTFS default sector size) and stores it.

Only if another file is found with the same MD5 snippet, the full MD5 of both files is computed to confirm duplicate.

This double MD5 compute strategy makes it vanishlying small that two files will be declared identical when they are not.

## Usage

List duplicates:
```
dff --path test/one_small_duplicate
```

Pretend to delete dupes:
```
dff --path test/duplicate_across_folders --delete --trial
```

Really delete them - carefull !!!:
```
dff --path test/duplicate_across_folders --delete
```

## Run the unit tests

```
test_dff
```

## Limitations

* If a permission denied (or locked) file is encountered, the script is aborted (will be fixed)
* If a read only duplicate file is encountered with --delete option, script will abort (will be fixed)
