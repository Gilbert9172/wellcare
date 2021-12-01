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
parser.add_argument('wash_flag', help='세안/환복', location='json', required=True)
parser.add_argument('agree_flag', help='설문지/동의서', location='json', required=True)
parser.add_argument('blood_flag', help='혈액/소변', location='json', required=True)
parser.add_argument('hair_flag', help='모발 검사', location='json', required=True)
parser.add_argument('skinmv_flag', help='피부 마이크로 바이옴', location='json', required=True)
parser.add_argument('bowel_flag', help='장 마이크로 바이옴', location='json', required=True)
parser.add_argument('hrv_flag', help='HRV', location='json', required=True)
parser.add_argument('body_flag', help='신체계측/체지방측정', location='json', required=True)
parser.add_argument('mind_flag', help='Mind-in', location='json', required=True)
parser.add_argument('brain_flag', help='뇌인지 측정', location='json', required=True)
parser.add_argument('skin_flag', help='피부 리더기', location='json', required=True)
parser.add_argument('eye_flag', help='안저 촬영', location='json', required=True)
parser.add_argument('exercise_flag', help='운동 측정', location='json', required=True)
parser.add_argument('smart_flag', help='스마트 밴드', location='json', required=True)

CHECKUPLIST_UPDATE_SQL = 'UPDATE checkup_list SET wash_flag=:wash_flag, agree_flag=:agree_flag, blood_flag=:blood_flag, hair_flag=:hair_flag, skinmv_flag=:skinmv_flag, bowel_flag=:bowel_flag, hrv_flag=:hrv_flag, body_flag=:body_flag, mind_flag=:mind_flag, brain_flag=:brain_flag, skin_flag=:skin_flag, eye_flag=:eye_flag, exercise_flag=:exercise_flag, smart_flag=:smart_flag WHERE agree_id=:agree_id'

@Root.route('/modified_checklist', methods=['GET', 'POST'])
class Modified_checklist(Resource):
    @Root.expect(parser)
    @Root.response(200, 'Success')
    @Root.response(500, 'Internal Server Error')
    def post(self):
        """체크리스트 수정 API"""
        args = parser.parse_args()

        try:
            q={}
            q['agree_id'] = args['agree_id']
            q['wash_flag'] = args['wash_flag'],
            q['agree_flag'] = args['agree_flag'],
            q['blood_flag'] = args['blood_flag'],
            q['hair_flag'] = args['hair_flag'],
            q['skinmv_flag'] = args['skinmv_flag'],
            q['bowel_flag'] = args['bowel_flag'],
            q['hrv_flag'] = args['hrv_flag'],
            q['body_flag'] = args['body_flag'],
            q['mind_flag'] = args['mind_flag'],
            q['brain_flag'] = args['brain_flag'],
            q['skin_flag'] = args['skin_flag'],
            q['eye_flag'] = args['eye_flag'],
            q['exercise_flag'] = args['exercise_flag'],
            q['smart_flag'] = args['smart_flag']
            row = app.db2.execute(text(CHECKUPLIST_UPDATE_SQL),q).lastrowid
            
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
                'flag': True
            }
        }