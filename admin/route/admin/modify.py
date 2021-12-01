from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .admin import Admin
import app
from sqlalchemy import text

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('admin_id', help='관리자 ID(PK)', location='json', required=True)
parser.add_argument('password', help='관리자 새 비밀번호', location='json', required=False)
parser.add_argument('name', help='관리자 이름', location='json', required=True)
parser.add_argument('email', help='관리자 이메일', location='json', required=True)
parser.add_argument('phone', help='관리자 연락처', location='json', required=True)

TOKEN_CHECK_SQL = 'SELECT AT.* FROM admin_account_token AS AT, admin_account AS A WHERE AT.token=:token AND AT.aid = A.id'
ADMIN_SELECT_SQL = 'SELECT * FROM admin_account WHERE admin_id=:admin_id'
ADMIN_EMAIL_SELECT_SQL = 'SELECT * FROM admin_account WHERE email=:email'
ADMIN_UPDATE_ALL_SQL = 'UPDATE admin_account SET password=:password, email=:email, phone=:phone WHERE admin_id=:admin_id'
ADMIN_UPDATE_SQL = 'UPDATE admin_account SET email=:email, phone=:phone WHERE admin_id=:admin_id'

@Admin.route('/modify')
class Modify(Resource):
    @Admin.expect(parser)
    @Admin.response(200, 'Success')
    @Admin.response(401, 'Unauthorized')
    @Admin.response(500, 'Internal Server Error')
    def put(self):
        """관리자 정보 수정 API"""
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
        q['admin_id'] = args['admin_id']
        q['password'] = args['password']
        q['email'] = args['email']
        q['phone'] = args['phone']

        row = app.db.execute(text(ADMIN_SELECT_SQL), q).fetchone()
        if row == None:
            return {
                'code': 'fail',
                'message': '존재하지 않는 ID입니다.',
                'response': {
                    'flag': False
                }
            }, 500
        
        sql = ""
        if q['password'] == None:
            sql = ADMIN_UPDATE_SQL
        else:
            sql = ADMIN_UPDATE_ALL_SQL

        if q['password'] != None and q['password'] == row['password']:
            return {
                'code': 'fail',
                'message': '비밀번호가 동일합니다. 다시 입력해 주세요',
                'response': {
                    'flag': False
                }
            }, 500
        
        row = app.db.execute(text(ADMIN_EMAIL_SELECT_SQL), q).fetchone()
        if row != None and row['admin_id'] != q['admin_id']:
            return {
                'code': 'fail',
                'message': '이미 존재하는 이메일입니다.',
                'response': {
                    'flag': False
                }
            }, 500

        app.db.execute(text(sql), q)

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'flag': True
            }
        }, 200
