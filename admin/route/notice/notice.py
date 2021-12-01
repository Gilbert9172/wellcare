from flask import request
from flask_restx import Resource, Api, Namespace, fields
from sqlalchemy.sql.expression import delete
Notice = Namespace(
    name="Notice",
    description="공지사항 API"
)

# API import
from . import write
from . import upload
from . import modify
from . import detail
from . import delete
from . import list