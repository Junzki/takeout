# -*- coding:utf-8 -*-
import os
import re
import argparse
import datetime
import threading
import queue
import json
import win32file
import win32con
import pywintypes
import pytz
from typing import Optional

WATCHED_EXTS = (
    'png',
    'jpg',
    'heic'
)
META_EXT = 'json'
EDITED_TAILOR = '-edited'


parser = argparse.ArgumentParser()
parser.add_argument('src', help='Source folder.')
parser.add_argument('dest', help='Destination folder.')

DATE_PATTERN = re.compile(r'(?P<year>\d{4})\-\d{2}\-\d{2}')

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


def get_meta(fn: str) -> (str, datetime.datetime):
    with open(fn, 'r') as f:
        content = json.load(f)

    creation_time = content.get('photoTakenTime')
    if not creation_time:
        creation_time = content['creationTime']

    ts = int(creation_time['timestamp'])
    dt = datetime.datetime.fromtimestamp(ts).replace(tzinfo=pytz.UTC)
    year = dt.year

    return str(year), dt


def time_from_path(fn: str) -> (str, datetime.datetime):
    m = DATE_PATTERN.search(fn)
    dt = m.group()

    dt = datetime.datetime.strptime(dt, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)
    return str(dt.year), dt


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

        # TODO:
        # It seems files with tailor `-edited` are ignored unexpectly, and
        # the original images are copied twice (which creates a duplicated file to be removed).
        # Fix it in the near future.
        pair = (
            f,
            meta_fn if meta_fn else None
        )

        shared.put(pair)


def copy_file(dest: str,
              fn: str,
              year: str,
              created_at: datetime.datetime):
    dirname = os.path.join(dest, year)
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

    _, name = os.path.split(fn)

    target = os.path.join(dirname, name)
    win32file.CopyFile(fn, target, False)
    changeFileCreationTime(target, created_at)


def work(dest: str):
    t: threading.Thread = threading.current_thread()
    ok = False

    while alive or ok:
        try:
            v = shared.get(block=True, timeout=3)
        except queue.Empty:
            ok = False
            continue

        if not v:
            ok = False
            continue

        ok = True
        fn, meta_fn = v
        print(f'[{t.name}] File: {fn}')
        print(f'[{t.name}] Meta: {meta_fn}')

        if meta_fn:
            year, created_at = get_meta(meta_fn)
        else:
            year, created_at = time_from_path(fn)

        copy_file(dest, fn, year, created_at)
        if meta_fn:
            copy_file(dest, meta_fn, year, created_at)


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
