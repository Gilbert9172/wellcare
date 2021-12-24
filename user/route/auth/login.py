#-- Modules
from flask import request
from flask_restx import Resource, reqparse
from werkzeug.wrappers import response
from .auth import Auth
from sqlalchemy import text
import app, bcrypt, jwt
from datetime import datetime, timedelta

#-- Parser
parser = reqparse.RequestParser()
parser.add_argument("user_id", help="아이디 입력", location="json", required=True)
parser.add_argument("password", help="암호 입력", location="json", required=True)

#-- SQL
CHECK_ID =  "SELECT id,user_id,password FROM user_account WHERE (user_id=:user_id)"
TOKEN_INSERT = 'INSERT INTO user_account_token(uid, token) VALUES(:uid, :token)'
TOKEN_DELETE = 'DELETE FROM user_account_token WHERE uid=:uid'

#-- Logic
@Auth.expect(parser)
@Auth.response(200, 'Success') 
@Auth.response(404, 'Page Not Found')
@Auth.response(500, 'Internal Server Error')
@Auth.route('/login')
class AuthLogin(Resource):
    def post(self):
        """로그인"""

        #-- Validation.


        #-- 입력한 아이디/비번
        login = {
            'user_id' : request.json['user_id'],
            'password': request.json['password']
        }

        #-- DB에 있는 아이디, 비밀번호(str → byte)
        db_row= app.db2.execute(text(CHECK_ID),login).first()
        db_index_id = db_row[0]
        db_user_id = db_row[1]
        db_password = db_row[2]
        db_byte_password = bytes(db_password, encoding = "utf-8")

        #-- DB에 아이디 있는지 확인
        if login['user_id'] != db_user_id:
            return {
                "message" : "등록된 사용자가 없습니다."
            }, 404
        
        #-- 입력한 비번과 DB에 저장된 비번 같은지 확인. / 암호 찾았을 때, 임시 암호로도 로그인 가능하게.(12/23)  
        elif not bcrypt.checkpw(login['password'].encode('utf-8'), db_byte_password) and login['password'] != db_password:
            return {
                "message" : "비밀번호가 틀립니다."
            }, 404
        
        #-- 아이디, 비밀번호 옳게 입력했을 경우.(JWT생성)
        else:
            token = {
                'uid' : db_index_id,
                'token': jwt.encode({'name': login['user_id'], 'exp':datetime.utcnow() + timedelta(hours=9) + timedelta(seconds=30)}, "어케스헬인파4321", algorithm="HS256")
            }

            token_delete = app.db2.execute(text(TOKEN_DELETE),token)
            token_row = app.db2.execute(text(TOKEN_INSERT),token)
            return token['token']