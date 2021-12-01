from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .questionnaire import Questionnaire
import app
from datetime import datetime
from sqlalchemy import text

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('id', help='참여자 ID(pk)', type=int, required=True)
# parser.add_argument('tab_num', help='문진표 Type(Tab 번호) [ 1:종합검진 / 2:영양 생활습관 / 3: 인지기능 / 4: 정신건강 / 5: 스트레스 / 6: 위장건강 / 7: 수면장애 / 8: 피로도 / 9: 삼킴 ]', required=True, default=1)
parser.add_argument('tab_num', help='문진표 Type(Tab 번호) [ 1:종합검진 / 2:영양 생활습관, 인지기능, 정신건강, 스트레스, 위장건강, 수면장애, 피로도, 삼킴 ]', required=True, default=1)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'

SELECT_COMMON_SQL = 'SELECT * FROM common_question CQ LEFT OUTER JOIN (SELECT id, agree_name FROM agree) A ON A.id = CQ.agree_id WHERE agree_id=:id AND question_type_id=:tab_num'
SELECT_NUTRITION_SQL = 'SELECT * FROM nutrition_question NQ LEFT OUTER JOIN (SELECT id, agree_name FROM agree) A ON A.id = NQ.agree_id WHERE agree_id=:id AND question_type_id=:tab_num'
SELECT_COGNITIVE_SQL = 'SELECT * FROM cognitive_question CQ LEFT OUTER JOIN (SELECT id, agree_name FROM agree) A ON A.id = CQ.agree_id WHERE agree_id=:id AND question_type_id=:tab_num'
SELECT_MENTAL_SQL = 'SELECT * FROM mental_question MQ LEFT OUTER JOIN (SELECT id, agree_name FROM agree) A ON A.id = MQ.agree_id WHERE agree_id=:id AND question_type_id=:tab_num'
SELECT_STRESS_SQL = 'SELECT * FROM stress_question SQ LEFT OUTER JOIN (SELECT id, agree_name FROM agree) A ON A.id = SQ.agree_id WHERE agree_id=:id AND question_type_id=:tab_num'
SELECT_STOMACH_SQL = 'SELECT * FROM stomach_question SQ LEFT OUTER JOIN (SELECT id, agree_name FROM agree) A ON A.id = SQ.agree_id WHERE agree_id=:id AND question_type_id=:tab_num'
SELECT_SLEEP_SQL = 'SELECT * FROM sleep_question SQ LEFT OUTER JOIN (SELECT id, agree_name FROM agree) A ON A.id = SQ.agree_id WHERE agree_id=:id AND question_type_id=:tab_num'
SELECT_FATIGUE_SQL = 'SELECT * FROM fatigue_question FQ LEFT OUTER JOIN (SELECT id, agree_name FROM agree) A ON A.id = FQ.agree_id WHERE agree_id=:id AND question_type_id=:tab_num'
SELECT_SAMKIM_SQL = 'SELECT * FROM samkim_question SQ LEFT OUTER JOIN (SELECT id, agree_name FROM agree) A ON A.id = SQ.agree_id WHERE agree_id=:id AND question_type_id=:tab_num'

