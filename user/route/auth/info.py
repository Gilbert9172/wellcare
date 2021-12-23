#-- Modules
from flask import request
from flask_restx import Resource, reqparse
from sqlalchemy import text
from .auth import Auth
import app

#-- Parse
parser = reqparse.RequestParser()
parser.add_argument("Authorization", help="Bearer 토큰", location='headers', required=True)

#-- SQL
GET_TOKEN = "SELECT * FROM user_account_token WHERE (token=:token)"
USER_TOKEN_INNER = "SELECT ua.user_id, ua.email, ua.name, ua.phone FROM user_account ua LEFT JOIN user_account_token uat ON ua.id = uat.uid WHERE uid=:uid;"

#-- Logic
@Auth.route('/info')
@Auth.expect(parser)
@Auth.response(200, 'Success')
@Auth.response(404, 'Page Not Found')
@Auth.response(500, 'Server Error')
class AuthInFo(Resource):
    def get(self):
        token = request.headers['Authorization']
        token = {
            'token':token.split(' ')[1]
        }
        token_row = app.db2.execute(text(GET_TOKEN),token).first()
        
        if token_row :
            uid = {'uid':token_row['uid']}
            inner_row = app.db2.execute(text(USER_TOKEN_INNER),uid).first()
            
            user_info = {
                'user_id' : inner_row[0],
                'user_email' : inner_row[1],
                'user_name' : inner_row[2],
                'user_phone' : inner_row[3],
            }
        else:
            return {
                "code" : 500,
                "message" : "존재하지 않는 정보"
            }, 500

        return {
            "code" : 200,
            "message" : "요청한 정보",
            "respone" : user_info
        }, 200