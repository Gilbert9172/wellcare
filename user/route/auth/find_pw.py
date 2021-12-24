#-- Modules
from flask import request, jsonify
from flask_restx import reqparse, Resource
from .auth import Auth
from sqlalchemy import text
import app, bcrypt


#-- Parser
parser = reqparse.RequestParser()
parser.add_argument("user_id", help="회원 아이디", location="headers", required=True)
parser.add_argument("email", help="이메일", location="headers", required=True)

#-- SQL
CHECK_EMAIL_ID = "SELECT user_id, password, email FROM user_account WHERE user_id=:user_id AND email LIKE :email"


#-- Logic
@Auth.expect(parser)
@Auth.response(200, 'Success')
@Auth.response(404, 'Page Not Found')
@Auth.response(500, 'Server Error')
@Auth.route('/find-pw')
class FindPw(Resource):
    def get(self):
        """비밀번호 찾기"""
        search_info = {
            'user_id':request.headers['user_id'],
            'email':request.headers['email']
        }

        search_row = app.db2.execute(text(CHECK_EMAIL_ID), search_info).first()

        # search_row가 있으면 암호화된 비밀번호 반환.
        if search_row :
            search_pw = search_row['password']
            message = "비밀번호를 꼭 바꿔주세요."
        else:
            return {
                "message" : "회원정보가 없습니다."
            }, 500
        
        return {
            'pw' : search_pw,
            'message':message
        }, 200