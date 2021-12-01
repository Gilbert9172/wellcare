from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .reservation import Reservation
import app
from sqlalchemy import text

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('user_name', help='참여자 이름', location='json', required=True)
parser.add_argument('user_phone', help='참여자 휴대폰번호', location='json', required=True)

TOKEN_CHECK_SQL = 'SELECT AT.* FROM admin_account_token AS AT, admin_account AS A WHERE AT.token=:token AND AT.aid = A.id'
SELECT_USER_ID_SQL = 'SELECT id FROM user WHERE user_name=:user_name AND user_phone=:user_phone'
DELETE_RESERVATION_SQL = 'DELETE FROM resv_consultation WHERE user_id=:id'
DELETE_USER_SQL = 'DELETE FROM user WHERE id=:id'

@Reservation.route('/delete')
class Delete(Resource):
    @Reservation.expect(parser)
    @Reservation.response(200, 'Success')
    @Reservation.response(401, 'Unauthorized')
    @Reservation.response(500, 'Internal Server Error')
    def delete(self):
        """예약 삭제하기 API"""
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
        q['user_name'] = args['user_name']
        q['user_phone'] = args['user_phone']
        row_id = app.db.execute(text(SELECT_USER_ID_SQL),q).fetchone()
        try:
            wq = {}
            wq['id'] = row_id['id']
            app.db.execute(text(DELETE_RESERVATION_SQL),wq)
            app.db.execute(text(DELETE_USER_SQL),wq)
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
            'code':'success',
            'message':'succes',
            'response': {
                'flag' : True
            }
        }
