from os import close
from flask import request, jsonify
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from werkzeug.wrappers import Response
from .root import Root
from sqlalchemy import text
import json

import app

parser = reqparse.RequestParser()
parser.add_argument('id', help='동의서 번호', location='json', type=int, required=True)

SELECT_AGREE_ID_SQL = 'SELECT agree_name, agree_birth, agree_phone FROM agree WHERE id=:id'
SELECT_USER_ID_SQL = 'SELECT id FROM user WHERE user_name=:agree_name AND user_birth=:agree_birth AND user_phone=:agree_phone'
RESV_FLAG_UPDATE_SQL = 'UPDATE resv_consultation SET resv_flag=6 WHERE user_id=:user_id'


@Root.route('/checklist_check')
class Checklist_check(Resource):
    @Root.expect(parser)
    @Root.response(200, 'Success')
    @Root.response(500, 'Internal Server Error')
    def post(self):
        """체크리스트 작성완료 체크 API"""
        args = parser.parse_args()
        
        try:
            q = {}
            q['id'] = args['id']
            row = app.db2.execute(text(SELECT_AGREE_ID_SQL), q).fetchone()

            wq = {}
            wq['agree_name'] = row['agree_name']
            wq['agree_birth'] = row['agree_birth']
            wq['agree_phone'] = row['agree_phone']
            row2 = app.db.execute(text(SELECT_USER_ID_SQL), wq).fetchone()

            tq = {}
            tq['user_id'] = row2['id']
            row3 = app.db.execute(text(RESV_FLAG_UPDATE_SQL), tq).lastrowid

        except Exception as e:
            print(e)
            return {
                'code': 'fail',
                'message': 'Internal Server Error',
                'response': {
                    'flag': False
                }
            }, 500 
       
        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'flag': True
            }
        }, 200
