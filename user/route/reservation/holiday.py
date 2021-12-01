from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .reservation import Reservation
import app

from datetime import datetime
from sqlalchemy import text


parser = reqparse.RequestParser()

SELECT_HOLIDAY_SQL = "SELECT * FROM holiday"

@Reservation.route('/holiday')
class Holiday(Resource):
    @Reservation.expect(parser)
    @Reservation.response(200, 'Success')
    @Reservation.response(500, 'Failed')
    def get(self):
        """공휴일 API"""
        args = parser.parse_args()
        
        q = {}
        row = app.db.execute(text(SELECT_HOLIDAY_SQL),q).fetchall()
        
        list_holiday = []
        for r in row:
            holiday = {}
            holiday['date'] = r['date']
            holiday['text'] = r['text']
            list_holiday.append(holiday)

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'list': list_holiday
            }
        }, 200
