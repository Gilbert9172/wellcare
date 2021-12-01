from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .reservation import Reservation
import app

from datetime import datetime
from sqlalchemy import text


parser = reqparse.RequestParser()
SELECT_NONTIME_SQL = "SELECT * FROM resv_non_datetime"


@Reservation.route('/nontime')
class Nontime(Resource):
    @Reservation.expect(parser)
    @Reservation.response(200, 'Success')
    @Reservation.response(500, 'Failed')
    def get(self):
        """예약불가 시간 API"""
        args = parser.parse_args()

        q = {}
        row = app.db.execute(text(SELECT_NONTIME_SQL),q).fetchall()
        list_nontime = []
        for r in row:
            nontime = {}
            nontime['date'] = r['date']
            nontime['time'] = r['time']
            list_nontime.append(nontime)

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'list': list_nontime
            }
        }, 200
