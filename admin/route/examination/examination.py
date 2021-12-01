from flask import request
from flask_restx import Resource, Api, Namespace, fields
Examination = Namespace(
    name="Examination",
    description="검사 API"
)

# API import
from . import check_list