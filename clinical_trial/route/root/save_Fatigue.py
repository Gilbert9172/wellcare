from os import close
from flask import request, jsonify
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from werkzeug.wrappers import Response
from .root import Root
from sqlalchemy import text
import json

import app

parser = reqparse.RequestParser()

FATIGUE_QUESTION_INSERT_SQL = 'INSERT INTO fatigue_question(agree_id, answer_text, answer) VALUES(:agree_id, :answer_text, :answer)'
COMPLETE_CHECK_UPDATE_SQL = 'UPDATE complete_check SET fatigue_flag=1 WHERE agree_id=:agree_id'

@Root.route('/Save_Fatigue', methods=['GET', 'POST'])
class Save_Fatigue(Resource):
    @Root.expect(parser)
    @Root.response(200, 'Success')
    @Root.response(500, 'Internal Server Error')
    def post(self):
        """피로도 API"""
        args = parser.parse_args()
        
        if request.get_json != None:
            json_data = request.get_json()

        try:
            data_all = dict()
            data_all = json_data['answer_list'][0]

            for key, value in data_all.items():
                q = {}

                q['agree_id'] = json_data['agree_id']
                q['answer_text'] = key
                q['answer'] = value

                row_id = app.db2.execute(text(FATIGUE_QUESTION_INSERT_SQL), q).lastrowid

            wq = {}
            wq['agree_id'] = json_data['agree_id']
            row_id = app.db2.execute(text(COMPLETE_CHECK_UPDATE_SQL), wq).lastrowid

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
