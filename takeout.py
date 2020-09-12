# -*- coding:utf-8 -*-
import os
import argparse
import datetime
import threading
import queue
import json
import win32file
import win32con
import pywintypes
from typing import Optional

WATCHED_EXTS = (
    'png',
    'jpg'
)
META_EXT = 'json'
EDITED_TAILOR = '-edited'


parser = argparse.ArgumentParser()
parser.add_argument('src', help='Source folder.')
parser.add_argument('dest', help='Destination folder.')

shared: queue.Queue = queue.Queue()
alive = True


def changeFileCreationTime(fname, newtime):
    wintime = pywintypes.Time(newtime)
    winfile = win32file.CreateFile(
        fname, win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None, win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL, None)

    win32file.SetFileTime(winfile, wintime, None, None)

    winfile.close()


def get_meta(fn: str) -> str:
    return ''


def get_meta_filename(fn: str) -> Optional[str]:
    h, ext = fn.rsplit('.', 1)
    if EDITED_TAILOR in h:
        h = h.rstrip(EDITED_TAILOR)

    f1 = '.'.join((h, ext, META_EXT))
    f2 = '.'.join((h, META_EXT))

    if os.path.exists(f1):
        return f1

    if os.path.exists(f2):
        return f2

    return None


def tree_file(src: str):
    files = os.listdir(src)
    for f in files:
        f = os.path.join(src, f)

        if os.path.isdir(f):
            tree_file(f)
            continue

        if '.' not in f:
            continue

        _, ext = f.rsplit('.', 1)
        ext = ext.lower()
        if ext not in WATCHED_EXTS:
            continue

        meta_fn = get_meta_filename(f)

        pair = (
            f,
            meta_fn if meta_fn else None
        )

        shared.put(pair)


def work(dest: str):
    t: threading.Thread = threading.current_thread()

    while alive:
        try:
            v = shared.get(block=True, timeout=3)
        except queue.Empty:
            continue

        if not v:
            continue

        fn, meta_fn = v
        print(f'[{t.name}] File: {fn}')
        print(f'[{t.name}] Meta: {meta_fn}')


if __name__ == '__main__':
    args = parser.parse_args()
    src = args.src
    dest_ = args.dest

    if not os.path.isdir(src):
        raise ValueError(f"Source folder `{src}` does not exist or not a directory.")

    if not os.path.exists(dest_):
        os.mkdir(dest_)
    elif not os.path.isdir(dest_):
        raise ValueError(f"Destination folder `{dest_}` appeared and is not a directory.")

    work_thead = threading.Thread(name='Worker', target=work, args=(dest_, ))
    work_thead.start()

    tree_file(src)

    alive = False
    work_thead.join()
