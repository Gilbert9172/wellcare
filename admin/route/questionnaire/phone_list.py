from flask import request
from flask_restx import Resource, reqparse
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null
from .questionnaire import Questionnaire
import app
from datetime import datetime
from sqlalchemy import text

parser = reqparse.RequestParser()

# SQL문 HEAD
QUESTIONNAIRE_COUNT_SQL = 'SELECT count(*) as cnt '
QUESTIONNAIRE_SELECT_SQL = 'SELECT * '

# SQL문 BODY
QUESTIONNAIRE_SELECT_BODY = 'FROM complete_check CC LEFT OUTER JOIN (SELECT id, agree_name, agree_birth, agree_phone FROM agree) A ON A.id = CC.agree_id WHERE 1'


@Questionnaire.route('/phone_list')
class Phone_list(Resource):
    @Questionnaire.expect(parser)
    @Questionnaire.response(200, 'Success')
    @Questionnaire.response(401, 'Unauthorized')
    @Questionnaire.response(500, 'Internal Server Error')
    def get(self):
        """안드로이드 문진표 리스트 API"""
        args = parser.parse_args()
        
        q = dict()
        
        sql_body = QUESTIONNAIRE_SELECT_BODY
        count_sql = QUESTIONNAIRE_COUNT_SQL + sql_body

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
