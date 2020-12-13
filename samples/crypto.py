# -*- coding:utf-8 -*-
import hashlib


def hash_buf(buf: bytes) -> str:
    """ Calculate SHA256
    """
    result = hashlib.sha256(buf)
    return result.hexdigest()
