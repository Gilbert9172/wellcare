from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .reservation import Reservation
import app

from datetime import datetime
from sqlalchemy import text


parser = reqparse.RequestParser()
parser.add_argument('user_name', help='이름', location='json', required=True)
parser.add_argument('id', help='예약번호', location='json', type=int, required=True)

RESERVATION_SELECT_SQL = 'SELECT * FROM resv_consultation WHERE id=:id'
USER_SELECT_SQL = 'SELECT * FROM user WHERE user_name=:user_name AND id=(SELECT user_id FROM resv_consultation WHERE id=:id)'


@Reservation.route('/info')
class Info(Resource):
    @Reservation.expect(parser)
    @Reservation.response(200, 'Success')
    @Reservation.response(500, 'Failed')
    def post(self):
        """예약정보 조회 API"""
        args = parser.parse_args()
        

        q = {}
        q['id'] = args['id']


        row = app.db.execute(text(RESERVATION_SELECT_SQL), q).fetchone()
        
        wq = {}
        wq['user_name'] = args['user_name']
        wq['id'] = args['id']

        row2 = app.db.execute(text(USER_SELECT_SQL), wq).fetchone()


        if row == None:
            return {
                'code': 'fail',
                'message': '예약된 내역이 없습니다.',
                'response': {}
            }, 200

   
            
        # 디데이 계산
        thisDay = datetime.today()
        resvDate = datetime.strptime(str(row['resv_date']), "%Y-%m-%d")
        currentDay = resvDate - thisDay
        if currentDay.days + 1 > 0:    
            dDay = currentDay.days + 1
        elif currentDay.days + 1 == 0:
            dDay = 0
        else:
            dDay = -1

        # 예약번호 '0' 붙여서 6자리로 만들기 처리
        if row['id'] < 10:
            resv_id = '00000' + str(row['id'])
        elif 100 > row['id'] >= 10:
            resv_id = '0000' + str(row['id'])
        elif  1000 >row['id'] >= 100:
            resv_id = '000' + str(row['id'])
        elif 10000 > row['id'] >= 1000:
            resv_id = '00' + str(row['id'])
        elif 100000 > row['id'] >= 10000:
            resv_id = '0' + str(row['id'])
        elif row['id'] >= 100000:
            resv_id = str(row['id'])
        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'user_name': row2['user_name'],
                'user_phone': row2['user_phone'],
                'user_gender': row2['user_gender'],
                'user_birth': row2['user_birth'],
                'id': resv_id,
                'resv_date': str(row['resv_date']),
                'resv_time': str(row['resv_time']),
                'resv_flag': row['resv_flag'],
                'd_day': dDay,
            }
        }, 200
