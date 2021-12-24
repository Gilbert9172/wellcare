#-- Modules
from flask import request
from flask_restx import Resource, reqparse
from .auth import Auth
from sqlalchemy import text
import app, bcrypt


#-- Parser
parser = reqparse.RequestParser()
parser.add_argument("email", help="이메일 확인", location="headers", required=True)
parser.add_argument("password", help="비밀번호 확인", location="headers", required=True)


#-- SQL
CHECK_EMAIL = "SELECT user_id, password, email, name FROM user_account WHERE email LIKE :email"


#-- Logic
@Auth.expect(parser)
@Auth.response(200, 'Success')
@Auth.response(404, 'Page Not Found')
@Auth.response(500, 'Server Error')
@Auth.route('/find-id')
class FindId(Resource):
    def get(self):
        """아이디 찾기"""
        serach_info = {
            'email' : request.headers['email'],
            'pw': request.headers['password']
        }

        search_db = app.db2.execute(text(CHECK_EMAIL),serach_info).first()
        
        db_email = search_db['email']
        db_pw = bytes(search_db['password'], encoding='utf-8')
        
        if db_email:
            if bcrypt.checkpw(serach_info['pw'].encode('utf-8'), db_pw):

                search_result = {
                    '아이디' : search_db['user_id'],
                }

            else:
                return {
                    'code':500,
                    'message':"비밀번호가 틀렸습니다."
                }, 500

        else:
            return {
                'code':500,
                'massage':"이메일 주소를 정확하게 입력해주세요."
            }, 500

        return search_result