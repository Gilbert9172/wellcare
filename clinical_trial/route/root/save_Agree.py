from os import close
from flask import request, jsonify
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from werkzeug.wrappers import Response
from .root import Root
import secrets
import werkzeug
import os
import time
from sqlalchemy import text
import json

import app

parser = reqparse.RequestParser()
parser.add_argument('agree_name', help='이름', location='json', required=True)
parser.add_argument('agree_birth', help='생년월일', location='json', required=True)
parser.add_argument('agree_gender', help='성별', location='json', required=True)
parser.add_argument('agree_phone', help='휴대전화', location='json', required=True)

AGREEE_INSERT_SQL = 'INSERT INTO agree(agree_name,agree_birth,agree_gender,agree_phone) VALUES(:agree_name, :agree_birth,:agree_gender, :agree_phone)'
COMPLETE_CHECK_INSERT_SQL = 'INSERT INTO complete_check(agree_id) VALUES(:agree_id)'
CHECKUP_LIST_INSERT_SQL = 'INSERT INTO checkup_list(agree_id) VALUES(:agree_id)'

@Root.route('/Save_Agree', methods=['GET', 'POST'])
class Save_Agree(Resource):
    @Root.expect(parser)
    @Root.response(200, 'Success')
    @Root.response(500, 'Internal Server Error')
    def post(self):
        """동의서2 API"""
        args = parser.parse_args()

        try:
            if request.get_json != None:
                agree = request.get_json()

                agree['AGREE_NAME'] = args['agree_name']
                agree['AGREE_BIRTH']= args['agree_birth']
                agree['AGREE_GENDER'] = args['agree_gender']
                agree['AGREE_PHONE']= args['agree_phone']

                row = app.db2.execute(text(AGREEE_INSERT_SQL),agree).lastrowid

                wq = {}
                wq['agree_id'] = row
                row2 = app.db2.execute(text(COMPLETE_CHECK_INSERT_SQL), wq).lastrowid
                row3 = app.db2.execute(text(CHECKUP_LIST_INSERT_SQL), wq).lastrowid

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
                'agree_id':row,
                'agree_name':agree['AGREE_NAME'],
                'agree_birth':agree['AGREE_BIRTH'],
                'agree_gender':agree['AGREE_GENDER'],
                'agree_phone':agree['AGREE_PHONE']
            }
        }