# coding: utf-8
import pywss

from pydantic import BaseModel
from sqlalchemy import func
from db import Session
from db.model import Exam, ExamQuestion
from utils.http import Response
from service import db as dbService
from typing import List

__route__ = "/record/{rid}"


class View:

    @pywss.openapi.docs("试题列表")
    def http_get(self, ctx: pywss.Context):
        pass

    @pywss.openapi.docs("创建考试")
    def http_post(self, ctx: pywss.Context):
        pass
