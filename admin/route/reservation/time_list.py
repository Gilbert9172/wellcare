from os import close
from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .reservation import Reservation
from sqlalchemy import text

import app

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'
TIME_LIST = 'SELECT * FROM resv_consultation_limit'

@Reservation.route('/time_list')
class TimeList(Resource):
    @Reservation.expect(parser)
    @Reservation.response(200, 'Success')
    @Reservation.response(401, 'Unauthorized')
    @Reservation.response(500, 'Internal Server Error')
    def get(self):
        """예약 시간 리스트 API"""
        args = parser.parse_args()
        token = args['Authorization']

        if token == None:
            return {
                'code': 'fail',
                'message': '토큰정보가 없습니다',
                'response': {}
            }, 401

        token = token.split(' ')[1]
        row = app.db.execute(text(TOKEN_CHECK_SQL), {
            'token': token
        }).fetchone()
        if row == None:
            return {
                'code': 'fail',
                'message': '토큰이 유효하지 않습니다',
                'response': {}
            }, 401

        rows = app.db.execute(text(TIME_LIST)).fetchall()

        resp = []
        for row in rows:
            r={}
            r['id'] = row['id']
            r['hour'] = row['hour']
            r['limit'] = row['limit']
            resp.append(r)
            

        return {
            'code':'success',
            'message':'success',
            'response':{
                'list':resp
            }
        },200
