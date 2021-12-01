from os import close
from flask import request, jsonify
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from werkzeug.wrappers import Response
from .root import Root
from sqlalchemy import text
import json

import app

parser = reqparse.RequestParser()
parser.add_argument('agree_name', help='이름', location='json', required=True)
parser.add_argument('agree_birth', help='생년월일', location='json', required=True)
parser.add_argument('agree_phone', help='휴대전화', location='json', required=True)

AGREEE_SELECT_SQL = 'SELECT id FROM agree WHERE agree_name=:agree_name AND agree_birth=:agree_birth AND agree_phone=:agree_phone'

@Root.route('/Agree_Info', methods=['GET', 'POST'])
class Agree_Info(Resource):
    @Root.expect(parser)
    @Root.response(200, 'Success')
    @Root.response(500, 'Internal Server Error')
    def post(self):
        """참여자 ID 조회 API"""
        args = parser.parse_args()

        try:
            # if request.get_json != None:
            #     agree = request.get_json()
            q={}
            q['agree_name'] = args['agree_name']
            q['agree_birth']= args['agree_birth']
            q['agree_phone']= args['agree_phone']

            row = app.db2.execute(text(AGREEE_SELECT_SQL),q).fetchone()

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
                'id': row['id'],
            }
        }