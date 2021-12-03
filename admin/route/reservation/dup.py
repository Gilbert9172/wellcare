from flask_restx import Resource, reqparse
from .reservation import Reservation
import app
from sqlalchemy import text
from datetime import datetime
import numpy

parser = reqparse.RequestParser()
# parser = request 값.
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)


#-- Token_Sql
TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'

#-- Sql_Header
SQL_HEAD1 = 'SELECT user.id, user_name, user_birth, user_gender, user_phone, resv_flag '
SQL_HEAD2 = 'SELECT user.id, user_name, user_phone, resv_date '


#-- Sql_Body
SQL_BODY1 = 'FROM user '\
            'INNER JOIN resv_consultation '\
            'ON user.id = resv_consultation.user_id '


#-- Sql_Query
SQL_QUERY1 = 'WHERE (user_name NOT LIKE "%스트%" AND \
                    user_name NOT LIKE "%st%" AND \
                    user_name NOT LIKE "%차방문%" AND \
                    user_name NOT LIKE "%연구소%") '

SQL_QUERY2 = 'AND (resv_flag=0 OR resv_flag=2 OR resv_flag=4) '

SQL_QUERY3 = 'GROUP BY user_phone '


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

        q = {}
        sql_query1 = SQL_HEAD1 + SQL_BODY1 + (SQL_QUERY1 + SQL_QUERY2 + SQL_QUERY3)
        row = app.db.execute(text(sql_query1)).fetchall()

        #-- row에서 20~70대인 사람.
        new_row = []
        for i in row:
            year = int(i['user_birth'][0:2])

            if year <= 2:
                new_row.append(i)
            elif year >= 42:
                new_row.append(i)

        reservations = len(new_row)


        #-- 20~70대 예약자 성별 통계
        def gender_ratio(x):
            genders = []
            for i in range(x):
                gender = new_row[i]['user_gender']
                if gender == '남성':
                    genders.append(0)
                else:
                    genders.append(1)

            # 퍼센트는 따로 계산하지 않아도 된다.
            male_ratio = int(genders.count(0)/len(genders)*100)
            female_ratio = int(genders.count(1)/len(genders)*100)

            return [male_ratio, female_ratio]

        # print(f'예약자 성별 통계(남,여): {gender_ratio(reservations)}')


        #-- 예약자 연령대 통계(20대~70대)
        def age_ratio(x):
            ages = [] 
            for i in range(x):
                birth = int(new_row[i]['user_birth'][0:2])
                if birth <= 3:
                    age = datetime.today().year - (2000+birth) + 1
                    ages.append(age)
                elif birth >= 43:
                    age = datetime.today().year - (1900+birth) + 1
                    ages.append(age)

            stats = []
            for i in numpy.arange(1,4,0.5):
                age_ratio = list(map(lambda x: 20*i<=x<20*(i+0.5), ages))
                stat = int(round(age_ratio.count(True)/x,2)*100)
                stats.append(stat)
            
            return stats

        # print(f'예약자 연령대 통계(20대 ~ 70대): {age_ratio(reservations)}')



        #-- 월별 예약 건수 비율.
        sql_query2 = SQL_HEAD2 + SQL_BODY1 + (SQL_QUERY1 + SQL_QUERY3)
        row2 = app.db.execute(text(sql_query2)).fetchall()  

        # def month_ratio(self):
            
        months_2021, months_2022 = [],[]
        for i in row2:

            date = str(i['resv_date']).split("-")
            year = date[0]
            month = date[1]

            if year == '2021':
                months_2021.append(int(month))
            elif year == '2022':
                months_2022.append(int(month))

        cnt_months_2021 = list(map(lambda x: int((months_2021.count(x)/len(months_2021))*100), range(1,13)))
        cnt_months_2022 = list(map(lambda x: int((months_2022.count(x)/len(months_2022))*100), range(1,13)))
        print(cnt_months_2021,cnt_months_2022,sep="\n")


        return {
            'code': 'success',
            'message': 'success',
            'response': {
                '예약자 성별 통계(남/여)': gender_ratio(reservations),
                '예약자 연령대 통계(20~70대)': age_ratio(reservations),
                '월별 예약 건수 비율(2021)': cnt_months_2021,
                '월별 예약 건수 비율(2022)': cnt_months_2022,
            }
        }, 200