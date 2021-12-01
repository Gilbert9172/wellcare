from flask import request
from flask_restx import Resource, Api, Namespace, fields

Reservation = Namespace(
    name="Reservation",
    description="예약 API"
)

# API import
from . import write
from . import info
from . import cancel
from . import time_check
from . import holiday
from . import non_time