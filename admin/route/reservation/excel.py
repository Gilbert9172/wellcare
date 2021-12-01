from flask import request
from flask_restx import Resource, reqparse
from flask import send_from_directory
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null
from .reservation import Reservation
import app
from sqlalchemy import text
from datetime import datetime
import time
from openpyxl.styles import Alignment
import pandas as pd



parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('start', help='시작 index', type=int, required=True, default=0)
parser.add_argument('size', help='페이지 수', type=int, required=True, default=10)
parser.add_argument('startdate', help='예약일자 시작', required=False)
parser.add_argument('enddate', help='예약일자 끝', required=False)
parser.add_argument('q', help='검색(이름, 휴대폰번호, 생년월일)', required=False)
parser.add_argument('gender', help='성별(전체(0), 남성(1), 여성(2)', type=int, required=True, default=0)
parser.add_argument('status', help='상태(전체(0), 예약 완료(1), 예약 취소(2), 관리자 추가(3), 관리자 취소(4), 관리자 예약 변경(5), 등록 완료(6), 수집 완료(7)', type=int, required=True, default=0)
parser.add_argument('sort', help='없음(0), 예약일(1), 생년월일(2), 상태(3)', type=int, required=True, default=0)
parser.add_argument('order', help='내림차순(0), 오름차순(1)', type=int, required=True, default=0)
parser.add_argument('timestamp', help='timestamp', type=int, required=True)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'

# SQL문 HEAD
RESERVATION_COUNT_SQL = 'SELECT count(*) as cnt '
RESV_SELECT_SQL = 'SELECT RC.resv_date, RC.resv_time, U.user_name, U.user_phone, U.user_birth, U.user_gender, RC.resv_flag,U.user_memo, RC.resv_cancel_note, RC.modified_date, RC.create_date, RC.id '

# SQL문 BODY
RESV_SELECT_BODY = 'FROM resv_consultation RC '\
    'LEFT OUTER JOIN (SELECT * FROM user) U ON U.id=RC.user_id '\
    'WHERE 1 '

# SQL문 조건
MIN_DATE_SQL = 'AND RC.resv_date >= str_to_date(:startdate, \'%Y-%m-%d\') '
MAX_DATE_SQL = 'AND RC.resv_date <= str_to_date(:enddate, \'%Y-%m-%d %H:%i:%s\') '
USER_Q_SQL = 'AND (U.user_name LIKE :q1 or U.user_phone LIKE :q1 or U.user_birth LIKE :q1) '
GENDER_SQL = 'AND user_gender=:user_gender '
STATUS_SQL = 'AND resv_flag=:resv_flag '
LIMIT_SQL = 'LIMIT :start, :size '


