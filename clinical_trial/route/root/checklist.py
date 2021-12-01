from os import close
from flask import request, jsonify
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from werkzeug.wrappers import Response
from .root import Root
from sqlalchemy import text
import json

import app

parser = reqparse.RequestParser()
parser.add_argument('agree_id', help='동의서 ID', location='json', required=True)

CHECKUPLIST_SELECT_SQL = 'SELECT * FROM checkup_list WHERE agree_id=:agree_id'

@Root.route('/checklist', methods=['GET', 'POST'])
class Checklist(Resource):
    @Root.expect(parser)
    @Root.response(200, 'Success')
    @Root.response(500, 'Internal Server Error')
    def post(self):
        """체크리스트 조회 API"""
        args = parser.parse_args()

        try:
            q={}
            q['agree_id'] = args['agree_id']
            row = app.db2.execute(text(CHECKUPLIST_SELECT_SQL),q).fetchone()
        except Exception as e:
            print(e)
            return{
                'code': 'fail',
                'message':'Internal Server Error',
                'response':{
                    'flag':False
                }
            },500

        return{
            'code':'success',
            'message':'success',
            'response':{
                'agree_id': row['agree_id'],
                'wash_flag': row['wash_flag'],
                'agree_flag': row['agree_flag'],
                'blood_flag': row['blood_flag'],
                'hair_flag': row['hair_flag'],
                'skinmv_flag': row['skinmv_flag'],
                'bowel_flag': row['bowel_flag'],
                'hrv_flag': row['hrv_flag'],
                'body_flag': row['body_flag'],
                'mind_flag': row['mind_flag'],
                'brain_flag': row['brain_flag'],
                'skin_flag': row['skin_flag'],
                'eye_flag': row['eye_flag'],
                'exercise_flag': row['exercise_flag'],
                'smart_flag': row['smart_flag']
            }
        }