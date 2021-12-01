from flask import request
from flask_restx import Resource, Api, Namespace, fields

Consent = Namespace(
    name="Consent",
    description="동의서 API"
)

# API import
from . import list