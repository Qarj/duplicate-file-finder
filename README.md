# duplicate-file-finder 0.7.0

Very quickly find files with duplicate content, and optionally delete duplicates.

This Python 3 script computes the Blake2 64 byte hash of the first 4096 bytes of a file (NTFS default sector size) and stores it.

Only if another file is found with the same Blake2 hash snippet, the full Blake2 of both files is computed to confirm duplicate.

This double Blake2 compute strategy makes it extremely unlikely that two files will be declared identical when they are not.

## Usage

List duplicates:
```
dff --path test/one_small_duplicate
```

Pretend to delete dupes:
```
dff --path test/duplicate_across_folders --delete --trial
```

Really delete them - careful !!! - deletes read only files too:
```
dff --path test/duplicate_across_folders --delete
```

Delete the file with the shorter file name rather than always the file currently being processed:
```
dff --path test/duplicate_across_folders --delete --shorter
```
When using this option, some multiple duplicates of a file might be missed. In that case you'll need to run
the script again. A message at script completion will tell you if this is the case.

This option is recommended for where you have photos and have taken the trouble to give a meaningful description
to the photo content - you'll want to keep the longer file name rather than just the basic automatically given name.


## Run the unit tests

```
test_dff
```

