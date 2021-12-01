from flask import request
from flask_restx import Resource, reqparse
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null
from .questionnaire import Questionnaire
import app
from datetime import datetime
from sqlalchemy import text

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('start', help='시작 index', type=int, required=True, default=0)
parser.add_argument('size', help='페이지 수', type=int, required=True, default=10)
parser.add_argument('q', help='검색(이름)', required=False)
parser.add_argument('sort', help='없음(0), 마지막 작성일시(1)', type=int, required=True, default=0)
parser.add_argument('order', help='내림차순(0), 오름차순(1)', type=int, required=True, default=0)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'

# SQL문 HEAD
QUESTIONNAIRE_COUNT_SQL = 'SELECT count(*) as cnt '
QUESTIONNAIRE_SELECT_SQL = 'SELECT * '

# SQL문 BODY
QUESTIONNAIRE_SELECT_BODY = 'FROM complete_check CC LEFT OUTER JOIN (SELECT id, agree_name, agree_birth, agree_phone FROM agree) A ON A.id = CC.agree_id WHERE (CC.common_flag != 0 or CC.nutrition_flag != 0 or CC.cognitive_flag != 0 or CC.mental_flag != 0 or CC.stress_flag != 0 or CC.stomach_flag != 0 or CC.sleep_flag != 0 or CC.fatigue_flag != 0 or CC.samkim_flag != 0) '

# SQL문 조건
AGREE_Q_SQL = 'AND agree_name LIKE :q1 '
LIMIT_SQL = 'LIMIT :start, :size '


@Questionnaire.route('/list')
class List(Resource):
    @Questionnaire.expect(parser)
    @Questionnaire.response(200, 'Success')
    @Questionnaire.response(401, 'Unauthorized')
    @Questionnaire.response(500, 'Internal Server Error')
    def get(self):
        """문진표 리스트 API"""
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
        
        q = dict()
        sql_body = QUESTIONNAIRE_SELECT_BODY
        q['start'] = args['start']
        q['size'] = args['size']
        if args['q'] != None:
            q['q1'] = '%' + args['q'] + '%'
            sql_body += AGREE_Q_SQL
        count_sql = QUESTIONNAIRE_COUNT_SQL + sql_body

        if args['sort'] == 0:
            sql_body += 'ORDER BY CC.modified_date DESC '
        elif args['sort'] == 1:
            sql_body += 'ORDER BY CC.modified_date '
            if args['order'] == 0:
                sql_body += 'DESC '
            elif args['order'] == 1:
                sql_body += 'ASC '
            else:
                return {
                    'code': 'fail',
                    'message': 'order가 잘못되었습니다.'
                }, 500
        else:
            return {
                'code': 'fail',
                'message': 'sort가 잘못되었습니다.'
            }, 500
        
        sql_body += LIMIT_SQL

        select_sql = QUESTIONNAIRE_SELECT_SQL + sql_body
        
        rows = app.db2.execute(text(select_sql), q).fetchall()
        cnt = app.db2.execute(text(count_sql), q).fetchone()

        resp = []
        for row in rows:
            r = {}
            # 나이 계산
            if int(row['agree_birth'][0:2]) < 30:
                birthYear = '20' + row['agree_birth'][0:2]
            else:
                birthYear = '19' + row['agree_birth'][0:2]
            thisYear = datetime.today().year
            age = int(thisYear) - int(birthYear) + 1

            r['agree_id'] = row['agree_id']
            r['agree_name'] = row['agree_name']
            r['age'] = str(age)
            r['agree_phone'] = row['agree_phone']
            r['common_flag'] = row['common_flag']
            r['nutrition_flag'] = row['nutrition_flag']
            r['cognitive_flag'] = row['cognitive_flag']
            r['mental_flag'] = row['mental_flag']
            r['stress_flag'] = row['stress_flag']
            r['stomach_flag'] = row['stomach_flag']
            r['sleep_flag'] = row['sleep_flag']
            r['samkim_flag'] = row['samkim_flag']
            r['fatigue_flag'] = row['fatigue_flag']
            r['modified_date'] = row['modified_date'].strftime('%Y-%m-%d %H:%M:%S')
            resp.append(r)

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'count': cnt['cnt'],
                'List': resp
            }
        }, 200
