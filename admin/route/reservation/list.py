from flask import request
from flask_restx import Resource, reqparse
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null
from .reservation import Reservation
import app
from sqlalchemy import text

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('start', help='시작 index', type=int, required=True, default=0)
parser.add_argument('size', help='페이지 수', type=int, required=True, default=10)
parser.add_argument('startdate', help='예약일자 시작', required=False)
parser.add_argument('enddate', help='예약일자 끝', required=False)
parser.add_argument('q', help='검색(이름, 휴대폰번호, 생년월일)', required=False)
parser.add_argument('gender', help='성별(전체(0), 남성(1), 여성(2)', type=int, required=True, default=0)
parser.add_argument('status', action='append', help='상태(전체(0), 예약 완료(1), 예약 취소(2), 관리자 추가(3), 관리자 취소(4), 관리자 예약 변경(5), 등록 완료(6), 수집 완료(7)', type=int, required=True)
parser.add_argument('sort', help='없음(0), 예약일(1), 생년월일(2), 예약시간(3)', type=int, required=True, default=0)
parser.add_argument('order', help='내림차순(0), 오름차순(1)', type=int, required=True, default=0)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'

# SQL문 HEAD
RESERVATION_COUNT_SQL = 'SELECT count(*) as cnt '
RESV_SELECT_SQL = 'SELECT RC.resv_date, RC.resv_time, U.user_name, U.user_phone, U.user_birth, U.user_gender, U.user_memo, RC.resv_flag, RC.resv_cancel_note, RC.modified_date, RC.create_date, RC.id '

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


@Reservation.route('/list')
class List(Resource):
    @Reservation.expect(parser)
    @Reservation.response(200, 'Success')
    @Reservation.response(401, 'Unauthorized')
    @Reservation.response(500, 'Internal Server Error')
    def get(self):
        """예약 리스트 API"""
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
        if args['status'][0] == 0:
            sql_body
        else:
            for status in args['status']:
                if status == 1:
                    q['resv_flag1'] = 0
                    if 'resv_flag' in sql_body:
                        sql_body += ' OR resv_flag=:resv_flag1'
                    else:
                        sql_body += 'AND (resv_flag=:resv_flag1'
                elif status == 2:
                    q['resv_flag2'] = 1
                    if 'resv_flag' in sql_body:
                        sql_body += ' OR resv_flag=:resv_flag2'
                    else:
                        sql_body += 'AND (resv_flag=:resv_flag2'
                elif status == 3:
                    q['resv_flag3'] = 2
                    if 'resv_flag' in sql_body:
                        sql_body += ' OR resv_flag=:resv_flag3'
                    else:
                        sql_body += 'AND (resv_flag=:resv_flag3'
                elif status == 4:
                    q['resv_flag4'] = 3
                    if 'resv_flag' in sql_body:
                        sql_body += ' OR resv_flag=:resv_flag4'
                    else:
                        sql_body += 'AND (resv_flag=:resv_flag4'
                elif status == 5:
                    q['resv_flag5'] = 4
                    if 'resv_flag' in sql_body:
                        sql_body += ' OR resv_flag=:resv_flag5'
                    else:
                        sql_body += 'AND (resv_flag=:resv_flag5'
                elif status == 6:
                    q['resv_flag6'] = 5
                    if 'resv_flag' in sql_body:
                        sql_body += ' OR resv_flag=:resv_flag6'
                    else:
                        sql_body += 'AND (resv_flag=:resv_flag6'
                elif status == 7:
                    q['resv_flag7'] = 6
                    if 'resv_flag' in sql_body:
                        sql_body += ' OR resv_flag=:resv_flag7'
                    else:
                        sql_body += 'AND (resv_flag=:resv_flag7'
                else:
                    if status != 0:
                        return {
                            'code': 'fail',
                            'message': '잘못된 status 값입니다.'
                        }
            sql_body += ') '
            
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
            sql_body += 'ORDER BY U.user_birth '
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
            sql_body += 'ORDER BY RC.resv_time '
            if args['order'] == 0:
                sql_body += 'DESC '
            elif args['order'] == 1:
                sql_body += 'ASC '
            else:
                return {
                    'code': 'fail',
                    'message': 'order가 잘못되었습니다.'
                }, 500

            sql_body += ", RC.resv_date ASC "
        else:
            return {
                'code': 'fail',
                'message': 'sort가 잘못되었습니다.'
            }, 500
        
        sql_body += LIMIT_SQL

        select_sql = RESV_SELECT_SQL + sql_body
        rows = app.db.execute(text(select_sql), q).fetchall()
        cnt = app.db.execute(text(count_sql), q).fetchone()
        resp = []
        for row in rows:
            r = {}
            r['resv_date'] = row['resv_date'].strftime('%Y-%m-%d')
            r['resv_time'] = row['resv_time']
            r['user_name'] = row['user_name']
            r['user_phone'] = row['user_phone']
            r['user_birth'] = row['user_birth']
            r['user_gender'] = row['user_gender']
            if row['user_memo'] == None:
                r['user_memo'] = ''
            else:
                r['user_memo'] = row['user_memo']
            r['resv_flag'] = row['resv_flag']
            if row['resv_cancel_note'] == None:
                r['resv_cancel_note'] = ''
            else:
                r['resv_cancel_note'] = row['resv_cancel_note']
            r['resv_num'] = row['id']
            if row['resv_flag'] == 0 or row['resv_flag'] == 1:
                r['modified_date'] = None
            else:
                r['modified_date'] = row['modified_date'].strftime('%Y-%m-%d %H:%M:%S')
            resp.append(r)

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'count': cnt['cnt'],
                'List': resp
            }
        }, 200
