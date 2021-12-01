from os import close
from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .reservation import Reservation
from sqlalchemy import text

from datetime import datetime
import calendar
import app
import requests
import json

parser = reqparse.RequestParser()
# parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('user_name', help='이름', location='json', required=True)
parser.add_argument('user_birth', help='생년월일', location='json', required=True)
parser.add_argument('user_gender', help='성별', location='json', required=True)
parser.add_argument('user_phone', help='휴대폰번호', location='json', required=True)
parser.add_argument('resv_date', help='예약일시', location='json', required=True)
parser.add_argument('resv_time', help='예약시간', location='json', required=True)

USER_INSERT_SQL = 'INSERT INTO user(user_name, user_birth, user_gender, user_phone)'\
                    'VALUES(:user_name, :user_birth, :user_gender, :user_phone)'
RESV_INSERT_SQL = 'INSERT INTO resv_consultation(resv_date, resv_time, user_id, clinical_trial_type, resv_flag)'\
                    ' VALUES(:resv_date, :resv_time, (SELECT id FROM user WHERE user_phone=:user_phone ORDER BY id DESC LIMIT 1), (SELECT id FROM clinical_trial ORDER BY create_date DESC LIMIT 1), :resv_flag)'

RESV_TYPE_CHECK_SQL = 'SELECT RC.clinical_trial_type FROM resv_consultation AS RC, user AS U'\
                     ' WHERE (SELECT user_phone FROM user WHERE user_name=:user_name AND user_birth=:user_birth ORDER BY user_phone DESC LIMIT 1)=:user_phone ORDER BY RC.clinical_trial_type DESC LIMIT 1'

CLINICAL_TRIAL_TYPE_CHECK_SQL = 'SELECT id FROM clinical_trial ORDER BY create_date DESC LIMIT 1'
RESV_FLAG_CHECK_SQL = 'SELECT resv_flag FROM resv_consultation WHERE user_id=:user_id ORDER BY create_date DESC LIMIT 1'
USER_ID_SQL = 'SELECT id FROM user WHERE user_phone=:user_phone ORDER BY create_date DESC LIMIT 1'
PHONE_NUM_CHECK_SQL = 'SELECT * FROM user WHERE user_phone=:user_phone ORDER BY user_phone DESC LIMIT 1'
NAME_CHECK_SQL = 'SELECT * FROM user WHERE user_name=:user_name ORDER BY user_name DESC LIMIT 1'
BIRTH_CHECK_SQL = 'SELECT * FROM user WHERE user_birth=:user_birth ORDER BY user_birth DESC LIMIT 1'

