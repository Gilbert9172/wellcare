from os import close
from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .reservation import Reservation
from sqlalchemy import text
import app

parser = reqparse.RequestParser()
parser.add_argument('resv_date', help='날짜', location='json', required=True)

CONSULTATION_CHECK = 'SELECT li.hour,li.limit FROM resv_consultation_limit as li '
CONSULTATION_TIME_COUNT_CHECK = 'SELECT COUNT(resv_time) FROM resv_consultation AS C WHERE (C.resv_flag = 0 OR C.resv_flag = 2 OR C.resv_flag = 4) AND C.resv_date=:resv_date AND C.resv_time=:resv_time'

@Reservation.route('/count')
class Count(Resource):
    @Reservation.expect(parser)
    @Reservation.response(200, 'Success')
    @Reservation.response(500, 'Failed')
    def post(self):
        """예약 시간 인원 카운트 API"""
        args = parser.parse_args()

        time_list = list()
        row = app.db.execute(text(CONSULTATION_CHECK)).fetchall()
        print(row)
        for t in row:
            q = {}
            q['resv_date'] = args['resv_date']
            q['resv_time'] = t['hour']
            rows = app.db.execute(text(CONSULTATION_TIME_COUNT_CHECK), q).fetchone()
            print(rows)
            minus = 0
            minus = int(rows['COUNT(resv_time)'])
            # minus = int(row[0]['limit']) - int(rows['COUNT(resv_time)'])
            # if minus < 0:
                # minus = 0

            time_list.append({
                'time': t['hour'],
                'count': minus
            })

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'list': time_list
            }
        }, 200