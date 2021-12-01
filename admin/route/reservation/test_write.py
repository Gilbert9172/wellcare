from os import close
from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .reservation import Reservation
from sqlalchemy import text

import app

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰',location='headers', required=True)
parser.add_argument('user_name', help='이름', location='json', required=True)
parser.add_argument('user_birth', help='생년월일', location='json', required=True)
parser.add_argument('user_gender', help='성별', location='json', required=True)
parser.add_argument('user_phone', help='휴대폰번호', location='json', required=True)
parser.add_argument('resv_date', help='예약일시', location='json', required=True)
parser.add_argument('resv_time', help='예약시간', location='json', required=True)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'

USER_INSERT_SQL = 'INSERT INTO user(user_name, user_birth, user_gender, user_phone)'\
    'VALUES(:user_name, :user_birth, :user_gender, :user_phone)'
RESV_INSERT_SQL = 'INSERT INTO resv_consultation(resv_date, resv_time, user_id, clinical_trial_type, resv_flag)'\
    ' VALUES(:resv_date, :resv_time, (SELECT id FROM user WHERE user_phone=:user_phone ORDER BY id DESC LIMIT 1), (SELECT id FROM clinical_trial ORDER BY create_date DESC LIMIT 1), :resv_flag)'

PHONE_NUM_CHECK_SQL = 'SELECT * FROM user WHERE user_phone=:user_phone ORDER BY user_phone DESC LIMIT 1'
NAME_CHECK_SQL = 'SELECT * FROM user WHERE user_name=:user_name ORDER BY user_name DESC LIMIT 1'
BIRTH_CHECK_SQL = 'SELECT * FROM user WHERE user_birth=:user_birth ORDER BY user_birth DESC LIMIT 1'


@Reservation.route('/test_write')
class Test_Write(Resource):
    @Reservation.expect(parser)
    @Reservation.response(200, 'Success')
    @Reservation.response(500, 'Internal Server Error')
    def post(self):
        """테스트 예약추가하기 API"""
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
        wq['resv_flag'] = 2

        try:
            row_id = app.db.execute(text(USER_INSERT_SQL), q).lastrowid
            row_id2 = app.db.execute(text(RESV_INSERT_SQL), wq).lastrowid

            # 예약번호 '0' 붙여서 6자리로 만들기 처리
            if row_id2 < 10:
                row_id2 = '00000' + str(row_id2)
            elif row_id2 >= 10:
                row_id2 = '0000' + str(row_id2)
            elif row_id2 >= 100:
                row_id2 = '000' + str(row_id2)
            elif row_id2 >= 1000:
                row_id2 = '00' + str(row_id2)
            elif row_id2 >= 10000:
                row_id2 = '0' + str(row_id2)
            elif row_id2 >= 100000:
                row_id2 = row_id2
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
