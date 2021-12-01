from flask import request
from flask_restx import Resource, Api, Namespace, fields

Questionnaire = Namespace(
    name="Questionnaire",
    description="문진표 API"
)

# API import
from . import list
from . import detail
from . import phone_list
from . import phone_check_list
