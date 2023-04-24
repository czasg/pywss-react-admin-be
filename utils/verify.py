# coding: utf-8
import re

from .exception import StrException

name_regex = re.compile("^[a-zA-Z]+$")


def letter_name(v):
    if not name_regex.match(v):
        raise StrException("无效用户名，仅支持大小写字母")
