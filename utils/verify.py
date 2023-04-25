# coding: utf-8
import re

from .exception import StrException

name_regex = re.compile("^[a-zA-Z0-9]+$")


def letter_name(v):
    if v == "system":
        raise StrException("非法用户名")
    if not name_regex.match(v):
        raise StrException("无效用户名，仅支持大小写字母")
