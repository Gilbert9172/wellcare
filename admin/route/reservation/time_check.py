from os import close
from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .reservation import Reservation
from sqlalchemy import text

import app

parser = reqparse.RequestParser()
parser.add_argument('resv_date', help='날짜', location='json', required=True)
# parser.add_argument('resv_time', help='시간', location='json', required=True)

CONSULTATION_CHECK = 'SELECT li.hour,li.limit FROM resv_consultation_limit as li '
CONSULTATION_TIME_CHECK = 'SELECT C.resv_date, C.resv_time, C.resv_flag FROM resv_consultation AS C WHERE (C.resv_flag = 0 OR C.resv_flag = 2 OR C.resv_flag = 4) AND C.resv_date=:resv_date'


@Reservation.route('/check')
class Check(Resource):
    @Reservation.expect(parser)
    @Reservation.response(200, 'Success')
    @Reservation.response(500, 'Failed')
    def post(self):
        """예약 가능 시간 확인 API"""
        args = parser.parse_args()
        is_possible = False
        time_list = list()

        q = {}
        q['resv_date'] = args['resv_date']
        rows = app.db.execute(text(CONSULTATION_TIME_CHECK), q).fetchall()
        row = app.db.execute(text(CONSULTATION_CHECK)).fetchall()
        time1, time2, time3, time4, time5, time6, time7, time8 = 0, 0, 0, 0, 0, 0, 0, 0
        for r in rows:
            if r['resv_time'] == '08:00':
                time1 += 1
            if r['resv_time'] == '09:00':
                time2 += 1
            if r['resv_time'] == '10:00':
                time3 += 1
            if r['resv_time'] == '11:00':
                time4 += 1
            if r['resv_time'] == '13:00':
                time5 += 1
            if r['resv_time'] == '14:00':
                time6 += 1
            if r['resv_time'] == '15:00':
                time7 += 1
            if r['resv_time'] == '16:00':
                time8 += 1

        for t in row:
            time_list.append({
                'time': t['hour'],
                'isPossible': is_possible
            })
            if t['hour'] == '08:00':
                if time1 < t['limit']:
                    time_list[0]['isPossible'] = True
            if t['hour'] == '09:00':
                if time2 < t['limit']:
                    time_list[1]['isPossible'] = True
            if t['hour'] == '10:00':
                if time3 < t['limit']:
                    time_list[2]['isPossible'] = True
            if t['hour'] == '11:00':
                if time4 < t['limit']:
                    time_list[3]['isPossible'] = True
            if t['hour'] == '13:00':
                if time5 < t['limit']:
                    time_list[4]['isPossible'] = True
            if t['hour'] == '14:00':
                if time6 < t['limit']:
                    time_list[5]['isPossible'] = True
            if t['hour'] == '15:00':
                if time7 < t['limit']:
                    time_list[6]['isPossible'] = True
            if t['hour'] == '16:00':
                if time8 < t['limit']:
                    time_list[7]['isPossible'] = True
        
        # time1, time2, time3, time4, time5, time6, time7 = 0, 0, 0, 0, 0, 0, 0
        # for r in rows:
        #     if r['resv_time'] == '08:00':
        #         time1 += 1
        #     if r['resv_time'] == '09:00':
        #         time2 += 1
        #     if r['resv_time'] == '10:00':
        #         time3 += 1
        #     if r['resv_time'] == '11:00':
        #         time4 += 1
        #     if r['resv_time'] == '14:00':
        #         time5 += 1
        #     if r['resv_time'] == '15:00':
        #         time6 += 1
        #     if r['resv_time'] == '16:00':
        #         time7 += 1

        # for t in row:
        #     time_list.append({
        #         'time': t['hour'],
        #         'isPossible': is_possible
        #     })
        #     if t['hour'] == '08:00':
        #         if time1 < t['limit']:
        #             time_list[0]['isPossible'] = True
        #     if t['hour'] == '09:00':
        #         if time2 < t['limit']:
        #             time_list[1]['isPossible'] = True
        #     if t['hour'] == '10:00':
        #         if time3 < t['limit']:
        #             time_list[2]['isPossible'] = True
        #     if t['hour'] == '11:00':
        #         if time4 < t['limit']:
        #             time_list[3]['isPossible'] = True
        #     if t['hour'] == '14:00':
        #         if time5 < t['limit']:
        #             time_list[4]['isPossible'] = True
        #     if t['hour'] == '15:00':
        #         if time6 < t['limit']:
        #             time_list[5]['isPossible'] = True
        #     if t['hour'] == '16:00':
        #         if time7 < t['limit']:
        #             time_list[6]['isPossible'] = True

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'list': time_list
            }
        }, 200
