from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .reservation import Reservation
from sqlalchemy import text

import app

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('id', help='예약 시간 PK', location='json', type=int, required=True)
parser.add_argument('limit', help='인원 제한', location='json', type =int, required=True)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'
UPDATE_TIME_LIMIT_SQL = 'UPDATE resv_consultation_limit AS ls SET ls.limit = :limit WHERE id = :id'

@Reservation.route('/time_update')
class TimeUpdate(Resource):
    @Reservation.expect(parser)
    @Reservation.response(200, 'Success')
    @Reservation.response(401, 'Unauthorized')
    @Reservation.response(500, 'Internal Server Error')
    def put(self):
        """예약 인원 제한 수정 API"""
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
        q['limit'] = args['limit']

        try:
            row_id = app.db.execute(text(UPDATE_TIME_LIMIT_SQL), q).lastrowid
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
                'limit': q['limit'],
            }
        }, 200

    



