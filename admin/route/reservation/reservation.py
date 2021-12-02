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
from . import modify
from . import list
from . import time_update
from . import time_check
from . import time_list
from . import excel
from . import memo_update
from . import delete
from . import time_count
from . import test_write
from . import non_datetime
from . import non_update
from . import non_delete
from . import non_detail
from . import non_list
from . import dup
