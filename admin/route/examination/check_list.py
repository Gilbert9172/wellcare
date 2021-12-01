from os import close
from flask import request, jsonify
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from werkzeug.wrappers import Response
from .examination import Examination
from sqlalchemy import text
import json
from datetime import datetime

import app

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('start', help='시작 index', type=int, required=True, default=0)
parser.add_argument('size', help='페이지 수', type=int, required=True, default=10)
parser.add_argument('q', help='검색(이름)', required=False)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'

# SQL문 HEAD
CHECKLIST_COUNT_SQL = 'SELECT count(*) as cnt '
CHECKLIST_SELECT_SQL = 'SELECT * '

# SQL문 BODY
CHECKLIST_SELECT_BODY = 'FROM checkup_list CL LEFT OUTER JOIN (SELECT id, agree_name FROM agree) A ON A.id = CL.agree_id WHERE 1 ORDER BY modified_date DESC '

# SQL문 조건
AGREE_Q_SQL = 'AND agree_name LIKE :q1 '
LIMIT_SQL = 'LIMIT :start, :size'

@Examination.route('/check_list')
class Check_list(Resource):
    @Examination.expect(parser)
    @Examination.response(200, 'Success')
    @Examination.response(401, 'Unauthorized')
    @Examination.response(500, 'Internal Server Error')
    def post(self):
        """체크리스트 API"""
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
        sql_body = CHECKLIST_SELECT_BODY
        q['start'] = args['start']
        q['size'] = args['size']
        if args['q'] != None:
            q['q1'] = '%' + args['q'] + '%'
            sql_body += AGREE_Q_SQL

        count_sql = CHECKLIST_COUNT_SQL + sql_body
        sql_body += LIMIT_SQL
        select_sql = CHECKLIST_SELECT_SQL + sql_body
        
        rows = app.db2.execute(text(select_sql), q).fetchall()
        cnt = app.db2.execute(text(count_sql), q).fetchone()

        resp = []
        for row in rows:
            r = {}
            r['agree_name'] = row['agree_name']
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
