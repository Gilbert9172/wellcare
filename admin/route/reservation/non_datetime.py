from os import close
from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .reservation import Reservation
from sqlalchemy import text

import app

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('date', help='날짜', location='json', required=True)
parser.add_argument('time', help='시간', location='json', required=True)
parser.add_argument('author', help='관리자', location='json', required=True)


TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'
NON_DATETIME_INSERT = 'INSERT INTO resv_non_datetime(date,time,author) VALUES(:date, :time,:author)'
NON_DATETIME_CHECK = 'SELECT * FROM resv_non_datetime WHERE date=:date AND time=:time'


@Reservation.route('/non_datetime')
class Nondatetime(Resource):
    @Reservation.expect(parser)
    @Reservation.response(200, 'Success')
    @Reservation.response(500, 'Failed')
    def post(self):
        """예약 불가 날짜시간 작성 API"""
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


        wq = {}
        wq['date'] = args['date']
        wq['time'] = args['time']
        row2 = app.db.execute(text(NON_DATETIME_CHECK), wq).fetchone()

        if row2 != None:
            row2.date == args['date'] or row2.time == args['time']
            return{
                'code' : 'fail',
                'message' : '이미 등록된 시간 날짜 입니다',
                'response' : {}
            },500
       

        q={}
        q['date'] = args['date']
        q['time'] = args['time']
        q['author'] = args['author']
        row = app.db.execute(text(NON_DATETIME_INSERT), q).lastrowid
    
        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'date' : q['date'],
                'time' : q['time'],
                'author' : q['author']
            }
        }, 200
