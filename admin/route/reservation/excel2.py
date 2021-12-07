from flask import request
from flask_restx import Resource, reqparse
from flask import send_from_directory
from .reservation import Reservation
import app
from sqlalchemy import text
from datetime import datetime
import time
from openpyxl.styles import Alignment
import pandas as pd
from datetime import datetime
import numpy as np

"""
birth를 나이로 바꿔줘야함.
쿼리로 가져와서 나이 로직 처리.
"""


parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('start', help='시작 index', type=int, required=True, default=0)
parser.add_argument('size', help='페이지 수', type=int, required=True, default=10)
parser.add_argument('startdate', help='예약일자 시작', required=False)
parser.add_argument('enddate', help='예약일자 끝', required=False)
# parser.add_argument('birth', help='검색(생년월일 앞 두 자리)', required=True)
# parser.add_argument('gender', help='성별(전체(0), 남성(1), 여성(2)', type=int, required=True, default=0)
# parser.add_argument('status', help='상태(전체(0), 예약 완료(1), 예약 취소(2), 관리자 추가(3), 관리자 취소(4), 관리자 예약 변경(5), 등록 완료(6), 수집 완료(7)', type=int, required=True, default=0)
# parser.add_argument('sort', help='없음(0), 예약일(1), 생년월일(2), 상태(3)', type=int, required=True, default=0)
parser.add_argument('order', help='내림차순(0), 오름차순(1)', type=int, required=True, default=0)

#-- Token
TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'

#-- SQL Header
SQL_HEAD = 'SELECT user.id, user_name, user_birth, user_gender,user_phone '

#-- SQL Body
SQL_BODY = 'FROM user '\
            'INNER JOIN resv_consultation '\
            'ON user.id = resv_consultation.user_id ' \

#-- SQL Query
SQL_QUERY1 = 'WHERE (user_name NOT LIKE "%스트%" AND \
user_name NOT LIKE "%st%" AND \
user_name NOT LIKE "%차방문%" AND \
user_name NOT LIKE "%연구소%") \
AND (resv_flag=0 OR resv_flag=2 OR resv_flag=4) '

SQL_QUERY2 = 'AND (LEFT(user_birth,2) > 43 OR 3> LEFT(user_birth,2) > 0) '

# SQL_QUERY3 = 'AND user_gender LIKE :gender '

# SQL_QUERY4 = 'AND user_birth LIKE :birth '

SQL_QUERY3 = 'GROUP BY user_phone '





@Reservation.route('/excel2')
class Excel(Resource):
    @Reservation.expect(parser)
    @Reservation.response(200, 'Success')
    @Reservation.response(401, 'Unauthorized')
    @Reservation.response(500, 'Internal Server Error')
    def get(self):
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

        base_sql = SQL_HEAD + SQL_BODY + SQL_QUERY1 + SQL_QUERY2 + SQL_QUERY3
        row = app.db.execute(text(base_sql)).fetchall()

        #-- 남성
        def man():
            row_man = [ i for i in row if i['user_gender']=="남성" ]
            
            man_ages = []
            for i in range(len(row_man)):
                birth = int(row_man[i]['user_birth'][0:2])
                if birth <= 3:
                    age = datetime.today().year - (2000+birth) + 1
                    man_ages.append(age)
                elif birth >= 43:
                    age = datetime.today().year - (1900+birth) + 1
                    man_ages.append(age)                
            
            man_ages_cnt = [["남성",i,man_ages.count(i)] for i in range(20,80)]
            return man_ages_cnt

        #-- 여성
        def woman():
            row_woman = [ i for i in row if i['user_gender']=="여성" ]
            
            woman_ages = []
            for i in range(len(row_woman)):
                birth = int(row_woman[i]['user_birth'][0:2])
                if birth <= 3:
                    age = datetime.today().year - (2000+birth) + 1
                    woman_ages.append(age)
                elif birth >= 43:
                    age = datetime.today().year - (1900+birth) + 1
                    woman_ages.append(age)                
            
            woman_ages_cnt = [["여성",i,woman_ages.count(i)] for i in range(20,80)]
            return woman_ages_cnt

        #-- 남성,여성 각가 df추출
        df_m = pd.DataFrame(data=man(), columns=["성별","나이","예약자 수"])
        df_w = pd.DataFrame(data=woman(), columns=["성별","나이","예약자 수"])


        #-- df_m, df_w concat
        df = pd.concat([df_m,df_w], axis=0)
        df["예약자 수"].replace(0,np.nan, inplace=True)
        df = df.dropna(axis=0)
        df = df.sort_values(by=["나이"])
        df = df.reset_index(drop=True)


        #-- 비율 df
        ratio = list(map(lambda x: str(round(x/sum(df["예약자 수"])*100,2))+"%", df["예약자 수"]))
        df_ratio = pd.DataFrame(data=ratio,columns=["비율"])

        #-- df와 df_ratio concat
        pdf = pd.concat([df,df_ratio],axis=1)

        #-- datetime module을 활용하 파일 이름명 지정해주는 로직. 
        now = datetime.now()

        #-- datetime → 문자열 <class 'str'>
        str_now = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')      

        #-- str_now을 struct_time으로
        struct_now = time.strptime(str_now,'%Y-%m-%d %H:%M:%S')

        # time.mktime(struct_type이 들어가야함.) / 시간(초)을 돌려준다.
        t_in_secs = str(int(time.mktime(struct_now)))


        fname = 'export_list_' + t_in_secs + '.xlsx'
        # print(app.app.config['RESERV_EXCEL_DIRECTORY'] + "/" + fname, ' : 경로!')


        #-- 엑셀로 추출.
        pdf.to_excel(
            excel_writer=app.app.config['RESERV_EXCEL_DIRECTORY'] + "/" + fname, index=False
        )


        return send_from_directory(app.app.config['RESERV_EXCEL_DIRECTORY'], fname)