from os import close
from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .reservation import Reservation
from sqlalchemy import text

import app

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('id', help='날짜id', location='json', type=int, required=True)
parser.add_argument('date', help='날짜', location='json', required=True)
parser.add_argument('time', help='시간', location='json', required=True)
parser.add_argument('author', help='작성자', location='json', required=True)



TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'
MODIFY_DATETIME_SQL = 'UPDATE resv_non_datetime SET date=:date, time=:time, author=:author WHERE id=:id'



@Reservation.route('/non_datetime_update')
class Update(Resource):
    @Reservation.expect(parser)
    @Reservation.response(200, 'Success')
    @Reservation.response(500, 'Failed')
    def post(self):
        """예약 불가 날짜시간 수정 API"""
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
        q['date'] = args['date']
        q['time'] = args['time']
        q['author'] = args['author']

        try:
            row_id = app.db.execute(text(MODIFY_DATETIME_SQL), q).lastrowid

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
                'date': q['date'],
                'time' : q['time']
            }
        }, 200
