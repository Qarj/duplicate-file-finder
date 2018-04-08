# duplicate-file-finder 0.5.0

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

Really delete them - carefull !!! - deletes read only files too:
```
dff --path test/duplicate_across_folders --delete
```

Delete the file with the shorter file name rather than always the file currently being processed:
```
dff --path test/duplicate_across_folders --delete --shorter
```
When using this option, some multiple duplicates of a file might be missed. In that case you'll need to run
the script again. A message at script completion will tell you if this is the case.


## Run the unit tests

```
test_dff
```