@Reservation.route('/excel')
class Excel(Resource):
    @Reservation.expect(parser)
    @Reservation.response(200, 'Success')
    @Reservation.response(401, 'Unauthorized')
    @Reservation.response(500, 'Internal Server Error')
    def get(self):
        """예약 엑셀 API"""
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
        sql_body = RESV_SELECT_BODY
        q['start'] = args['start']
        q['size'] = args['size']
        if args['startdate'] != None:
            q['startdate'] = args['startdate']
            sql_body += MIN_DATE_SQL
        if args['enddate'] != None:
            q['enddate'] = args['enddate'] + ' 23:59:59'
            sql_body += MAX_DATE_SQL
        if args['q'] != None:
            q['q1'] = '%' + args['q'] + '%'
            sql_body += USER_Q_SQL
        if args['gender'] == 1:
            q['user_gender'] = '남성'
            sql_body += GENDER_SQL
        elif args['gender'] == 2:
            q['user_gender'] = '여성'
            sql_body += GENDER_SQL
        else:
            if args['gender'] != 0:
                return {
                    'code': 'fail',
                    'message': '잘못된 gender 값입니다'
                }, 500
        if args['status'] == 1:
            q['resv_flag'] = 0
            sql_body += STATUS_SQL
        elif args['status'] == 2:
            q['resv_flag'] = 1
            sql_body += STATUS_SQL
        elif args['status'] == 3:
            q['resv_flag'] = 2
            sql_body += STATUS_SQL
        elif args['status'] == 4:
            q['resv_flag'] = 3
            sql_body += STATUS_SQL
        elif args['status'] == 5:
            q['resv_flag'] = 4
            sql_body += STATUS_SQL
        elif args['status'] == 6:
            q['resv_flag'] = 5
            sql_body += STATUS_SQL
        elif args['status'] == 7:
            q['resv_flag'] = 6
            sql_body += STATUS_SQL
        else:
            if args['status'] != 0:
                return {
                    'code': 'fail',
                    'message': '잘못된 status 값입니다.'
                }
        count_sql = RESERVATION_COUNT_SQL + sql_body
        if args['sort'] == 0:
            sql_body += 'ORDER BY RC.create_date DESC '
        elif args['sort'] == 1:
            sql_body += 'ORDER BY RC.resv_date '
            if args['order'] == 0:
                sql_body += 'DESC '
            elif args['order'] == 1:
                sql_body += 'ASC '
            else:
                return {
                    'code': 'fail',
                    'message': 'order가 잘못되었습니다.'
                }, 500
            sql_body += ", RC.modified_date DESC "
        elif args['sort'] == 2:
            sql_body += 'ORDER BY RC.resv_date '
            if args['order'] == 0:
                sql_body += 'DESC '
            elif args['order'] == 1:
                sql_body += 'ASC '
            else:
                return {
                    'code': 'fail',
                    'message': 'order가 잘못되었습니다.'
                }, 500
            sql_body += ", RC.modified_date DESC "
        elif args['sort'] == 3:
            sql_body += 'ORDER BY RC.resv_flag '
            if args['order'] == 0:
                sql_body += 'DESC '
            elif args['order'] == 1:
                sql_body += 'ASC '
            else:
                return {
                    'code': 'fail',
                    'message': 'order가 잘못되었습니다.'
                }, 500
            sql_body += ", RC.modified_date DESC "
        else:
            return {
                'code': 'fail',
                'message': 'sort가 잘못되었습니다.'
            }, 500
        select_sql = RESV_SELECT_SQL + sql_body
        rows = app.db.execute(text(select_sql), q).fetchall()
        cnt = app.db.execute(text(count_sql), q).fetchone()
        resp = []
        first_row = ['예약일', '에약시간', '이름', '휴대폰번호', '생년월일', '성별', '상태', '메모']
        for row in rows:
            data_row = []
            data_row.append(row['resv_date'].strftime('%Y-%m-%d'))
            data_row.append(row['resv_time'])
            data_row.append(row['user_name'])
            data_row.append(row['user_phone'])
            data_row.append(row['user_birth'])
            data_row.append(row['user_gender'])
            data_row.append(row['resv_flag'])
            data_row.append(row['user_memo'])
            if data_row[-2] == 0:
                data_row[-2] = '예약완료'
            elif data_row[-2] == 1:
                data_row[-2] = '예약취소'
            elif data_row[-2] == 2:
                data_row[-2] = '관리자 추가'
            elif data_row[-2] == 3:
                data_row[-2] = '관리자 취소'
            elif data_row[-2] == 4:
                data_row[-2] = '관리자 예약 변경'
            elif data_row[-2] == 5:
                data_row[-2] = '등록 완료'
            elif data_row[-2] == 6:
                data_row[-2] = '수집 완료'
            resp.append(data_row)
        second_row = ['총합']
        datas = [cnt['cnt']]
        pd.options.display.max_colwidth = 50
        df = pd.DataFrame(data=resp, columns=first_row)
        df2 = pd.DataFrame(data=datas, columns=second_row)
        df_axis = pd.concat([df, df2], axis=1)
        now = datetime.now()
        now_datetime = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
        timestamp = time.mktime(datetime.strptime(
            now_datetime, '%Y-%m-%d %H:%M:%S').timetuple())
        timestamp_split = str(timestamp).split('.')[0]
        fname = 'export_list_' + str(timestamp_split) + '.xlsx'
        print(app.app.config['RESERV_EXCEL_DIRECTORY'] + "/" + fname, ' : 경로!')
        df_axis.to_excel(
            excel_writer=app.app.config['RESERV_EXCEL_DIRECTORY'] + "/" + fname, index=False)
        return send_from_directory(app.app.config['RESERV_EXCEL_DIRECTORY'], fname)
