from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .reservation import Reservation
import app
from sqlalchemy import text

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('user_name', help='이름', location='json', required=True)
parser.add_argument('id', help='예약번호', location='json', type=int, required=True)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'

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
            
        
           
        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'user_name': row2['user_name'],
                'user_phone': row2['user_phone'],
                'user_birth': row2['user_birth'],
                'id': row['id'],
                'resv_date': str(row['resv_date']),
                'resv_time': str(row['resv_time'])
            }
        }, 200
