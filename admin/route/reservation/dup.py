"""
-중복제거
SELECT DISTINCT (컬럼명) FROM 테이블명

-중복된 데이터 제거 후 COUNT
SELECT COUNT(DISTINCT (컬럼명)) FROM 테이블명

-중복찾기
SELECT 컬럼명 FROM 테이블명 GROUP BY 컬럼명 HAVING COUNT (컬럼명) > 1
"""

"""
1. 중복 예약 제외 "이름", "휴대폰 번호", "생년월일", "성별"
(휴대폰 번호는 개개인의 고유번호임으로 휴대폰 번호로만 조회.)

SQL_HEAD : SELECT user_name, user.user_birth, user_phone
SQL_BODY : FROM user, resv_consultation
SQL_Qeury : WHERE user.id = resv_consultation.id

2. 예약된 이름이 "연구소 비는 날", "이차방문", "2차 방문", 또는 "테스트"
SQL_HEAD : SELECT user_name 
SQL_BODY : FROM user
SQL_Qeury : WHERE user_name LIKE '%연구소%' OR
            user_name LIKE '%차%' OR 
            user_name LIKE '%방문%' OR
            user_name LIKE '%테스트%' OR 
            user_name LIKE '%test%'

3. 상태가 "예약 취소(1)" OR "관리자 취소(3)"
SQL_HEAD : SELECT user_id, user_name, resv_flag 
SQL_BODY : FROM user,resv_consultation
SQL_Qeury : WHERE resv_flag=1 OR resv_flag=3
"""

"""
SQL HEAD / SQL BODY 를 따로 정의해주기.
"""

from flask import request
from flask_restx import Resource, reqparse
from .reservation import Reservation
import app
from sqlalchemy import text

parser = reqparse.RequestParser()
# parser = request 값.
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)



TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'

# SQL문 HEAD
SQL_HEAD1 = 'SELECT user_name, user.user_birth, user_phone '
# SQL_HEAD2 = 'SELECT user_name ' 
# SQL_HEAD = 'SELECT user_id, user_name, resv_flag '
USER_SELECT = 'SELECT * FROM user'

# SQL문 Body
SQL_BODY1 = 'FROM user, resv_consultation '

@Reservation.route('/dup')
class Dup(Resource):
    @Reservation.expect(parser)
    @Reservation.response(200, 'Success')
    @Reservation.response(401, 'Unauthorized')
    @Reservation.response(500, 'Internal Server Error')
    
    def get(self):
        args = parser.parse_args()

        # 토큰 정의
        token = args['Authorization']

        if token == None:
            return {
                'code': 'fail',
                'messages': '토큰정보가 없습니다.',
                'response': {}
            }, 401
        
        token  = token.split(' ')[1]

        # 고유 토큰 담겨져 있음.
        row = app.db.execute(text(TOKEN_CHECK_SQL),{
            'token':token
        })

        if row == None:
            return {
                'code': 'fail',
                'message': '토큰이 유효하지 않습니다',
                'response': {}
            }, 401
        ###### print찍어보기.

        q = {}
        s = SQL_HEAD1 + SQL_BODY1 + 'WHERE user.id = resv_consultation.id '
        row = app.db.execute(text(s),q).fetchall()

        from datetime import datetime
        years = [int(row[i]['user_birth'][0:2]) for i in range(len(row))] 
        
        ages = []
        for year in years:
            if year > 21:
                age = datetime.today().year - (1900+year) + 1
                ages.append(age)
            else:
                age = datetime.today().year - (2000+year) + 1
                ages.append(age)
        ages.sort()

        for i in range(1,11):
            one = list(map(lambda x: 10*(i-1)<x<=10*i, ages))
            print(one.count(True))