@Questionnaire.route('/detail')
class Detail(Resource):
    @Questionnaire.expect(parser)
    @Questionnaire.response(200, 'Success')
    @Questionnaire.response(401, 'Unauthorized')
    @Questionnaire.response(500, 'Internal Server Error')
    def get(self):
        """문진표 상세 API"""
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
        q['id'] = args['id']
        q['tab_num'] = args['tab_num']
        
        if q['tab_num'] == '1':
            row = app.db2.execute(text(SELECT_COMMON_SQL), q).fetchall()
        elif q['tab_num'] == '2':
            wq = dict()
            wq['id'] = args['id']
            wq['tab_num'] = '1'
            row1 = app.db2.execute(text(SELECT_COMMON_SQL), wq).fetchall()
            row2 = app.db2.execute(text(SELECT_NUTRITION_SQL), q).fetchall()
            row3 = app.db2.execute(text(SELECT_COGNITIVE_SQL), q).fetchall()
            row4 = app.db2.execute(text(SELECT_MENTAL_SQL), q).fetchall()
            row5 = app.db2.execute(text(SELECT_STRESS_SQL), q).fetchall()
            row6 = app.db2.execute(text(SELECT_STOMACH_SQL), q).fetchall()
            row7 = app.db2.execute(text(SELECT_SLEEP_SQL), q).fetchall()
            row8 = app.db2.execute(text(SELECT_FATIGUE_SQL), q).fetchall()
            row9 = app.db2.execute(text(SELECT_SAMKIM_SQL), q).fetchall()

        response = {}
        resp = {}
        if q['tab_num'] == '1' or q['tab_num'] == 1:
            if len(row) == 0:
                response = '미작성 상태 입니다.'
            else:
                resp['agree_name'] = row[0]['agree_name']
                resp['createDate'] = row[1:][0]['create_date'].strftime('%Y-%m-%d %H:%M:%S')

                answer_list = []
                for idx in range(len(row)):
                    resp_answer = {}
                    if row[idx]['category_id'] != '4' or row[idx]['category_id'] != 4:
                        resp_answer['answer_text'] = row[idx]['answer_text']
                        resp_answer['answer'] = row[idx]['answer']
                        answer_list.append(resp_answer)
                        resp['answer_list'] = answer_list

                response = resp
        
        if q['tab_num'] == '2' or q['tab_num'] == 2:
            resp = []

            # 신체활동(운동) | 고강도/중강도
            r1 = {}
            if len(row1) == 0:
                r1['result'] = '미작성'
            else:
                r1['sum'] = row1[-1:][0]['answer']
                r1['createDate'] = row1[-1:][0]['create_date'].strftime('%Y-%m-%d %H:%M:%S')
                if int(row1[-1:][0]['answer']) <= 140:
                    r1['result'] = '부족'
                elif 150 <= int(row1[-1:][0]['answer']) <= 299:
                    r1['result'] = '충분하지 않음'
                elif int(row1[-1:][0]['answer']) >= 300:
                    r1['result'] = '충분'
            resp.append(r1)

            # 신체활동(운동) | 근력운동
            r2 = {}
            if len(row1) == 0:
                r2['result'] = '미작성'
            else:
                r2['sum'] = row1[-2:][0]['answer']
                r2['createDate'] = row1[-2:][0]['create_date'].strftime('%Y-%m-%d %H:%M:%S')
                if int(row1[-2:][0]['answer']) == 0 or int(row1[-2:][0]['answer']) == 1:
                    r2['result'] = '근력운동'
                elif 2 <= int(row1[-2:][0]['answer']) <= 7:
                    r2['result'] = '-'
                else:
                    r2['result'] = '--'
            resp.append(r2)

            # 영양 생활습관
            r3 = {}
            if len(row2) == 0:
                r3['result'] = '미작성'
            else:
                r3['sum'] = row2[-1:][0]['answer']
                r3['createDate'] = row2[-1:][0]['create_date'].strftime('%Y-%m-%d %H:%M:%S')
                if int(row2[-1:][0]['answer']) <= 27:
                    r3['result'] = '개선'
                elif 28 < int(row2[-1:][0]['answer']) <= 38:
                    r3['result'] = '보통'
                elif int(row2[-1:][0]['answer']) >= 39:
                    r3['result'] = '양호'
            resp.append(r3)

            # 인지기능
            r4 = {}
            if len(row3) == 0:
                r4['result'] = '미작성'
            else:
                r4['sum'] = row3[-1:][0]['answer']
                r4['createDate'] = row3[-1:][0]['create_date'].strftime('%Y-%m-%d %H:%M:%S')
                if int(row3[-1:][0]['answer']) <= 5:
                    r4['result'] = '정상'
                elif int(row3[-1:][0]['answer']) >= 6:
                    r4['result'] = '인지기능 저하'
            resp.append(r4)

            # 정신건강
            r5 = {}
            if len(row4) == 0:
                r5['result'] = '미작성'
            else:
                r5['sum'] = row4[-1:][0]['answer']
                r5['createDate'] = row4[-1:][0]['create_date'].strftime('%Y-%m-%d %H:%M:%S')
                if int(row4[-1:][0]['answer']) <= 4:
                    r5['result'] = '정상'
                elif 5 <= int(row4[-1:][0]['answer']) <= 9:
                    r5['result'] = '가벼운'
                elif 10 <= int(row4[-1:][0]['answer']) <= 19:
                    r5['result'] = '중간정도'
                elif int(row4[-1:][0]['answer']) >= 20:
                    r5['result'] = '심한'
            resp.append(r5)

            # 스트레스
            r6 = {}
            if len(row5) == 0:
                r6['result'] = '미작성'
            else:
                r6['sum'] = row5[-1:][0]['answer']
                r6['createDate'] = row5[-1:][0]['create_date'].strftime('%Y-%m-%d %H:%M:%S')
                r6['result'] = '-'
            resp.append(r6)

            # 위장건강
            r7 = {}
            if len(row6) == 0:
                r7['result'] = '미작성'
            else:
                r7['sum'] = row6[-1:][0]['answer']
                r7['createDate'] = row6[-1:][0]['create_date'].strftime('%Y-%m-%d %H:%M:%S')
                if int(row6[-1:][0]['answer']) <= 9:
                    r7['result'] = '위장문제 없음'
                elif 10 <= int(row6[-1:][0]['answer']) <= 19:
                    r7['result'] = '최소한의 위장문제'
                elif 20 <= int(row6[-1:][0]['answer']) <= 29:
                    r7['result'] = '보통의 위장문제'
                elif 30 <= int(row6[-1:][0]['answer']) <= 39:
                    r7['result'] = '보통의 심각한 위장문제'
                elif 40 <= int(row6[-1:][0]['answer']) <= 45:
                    r7['result'] = '심각한 위장문제'
            resp.append(r7)

            # 수면장애
            r8 = {}
            if len(row7) == 0:
                r8['result'] = '미작성'
            else:
                r8['sum'] = row7[-1:][0]['answer']
                r8['createDate'] = row7[-1:][0]['create_date'].strftime('%Y-%m-%d %H:%M:%S')
                r8['result'] = '-'
            resp.append(r8)

            # 피로도
            r9 = {}
            if len(row8) == 0:
                r9['result'] = '미작성'
            else:
                r9['sum'] = row8[-1:][0]['answer']
                r9['createDate'] = row8[-1:][0]['create_date'].strftime('%Y-%m-%d %H:%M:%S')
                if int(row8[-1:][0]['answer']) == 0:
                    r9['result'] = '-'
                elif 1 <= int(row8[-1:][0]['answer']) <= 3:
                    r9['result'] = '피로1-Mild'
                elif int(row8[-1:][0]['answer']) == 4:
                    r9['result'] = '피로2-Moderate'
                elif int(row8[-1:][0]['answer']) >= 5:
                    r9['result'] = '피로3-Serve'
            resp.append(r9)

            # 삼킴
            if row9 != None or row9 != 0:
                r10 = {}
                if len(row9) == 0:
                    r10['result'] = '미작성'
                else:
                    r10['sum'] = row9[-1:][0]['answer']
                    r10['createDate'] = row9[-1:][0]['create_date'].strftime('%Y-%m-%d %H:%M:%S')
                    r10['result'] = '-'
                resp.append(r10)

            if len(row1) != 0:
                response['admin_name'] = row1[0]['agree_name']
            elif len(row2) != 0:
                response['admin_name'] = row2[0]['agree_name']
            elif len(row3) != 0:
                response['admin_name'] = row3[0]['agree_name']
            elif len(row4) != 0:
                response['admin_name'] = row4[0]['agree_name']
            elif len(row5) != 0:
                response['admin_name'] = row5[0]['agree_name']
            elif len(row6) != 0:
                response['admin_name'] = row6[0]['agree_name']
            elif len(row7) != 0:
                response['admin_name'] = row7[0]['agree_name']
            elif len(row8) != 0:
                response['admin_name'] = row8[0]['agree_name']
            elif len(row9) != 0:
                response['admin_name'] = row9[0]['agree_name']
            else:
                return {
                    'code': 'failed',
                    'message': 'failed',
                    'reponse': '작성된 문진이 없습니다.'
                }
            response['result'] = resp

        return {
            'code': 'success',
            'message': 'success',
            'response': response
        }, 200
