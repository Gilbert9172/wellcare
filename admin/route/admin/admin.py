from flask import request
from flask_restx import Resource, Api, Namespace, fields

Admin = Namespace(
    name="Admin",
    description="관리자 회원 관리 API"
)

# API import
from . import create
from . import modify
from . import delete
from . import list
