from flask import request
from flask_restx import Resource, reqparse
from .auth import Auth
from sqlalchemy import text
import app

parser = reqparse.RequestParser()
parser.add_argument("Authorization", help="Bearer 토큰", location='headers', required=True)

#-- SQL
TOKEN_CHECK = 'SELECT * FROM user_account_token WHERE token=:token'
TOKEN_DELETE = 'DELETE FROM user_account_token WHERE uid=:uid'

#--
@Auth.expect(parser)
@Auth.response(200, 'Success') 
@Auth.response(404, 'Page Not Found')
@Auth.response(500, 'Internal Server Error')
@Auth.route('/logout')
class AuthLogout(Resource):
    def post(self):
        
        token = request.headers['Authorization']

        # 명시적으로 Baerer을 입력해준다.(Bearer : 토큰의 종류)
        token = {
            'token' : token.split(' ')[1]
        }

        row = app.db2.execute(text(TOKEN_CHECK),token).first()
        if row:
            app.db2.execute(text(TOKEN_DELETE))
        else:
            return 400
