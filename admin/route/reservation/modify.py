from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .reservation import Reservation
from sqlalchemy import text

import app

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('id', help='예약번호', location='json', type=int, required=False)
parser.add_argument('resv_date', help='예약날짜', location='json', required=True)
parser.add_argument('resv_time', help='예약시간', location='json', required=True)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'
MODIFY_RESVERVATION_SQL = 'UPDATE resv_consultation SET resv_date=:resv_date, resv_time=:resv_time, resv_flag=4 WHERE id=:id'

@Reservation.route('/modify')
class Modify(Resource):
    @Reservation.expect(parser) 
    @Reservation.response(200, 'Success')
    @Reservation.response(500, 'Internal Server Error')
    def put(self):
        """예약 수정하기 API"""
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

        q = {}
        q['id'] = args['id']
        q['resv_date'] = args['resv_date']
        q['resv_time'] = args['resv_time']

        try:
            row_id = app.db.execute(text(MODIFY_RESVERVATION_SQL), q).lastrowid
        except Exception as e:
            print(e)
            return {
                'code': 'fail',
                'message': 'Internal Server Error',
                'response': {
                    'flag': False
                }
            }, 500 

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'id': q['id'],
                'resv_date': q['resv_date'],
                'resv_time': q['resv_time']
            }
        }, 200