@Reservation.route('/write')
class Write(Resource):
    @Reservation.expect(parser) 
    @Reservation.response(200, 'Success')
    @Reservation.response(500, 'Internal Server Error')
    def post(self):
        """비회원 예약하기 API"""
        args = parser.parse_args()

        # 임상연구에 따른 재예약 확인
        eq = {}
        eq['user_phone'] = args['user_phone']
        eq['user_name'] = args['user_name']
        eq['user_birth'] = args['user_birth']

        sq = {}
        sq['user_phone'] = args['user_phone']

        row = app.db.execute(text(RESV_TYPE_CHECK_SQL), eq).fetchone()
        row2 = app.db.execute(text(CLINICAL_TRIAL_TYPE_CHECK_SQL)).fetchone()
        row3 = app.db.execute(text(PHONE_NUM_CHECK_SQL),sq).fetchone()
        row4 = app.db.execute(text(USER_ID_SQL),sq).fetchone()

        if row4 != None:
            wq = {}
            wq['user_id'] = row4['id']

            row5 = app.db.execute(text(RESV_FLAG_CHECK_SQL), wq).fetchone()

            if row != None and row2 != None and row5 != None:
                if row5['resv_flag'] != 1 and row5['resv_flag'] != 3:
                    if row[0] == row2[0]:
                        return {
                            'code': 'fail',
                            'message': '이미 예약이 완료 됐습니다.',
                            'response': {}
                        }, 500


            # 휴대폰번호는 같은데, 회원 이름이나 생년월일이 다를 경우 예외처리

            if row3 != None and row5 != None:
                if row5['resv_flag'] != 1 and row5['resv_flag'] != 3:
                    if row3['user_name'] != args['user_name'] and row3['user_birth'] != args['user_birth']:
                        return {
                            'code': 'fail',
                            'message': '이미 예약된 휴대폰번호 입니다.',
                            'response':{}
                        }, 500

        # 예약하기  
        q = {}
        q['user_name'] = args['user_name']
        q['user_birth'] = args['user_birth']
        q['user_gender'] = args['user_gender']
        q['user_phone'] = args['user_phone']
        
        wq = {}
        wq['resv_date'] = args['resv_date']
        wq['resv_time'] = args['resv_time']
        wq['user_phone'] = args['user_phone']
        wq['resv_flag'] = 0
        
        try:
            row_id = app.db.execute(text(USER_INSERT_SQL), q).lastrowid
            row_id2 = app.db.execute(text(RESV_INSERT_SQL), wq).lastrowid

            # 예약번호 '0' 붙여서 6자리로 만들기 처리
            if row_id2 < 10:
                row_id2 = '00000' + str(row_id2)
            elif 100 > row_id2 >= 10:
                row_id2 = '0000' + str(row_id2)
            elif 1000 > row_id2 >= 100:
                row_id2 = '000' + str(row_id2)
            elif 10000 > row_id2 >= 1000:
                row_id2 = '00' + str(row_id2)
            elif 100000 > row_id2 >= 10000:
                row_id2 = '0' + str(row_id2)
            elif row_id2 >= 100000:
                row_id2 = row_id2

            curr_date = datetime.strptime(wq['resv_date'], "%Y-%m-%d")
            date = calendar.day_name[curr_date.weekday()]

            if date == 'Monday':
                date = '(월)'
            elif date == 'Tuesday':
                date = '(화)'
            elif date == 'Wednesday':
                date = '(수)'
            elif date == 'Thursday':
                date = '(목)'   
            elif date == 'Friday':
                date = '(금)'
            elif date == 'Saturday':
                date = '(토)'
            elif date == 'Sunday':
                date ='(일)'

            # 알리고 문자 보내기 기능 ========================================================================================

            send_url = 'https://apis.aligo.in/send/' # 요청을 던지는 URL, 현재는 문자보내기
            # ================================================================== 문자 보낼 때 필수 key값
            # API key, userid, sender, receiver, msg
            # API키, 알리고 사이트 아이디, 발신번호, 수신번호, 문자내용

            sms_data={'key': 'bfw3vrqjeitg5s6la3wuyxlu2197gxxx', #api key
                    'userid': 'fineinsight', # 알리고 사이트 아이디
                    'sender': '01059166362', # 발신번호
                    'receiver': q['user_phone'], # 수신번호 (,활용하여 1000명까지 추가 가능)
                    'msg': '[웰케어] 예약완료\n\n'
                            '예약정보를 확인해주세요.\n'
                            '\n예약번호: ' + row_id2 +
                            '\n이름: ' + q['user_name']+
                            '\n휴대폰번호: ' + q['user_phone']+
                            '\n생년월일: ' + q['user_birth']+
                            '\n성별: ' + q['user_gender']+ 
                            '\n참여연구명: 웰케어 데이터 수집을 위한 임상 코호트 구축'
                            '\n예약일시: ' + wq['resv_date'] + ' ' + date + ', ' + wq['resv_time'] +
                            '\n\n※ 1층 원무 접수(웰케어 연구 참여 접수) → 6층 데이터 융합센터 방문'
                            '\n※ 본 연구는 총 2회 방문으로 참여하셔야 가능합니다.'
                            '\n- 1회차 금식 없는 검사 / 2회차 금식 상태로 혈액, 소변검사 위주'
                            '\n- 각 방문 시마다 1시간 이상 검사 시간 소요됩니다.'
                            '\n\n※ 주소: 강남메이저의원(서울특별시 강남구 대치동 도곡로 452) 6층 EDGC 데이터 융합연구소'
                            '\n※ 주차 공간 협소로 대중교통 이용 바랍니다. 주차비 발생됩니다.'
                            '\n※ 연구 문의: 예약 홈페이지 내 문의하기를 이용해 주세요. 전화 통화는 어렵습니다.',  # 문자 내용
                    'msg_type' : 'LMS', #메세지 타입 (SMS, LMS)
                    'title' : '[월케어] 예약완료', #메세지 제목 (장문에 적용)
                    # 'destination' : '01000000000|홍길동', # %고객명% 치환용 입력
                    # 'rdate' : '예약날짜',
                    # 'rtime' : '예약시간',
                    #'testmode_yn' : '' #테스트모드 적용 여부 Y/N
            }
            send_response = requests.post(send_url, data=sms_data)

            # =================================================================================================================================
            
          
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
                'user_name': q['user_name'],
                'user_birth': q['user_birth'],
                'user_gender': q['user_gender'],
                'user_phone': q['user_phone'],
                'resv_num': row_id2,
                'resv_date': wq['resv_date'],
                'resv_time': wq['resv_time'],
                'resv_flag': wq['resv_flag']
            }
        }, 200
