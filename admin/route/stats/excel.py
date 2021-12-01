from flask import request
from flask import send_from_directory
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .stats import Stats
import app
from sqlalchemy import text

from datetime import datetime
import time
from openpyxl.styles import Alignment
import pandas as pd

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('timestamp', help='timestamp', type=int, required=True)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'

AGREE_SELECT_SQL = 'SELECT DISTINCT birth, agree_gender, agree_phone FROM (SELECT DISTINCT SUBSTR(agree_birth,1,2) AS birth, agree_gender, agree_phone FROM agree)AS A ORDER BY birth DESC'
AGREE_COUNT_SQL = 'SELECT COUNT(*) FROM (SELECT DISTINCT SUBSTR(agree_birth,1,2) AS birth, agree_gender, agree_phone FROM agree)AS A'

@Stats.route('/excel')
class Excel(Resource):
    @Stats.expect(parser)
    @Stats.response(200, 'Success')
    @Stats.response(500, 'Failed')
    def get(self):
        """참여자 통계 Excel API"""
        args = parser.parse_args()
        token = args['Authorization']

        if token == None:
            return {
                'code': 'fail',
                'message': '토큰정보가 없습니다',
                'response': {}
            }, 401

        token = token.split(' ')[1]
        r = app.db.execute(text(TOKEN_CHECK_SQL), {
            'token': token
        }).fetchone()
        if r == None:
            return {
                'code': 'fail',
                'message': '토큰이 유효하지 않습니다',
                'response': {}
            }, 401

        row = app.db2.execute(text(AGREE_SELECT_SQL)).fetchall()

        row_id = app.db2.execute(text(AGREE_COUNT_SQL)).fetchone()
        stats_list = []
        first_row = ['성별','나이','참여자수','비율']

        for idx in range(0, len(row)):
            t = {}
            if row[idx]['agree_gender'] != None:
                t['성별'] = row[idx]['agree_gender']        
            else:
                t['성별'] = '-'        
            
            # 나이 계산
            if int(row[idx]['birth']) < 30:
                birthYear = '20' + row[idx]['birth']
            else:
                birthYear = '19' + row[idx]['birth']
            
            thisYear = datetime.today().year
            age = int(thisYear) - int(birthYear) + 1
            t['나이'] = str(age)

            # 성별,나이 같은 경우 참여자수 +1
            count = 0
            for idx2 in range(0, len(row)):
                if row[idx]['birth'] == row[idx2]['birth'] and row[idx]['agree_gender'] == row[idx2]['agree_gender']:
                    count += 1
            t['참여자수'] = count
                    
            t['비율'] = str(round((count / int(list(row_id)[0]))*100,2)) + '%'
            stats_list.append(t)
            
        # 중복되는 (성별,나이 )세트 제거
        new_stats_list = []
        for v in stats_list:
            if v not in new_stats_list:
                new_stats_list.append(v)

        # 나이순으로 배열 재배치
        nsl = sorted(new_stats_list, key=lambda l : l['나이'])

        df = pd.DataFrame(data=nsl, columns=first_row)
        df.style.set_properties(**{'text-align': 'center'}).set_table_styles([ dict(selector='th', props=[('text-align', 'center')] ) ])
        now = datetime.now()
        now_datetime = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
        timestamp = time.mktime(datetime.strptime(now_datetime, '%Y-%m-%d %H:%M:%S').timetuple())
        timestamp_split = str(timestamp).split('.')[0]
        fname='export_list_' + str(timestamp_split) + '.xlsx'
        print(app.app.config['STATS_EXCEL_DIRECTORY'] + "/" + fname , ' : 경로!')
        df.to_excel(excel_writer=app.app.config['STATS_EXCEL_DIRECTORY'] + "/" + fname, index=False)
        return send_from_directory(app.app.config['STATS_EXCEL_DIRECTORY'], fname)
    
