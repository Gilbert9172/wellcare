from flask import request, jsonify
from sqlalchemy.sql.schema import Index
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from werkzeug.wrappers import Response
from .root import Root
from sqlalchemy import text
import json
import app

parser = reqparse.RequestParser()

COMMON_QUESTION_INSERT_SQL = 'INSERT INTO common_question(agree_id, category_id, answer_text, answer) VALUES(:agree_id, :category_id,:answer_text, :answer)'
COMPLETE_CHECK_UPDATE_SQL = 'UPDATE complete_check SET common_flag=1 WHERE agree_id=:agree_id'

@Root.route('/Save_Common', methods=['GET', 'POST'])
class Save_Common(Resource):
    @Root.expect(parser)
    @Root.response(200, 'Success')
    @Root.response(500, 'Internal Server Error')
    def post(self):
        """건강검진 종합 API"""
        args = parser.parse_args()

        try:
            
            if request.get_json != None:
                common = request.get_json()
                
                answer_list1 = common['answer_list1']
                answer_list2 = common['answer_list2']
                answer_list3 = common['answer_list3']
                answer_list4 = common['answer_list4']

                for row in answer_list1['answer_list']:
                    q={}
                    q['agree_id'] = common['agree_id']
                    q['category_id'] = answer_list1['category_id']
                    q['answer_text'] = row['answer_text']
                    q['answer'] = row['answer']
                    row_id = app.db2.execute(text(COMMON_QUESTION_INSERT_SQL), q).lastrowid
                
                for row in answer_list2['answer_list']:
                    q={}
                    q['agree_id'] = common['agree_id']
                    q['category_id'] = answer_list2['category_id']
                    q['answer_text'] = row['answer_text']
                    q['answer'] = row['answer']
                    row_id = app.db2.execute(text(COMMON_QUESTION_INSERT_SQL), q).lastrowid

                for row in answer_list3['answer_list']:
                    q={}
                    q['agree_id'] = common['agree_id']
                    q['category_id'] = answer_list3['category_id']
                    q['answer_text'] = row['answer_text']
                    q['answer'] = row['answer']
                    row_id = app.db2.execute(text(COMMON_QUESTION_INSERT_SQL), q).lastrowid

                for row in answer_list4['answer_list']:
                    q={}
                    q['agree_id'] = common['agree_id']
                    q['category_id'] = answer_list4['category_id']
                    q['answer_text'] = row['answer_text']
                    q['answer'] = row['answer']
                    row_id = app.db2.execute(text(COMMON_QUESTION_INSERT_SQL), q).lastrowid

                wq = {}
                wq['agree_id'] = common['agree_id']
                row_id = app.db2.execute(text(COMPLETE_CHECK_UPDATE_SQL), wq).lastrowid

        except Exception as e:
            print(e)
            return{
                'code': 'fail',
                'message':'Internal Server Error',
                'response':{
                    'flag':False
                }
            },500

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'flag': True
            }
        }, 200
