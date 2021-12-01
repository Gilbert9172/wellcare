from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .reservation import Reservation
from sqlalchemy import text

import app

parser = reqparse.RequestParser()
parser.add_argument('id', help='예약번호', location='json', type=int, required=True)
parser.add_argument('resv_cancel_note', help='예약취소사유', location='json', required=True)

RESV_DELETE_SQL = 'UPDATE resv_consultation SET resv_cancel_note=:resv_cancel_note, resv_flag=1 WHERE id=:id'

RESV_FLAG_CHECK_SQL = 'SELECT resv_flag FROM resv_consultation WHERE id=:id'

SELECT_RESV_ID_LIST_SQL = 'SELECT id FROM resv_consultation'

@Reservation.route('/cancel')
class cancel(Resource):
    @Reservation.expect(parser)
    @Reservation.response(200, 'Success')
    @Reservation.response(500, 'Internal Server Error')
    def put(self):
        """예약 취소하기 API"""
        args = parser.parse_args()

        # 없는 예약번호 체크.
        row_list = app.db.execute(text(SELECT_RESV_ID_LIST_SQL)).fetchall()

        res = [x[0] for x in row_list]

        if int(args['id']) not in res:
            return {
                'code': 'fail',
                'message': '없는 예약번호입니다.',
                'response': {
                    'flag': False
                }
            }, 500

        # 예약취소FLAG 체크
        wq = {}
        wq['id'] = args['id']

        row = app.db.execute(text(RESV_FLAG_CHECK_SQL), wq).fetchone()

        if row != None:
            if row[0] == 1:
                return {
                    'code': 'fail',
                    'message': '이미 취소된 예약번호입니다.',
                    'response': {
                        'flag': False
                    }
                }, 500

        # 예약 번호 확인

        q = {}
        q['id'] = args['id']
        q['resv_cancel_note'] = args['resv_cancel_note']

        try:
            row_id = app.db.execute(text(RESV_DELETE_SQL), q).lastrowid
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
                'result': '예약이 취소 되었습니다.'
            }
        }, 200
