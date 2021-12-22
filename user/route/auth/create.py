from flask import request
from flask_restx import Resource, reqparse
from .auth import Auth
from sqlalchemy import text
import app, bcrypt, jwt
#--
parser = reqparse.RequestParser()
parser.add_argument('user_id', help="아이디", location='json', required=True)
parser.add_argument('password', help="비밀번호", location='json', required=True)
parser.add_argument('email', help="이메일", location='json', required=True)
parser.add_argument("name", help="사용자 이름", location='json', required=True)
parser.add_argument('phone', help="휴대폰 번호", location='json', required=True)

#-- 
CHECK_ID = "SELECT user_id FROM user_account WHERE (user_id=:user_id)"

CHECK_EMAIL= "SELECT email FROM user_account WHERE (email=:email)"

ADD_USER = "INSERT INTO user_account (user_id, password, email, name, phone )\
            VALUES(:user_id, :password, :email, :name, :phone)"


#--

@Auth.response(200, 'Success')
@Auth.response(500, 'Internal Server Error')
@Auth.route('/signup')
class Signup(Resource):
    @Auth.expect(parser)
    def post(self):
        # args = parser.parse_args()
        
        #-- Password Hashing 
        encrypted_password = bcrypt.hashpw(request.json['password'].encode("utf-8"), bcrypt.gensalt()) 

        #-- 회원가입
        sign = {}
        sign['user_id'] = request.json['user_id'] 
        sign['password'] = encrypted_password.decode('utf-8')
        sign['email'] = request.json['email']
        sign['name'] = request.json['name']
        sign['phone'] = request.json['phone']

        
        #============================================= Validations =============================================#
        
        # 동일한 아이디가 존재할 경우
        check_id = app.db2.execute(text(CHECK_ID),sign).first()
        if check_id:
            return {
                "message" : "존재하는 아이디입니다."
            }, 500
    
        # 동일한 이메일이 존재할 경우
        check_email = app.db2.execute(text(CHECK_EMAIL), sign).first()
        if check_email:
            return {
                'message' : "존재하는 이메일 입니다."
            }, 500

        # 모두 정상일 경우 
        new = app.db2.execute(text(ADD_USER),sign)

        return {
            'code': 'Success',
            'message': '회원가입을 축하드립니다.'
        }, 200


        

