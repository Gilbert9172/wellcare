from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .reservation import Reservation
from sqlalchemy import text

import app

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('user_memo', help='참여자 메모', location='json', required=True)
parser.add_argument('user_name', help='참여자 이름', location='json', required=True)
parser.add_argument('user_phone', help='참여자 휴대폰번호', location='json', required=True)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'
MODIFY_MEMO_SQL = 'UPDATE user SET user_memo=:user_memo WHERE user_name=:user_name AND user_phone=:user_phone'

@Reservation.route('/memo_update')
class Memo_Update(Resource):
    @Reservation.expect(parser) 
    @Reservation.response(200, 'Success')
    @Reservation.response(500, 'Internal Server Error')
    def put(self):
        """메모 수정하기 API"""
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
        q['user_memo'] = args['user_memo']
        q['user_name'] = args['user_name']
        q['user_phone'] = args['user_phone']

        try:
            row_id = app.db.execute(text(MODIFY_MEMO_SQL), q).lastrowid
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
                'flag': True
            }
        }, 200