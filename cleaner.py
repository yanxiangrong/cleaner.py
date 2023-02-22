#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path


class Option:
    pattern: str
    min_files: int
    dir: str
    quiet: bool


def get_files(path: Path, pattern: str) -> list[Path]:
    files = list[Path]()
    for item in path.iterdir():
        if not item.match(pattern):
            continue
        if item.is_file():
            files.append(item)
        elif item.is_dir():
            files.append(item)
    return files


def sort_by_mtime(files: list[Path]) -> list[Path]:
    files.sort(key=lambda item: item.stat().st_mtime)
    return files


def get_option() -> Option:
    prog = os.path.basename(sys.argv[0])
    example = f'''
example:
  In the current directory, delete everything but the 5 most recently touched 
  files: 
      {prog}
  Same as:
      {prog} -s '*' -m 5 -d .
  In the /home/myUser directory, delete all files including text "test", 
  except the most recent:
      {prog} -s test -m 1 -d /home/myUser
  Don't ask for any confirmation:
      {prog} -s test -m 1 -d /home/myUser -q'''

    parser = argparse.ArgumentParser(
        description='This script cleans directories.  It is useful for backup and log file directories, when you want '
                    'to delete older files. ',
        add_help=False
    )
    parser.add_argument('-h', '--help', action='store_true',
                        help='show this help message and exit')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='This script defaults to verbose, use -q to turn off messages '
                             '(Useful when using the cleaner.sh in automated scripts).')
    parser.add_argument('-s', '--search', default='*', metavar='PATTERN',
                        help="A search string to limit file deletion, defaults to '*' (All files).")
    parser.add_argument('-m', '--minimum', default=5, type=int,
                        help='The minimum number of files required in the directory (Files to be maintained), '
                             'defaults to 5.')
    parser.add_argument('-d', '--directory', default='.', type=str,
                        help='The directory to clean, defaults to the current directory.')
    args = parser.parse_args()

    if args.help:
        parser.print_help()
        print(example)
        exit(0)

    if args.minimum < 0:
        parser.print_usage()
        exit('MINIMUM must be >= 0')

    opt = Option()
    opt.quiet = args.quiet
    opt.pattern = args.search
    opt.dir = args.directory
    opt.min_files = args.minimum
    return opt


def remove_file(item: Path) -> int:
    deleted = 0
    if item.is_file():
        try:
            os.remove(item)
            deleted += 1
        except Exception as e:
            print(e)
    elif item.is_dir():
        for i in item.iterdir():
            deleted += remove_file(i)
        try:
            os.rmdir(item)
            deleted += 1
        except Exception as e:
            print(e)

    return deleted


def remove_files(files: list[Path]) -> int:
    deleted = 0
    for item in files:
        deleted += remove_file(item)
    return deleted


def print_files(files: list[Path]):
    if len(files) == 0:
        return
    for item in files:
        print(item.name, '\t', end='')
    print()


def main():
    opt = get_option()
    path = Path(opt.dir)
    files = get_files(path, opt.pattern)
    files = sort_by_mtime(files)
    files = files[:max(len(files) - opt.min_files, 0)]

    if not opt.quiet:
        if opt.min_files == 0:
            print('Delete the following files ([Y]es/[N]o)?')
        else:
            print(f'Delete the following files except the {opt.min_files} most recently touched ([Y]es/[N]o)?')
        print_files(files)
        confirm = input()
        if confirm in ['y', 'Y', 'yes', 'YES', 'Yes']:
            deleted = remove_files(files)
            print(f"Removed {deleted} file{'s' if deleted > 1 else ''}.")
        else:
            print('Cleaner canceled.')
    else:
        remove_files(files)


if __name__ == '__main__':
    main()
