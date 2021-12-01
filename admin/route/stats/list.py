from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .stats import Stats
import app
from sqlalchemy import text

from datetime import datetime

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'

AGREE_SELECT_SQL = 'SELECT DISTINCT birth, agree_gender, agree_phone FROM (SELECT DISTINCT SUBSTR(agree_birth,1,2) AS birth, agree_gender, agree_phone FROM agree )AS A'
AGREE_COUNT_SQL = 'SELECT COUNT(*) FROM ( SELECT DISTINCT SUBSTR(agree_birth,1,2) AS birth, agree_gender, agree_phone FROM agree )AS A'

@Stats.route('/list')
class List(Resource):
    @Stats.expect(parser)
    @Stats.response(200, 'Success')
    @Stats.response(500, 'Failed')
    def post(self):
        """참여자 통계 List API"""
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
        row2 = app.db2.execute(text(AGREE_COUNT_SQL)).fetchall()
        
        stats_list = list()
        for idx in range(len(row)):
            t = {}
            t['id'] = idx + 1
            t['gender'] = row[idx]['agree_gender']        
            
            # 나이 계산
            if int(row[idx]['birth'][0:2]) < 30:
                birthYear = '20' + row[idx]['birth'][0:2]
            else:
                birthYear = '19' + row[idx]['birth'][0:2]
            
            thisYear = datetime.today().year
            age = int(thisYear) - int(birthYear) + 1

            t['age'] = str(age)
            stats_list.append(t)

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'List': stats_list
            }
        }, 200
