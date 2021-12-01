from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .admin import Admin
import app
from sqlalchemy import text

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('adminId', help='관리자 아이디', location='json', required=True)
parser.add_argument('password', help='관리자 비밀번호', location='json', required=True)
parser.add_argument('name', help='관리자 이름', location='json', required=True)
parser.add_argument('email', help='관리자 이메일', location='json', required=True)
parser.add_argument('phone', help='관리자 휴대폰번호', location='json', required=True)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'
ADMIN_ID_SELECT_SQL = 'SELECT * FROM admin_account WHERE admin_id=:admin_id'
ADMIN_EMAIL_SELECT_SQL = 'SELECT * FROM admin_account WHERE email=:email'
ADMIN_INSERT_SQL = 'INSERT INTO admin_account(admin_id, password, name, email, phone) VALUES(:admin_id, :password, :name, :email, :phone)'

@Admin.route('/create')
class Create(Resource):
    @Admin.expect(parser)
    @Admin.response(200, 'Success')
    @Admin.response(401, 'Unauthorized')
    @Admin.response(500, 'Internal Server Error')
    def post(self):
        """관리자 정보 등록 API"""
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
        
        q={}
        q['admin_id'] = args['adminId']
        q['password'] = args['password']
        q['name'] = args['name']
        q['email'] = args['email']
        q['phone'] = args['phone']

        row = app.db.execute(text(ADMIN_ID_SELECT_SQL), q).fetchone()
        if row != None:
            return {
                'code': 'fail',
                'message': '이미 존재하는 아이디입니다.',
                'response': {
                    'flag': False
                }
            }, 500

        row = app.db.execute(text(ADMIN_EMAIL_SELECT_SQL), q).fetchone()
        if row != None:
            return {
                'code': 'fail',
                'message': '이미 존재하는 이메일입니다.',
                'response': {
                    'flag': False
                }
            }, 500

        app.db.execute(text(ADMIN_INSERT_SQL), q)

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'flag': True
            }
        }, 200


        

