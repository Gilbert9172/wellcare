from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .root import Root
import app
from sqlalchemy import text
import secrets

parser = reqparse.RequestParser()
parser.add_argument('admin_id', help='관리자 아이디', location='json', required=True)
parser.add_argument('password', help='관리자 비밀번호', location='json', required=True)

ADMIN_SELECT_SQL = 'SELECT * FROM admin_account WHERE admin_id=:admin_id'
TOKEN_INSERT_SQL = 'INSERT INTO admin_account_token(aid, token) VALUES(:aid, :token)'
TOKEN_DELETE_SQL = 'DELETE FROM admin_account_token WHERE aid=:aid'


@Root.route('/login')
class Login(Resource):
    @Root.expect(parser)
    @Root.response(200, 'Success')
    @Root.response(500, 'Internal Server Error')
    def post(self):
        """관리자 로그인 API"""
        args = parser.parse_args()

        q = dict()
        q['admin_id'] = args['admin_id']
        q['password'] = args['password']

        row = app.db.execute(text(ADMIN_SELECT_SQL), q).fetchone()
        if row == None:
            return {
                'code': 'fail',
                'message': '관리자로 등록된 아이디가 아닙니다.',
                'response': {}
            }, 200

        if row['password'] != q['password']:
            return {
                'code': 'fail',
                'message': '비밀번호가 잘못되었습니다.',
                'response': {}
            }, 200

        q['token'] = secrets.token_hex()
        q['aid'] = row['id']

        app.db.execute(text(TOKEN_DELETE_SQL), q)
        app.db.execute(text(TOKEN_INSERT_SQL), q)

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'userId': row['admin_id'],
                'name': row['name'],
                'token': q['token']
            }
        }, 200
