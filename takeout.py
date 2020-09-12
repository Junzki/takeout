# -*- coding:utf-8 -*-
import os
import argparse
import win32file
import win32con
import pywintypes

WATCHED_EXTS = (
    'png',
    'jpg'
)


parser = argparse.ArgumentParser()
parser.add_argument('src', dest='src', help='Source folder.')
parser.add_argument('dest', dest='dest', help='Destination folder.')


def changeFileCreationTime(fname, newtime):
    wintime = pywintypes.Time(newtime)
    winfile = win32file.CreateFile(
        fname, win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None, win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL, None)

    win32file.SetFileTime(winfile, wintime, None, None)

    winfile.close()


def tree_file(src: str):
    files = os.listdir(src)
    for f in files:
        pass



if __name__ == '__main__':
    args = parser.parse_args()
    src = args.src
    dest = args.dest

    if not (os.path.exists(src) and os.path.isdir(src)):
        raise ValueError(f"Source folder `{src}` does not exist or not a directory.")

    if not os.path.exists(dest):
        os.mkdir(dest)
    elif not os.path.isdir(dest):
        raise ValueError(f"Destination folder `{dest}` appeared and is not a directory.")
