# clear.py

```
$ ./clear.py -h
usage: clear.py [-h] [-q] [-s PATTERN] [-m MINIMUM] [-d DIRECTORY]

This script cleans directories. It is useful for backup and log file directories, when you want to delete older files.

options:
  -h, --help            show this help message and exit
  -q, --quiet           This script defaults to verbose, use -q to turn off messages (Useful when using the cleaner.sh in automated scripts).
  -s PATTERN, --search PATTERN
                        A search string to limit file deletion, defaults to '*' (All files).
  -m MINIMUM, --minimum MINIMUM
                        The minimum number of files required in the directory (Files to be maintained), defaults to 5.
  -d DIRECTORY, --directory DIRECTORY
                        The directory to clean, defaults to the current directory.

example:
  In the current directory, delete everything but the 5 most recently touched 
  files: 
      cleaner.sh
  Same as:
      clear.py -s '*' -m 5 -d .
  In the /home/myUser directory, delete all files including text "test", 
  except the most recent:
      clear.py -s test -m 1 -d /home/myUser
  Don't ask for any confirmation:
      clear.py -s test -m 1 -d /home/myUser -q
```
