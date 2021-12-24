#-- Modules 
from flask import request
from flask_restx import reqparse, Resource
from .auth import Auth
from sqlalchemy import text
import app,bcrypt


#-- Parser
parser = reqparse.RequestParser()
parser.add_argument("user_id", help="사용자 아이디", location="json", required=True)
parser.add_argument("new_pw", help="새로운 비밀번호", location="json", required=True)
parser.add_argument("ch_new_pw", help="새로운 비번 확인", location="json", required=True)


#-- SQL
CHANGE_PW = "UPDATE user_account SET password=:new_pw WHERE user_id=:user_id "


#-- Logic
@Auth.expect(parser)
@Auth.response(200, 'Success')
@Auth.response(404, 'Page Not Found')
@Auth.response(500, 'Server Error')
@Auth.route('/change-pw')
class NewPw(Resource):
    def put(self):
        """비밀번호 변경"""
        if request.json['new_pw'] != request.json['ch_new_pw']:
            return {
               "message" : "비밀번호가 일치하지 않습니다." 
            }, 500
        else:
            encrypted_password = bcrypt.hashpw(request.json['new_pw'].encode("utf-8"), bcrypt.gensalt())
            str_encrypted_password = encrypted_password.decode('utf-8')

            new_password = {
                'new_pw' : str_encrypted_password,
                'user_id' : request.json['user_id']
            }

            app.db2.execute(text(CHANGE_PW),new_password)

        return 200