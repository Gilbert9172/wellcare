from os import close
from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .reservation import Reservation
from sqlalchemy import text

import app

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('id', help='날짜id', type=int, required=True)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'
SELECT_DATETIME_SQL = 'SELECT * FROM resv_non_datetime WHERE id=:id'
DELETE_DATETIME_SQL = 'DELETE FROM resv_non_datetime WHERE id=:id'


@Reservation.route('/non_datetime_delete')
class Datetime_Delete(Resource):
    @Reservation.expect(parser)
    @Reservation.response(200, 'Success')
    @Reservation.response(500, 'Failed')
    def delete(self):
        """예약 불가 날짜시간 삭제 API"""
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

        q = dict()
        q['id'] = args['id']

        row = app.db.execute(text(SELECT_DATETIME_SQL), q).fetchone()

        if row == None:
            return {
                'code': 'fail',
                'message': '잘못된 시간정보 ID입니다'
            }, 500

        app.db.execute(text(DELETE_DATETIME_SQL), q)

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'flag': True
            }
        }, 200
