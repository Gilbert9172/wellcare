from flask import request
from flask_restx import Resource, reqparse
from .root import Root
import app
from sqlalchemy import text

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'
TOKEN_DELETE_SQL = 'DELETE FROM admin_account_token WHERE aid=:aid'

@Root.route('/logout')
class Logout(Resource):
    @Root.expect(parser)
    @Root.response(200, 'Success')
    @Root.response(401, 'Unauthorized')
    def post(self):
        """관리자 로그아웃 API"""
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

        app.db.execute(text(TOKEN_DELETE_SQL), {
            'aid': row['aid'],
            'token': token
        })

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'flag': True
            }
        }, 200
