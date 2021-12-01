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
CHECKUP_COUNT_SQL = 'SELECT count(*) as cnt '
CHECK_SELECT_SQL = 'SELECT * '
# SQL문 BODY
CHECK_SELECT_BODY = 'FROM checkup_list CC LEFT OUTER JOIN (SELECT id, agree_name, agree_birth, agree_phone FROM agree) A ON A.id = CC.agree_id WHERE 1'


@Questionnaire.route('/phone_check_list')
class Phone_chekc_list(Resource):
    @Questionnaire.expect(parser)
    @Questionnaire.response(200, 'Success')
    @Questionnaire.response(401, 'Unauthorized')
    @Questionnaire.response(500, 'Internal Server Error')
    def get(self):
        """안드로이드 체크 리스트 API"""
        args = parser.parse_args()
        q = dict()
        sql_body = CHECK_SELECT_BODY
        count_sql = CHECKUP_COUNT_SQL + sql_body
        select_sql = CHECK_SELECT_SQL + sql_body
        rows = app.db2.execute(text(select_sql), q).fetchall()
        cnt = app.db2.execute(text(count_sql), q).fetchone()
        resp = []
        for row in rows:
            r = {}
            r['agree_id'] = row['agree_id']
            r['agree_name'] = row['agree_name']
            r['agree_birth'] = row['agree_birth']
            r['agree_phone'] = row['agree_phone']
            r['wash_flag'] = row['wash_flag']
            r['agree_flag'] = row['agree_flag']
            r['blood_flag'] = row['blood_flag']
            r['hair_flag'] = row['hair_flag']
            r['skinmv_flag'] = row['skinmv_flag']
            r['bowel_flag'] = row['bowel_flag']
            r['hrv_flag'] = row['hrv_flag']
            r['body_flag'] = row['body_flag']
            r['mind_flag'] = row['mind_flag']
            r['brain_flag'] = row['brain_flag']
            r['skin_flag'] = row['skin_flag']
            r['eye_flag'] = row['eye_flag']
            r['exercise_flag'] = row['exercise_flag']
            r['smart_flag'] = row['smart_flag']
            r['modified_date'] = row['modified_date'].strftime(
                '%Y-%m-%d %H:%M:%S')
            resp.append(r)
        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'count': cnt['cnt'],
                'List': resp
            }
        }, 200
