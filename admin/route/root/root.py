from flask import request
from flask_restx import Resource, Api, Namespace, fields
Root = Namespace(
    name="Root",
    description="Root API"
)

# API import
from . import login
from . import logout
from . import photos