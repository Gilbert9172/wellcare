from flask import request
from flask_restx import Resource, reqparse
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null
from .admin import Admin
import app
from sqlalchemy import text

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('start', help='시작 index', type=int, required=True, default=0)
parser.add_argument('size', help='페이지 수', type=int, required=True, default=10)
parser.add_argument('q', help='검색(이름, 휴대폰번호)', required=False)
parser.add_argument('sort', help='없음(0), 번호(1), 등록일(2), 최근 로그인 일시(3),', type=int, required=True, default=0)
parser.add_argument('order', help='내림차순(0), 오름차순(1)', type=int, required=True, default=0)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'

# SQL문 HEAD
ADMIN_COUNT_SQL = 'SELECT count(*) as cnt '
ADMIN_SELECT_SQL = 'SELECT * '

# SQL문 BODY
ADMIN_SELECT_BODY = 'FROM admin_account AA LEFT OUTER JOIN (SELECT aid, last_login FROM admin_account_token) AT ON AA.id=AT.aid WHERE 1 '

# SQL문 조건
USER_Q_SQL = 'AND (name LIKE :q1 or phone LIKE :q1) '
LIMIT_SQL = 'LIMIT :start, :size '


@Admin.route('/list')
class List(Resource):
    @Admin.expect(parser)
    @Admin.response(200, 'Success')
    @Admin.response(401, 'Unauthorized')
    @Admin.response(500, 'Internal Server Error')
    def get(self):
        """관리자 리스트 API"""
        args = parser.parse_args()
        token = args['Authorization']

        if token == None:
            return {
                'code': 'fail',
                'message': '토큰정보가 없습니다',
                'response': {}
            }, 401

        token = token.split(' ')[1]
        ll = app.db.execute(text(TOKEN_CHECK_SQL), {
            'token': token
        }).fetchone()
        if ll == None:
            return {
                'code': 'fail',
                'message': '토큰이 유효하지 않습니다',
                'response': {}
            }, 401
        
        q = dict()
        sql_body = ADMIN_SELECT_BODY
        q['start'] = args['start']
        q['size'] = args['size']
        if args['q'] != None:
            q['q'] = args['q']
            q['q1'] = '%' + args['q'] + '%'
        else:
            q['q'] = None
        
        count_sql = ADMIN_COUNT_SQL + sql_body

        if q['q'] != None and q['q'] != '':
            sql_body += USER_Q_SQL
            count_sql += USER_Q_SQL

        if args['sort'] == 0:
            sql_body += 'ORDER BY id DESC '
        elif args['sort'] == 1:
            sql_body += 'ORDER BY id '
            if args['order'] == 0:
                sql_body += 'DESC '
            elif args['order'] == 1:
                sql_body += 'ASC '
            else:
                return {
                    'code': 'fail',
                    'message': 'order가 잘못되었습니다.'
                }, 500
        elif args['sort'] == 2:
            sql_body += 'ORDER BY create_date '
            if args['order'] == 0:
                sql_body += 'DESC '
            elif args['order'] == 1:
                sql_body += 'ASC '
            else:
                return {
                    'code': 'fail',
                    'message': 'order가 잘못되었습니다.'
                }, 500
        elif args['sort'] == 3:
            sql_body += 'ORDER BY last_login '
            if args['order'] == 0:
                sql_body += 'DESC '
            elif args['order'] == 1:
                sql_body += 'ASC '
            else:
                return {
                    'code': 'fail',
                    'message': 'order가 잘못되었습니다.'
                }, 500
        else:
            return {
                'code': 'fail',
                'message': 'sort가 잘못되었습니다.'
            }, 500
        
        sql_body += LIMIT_SQL

        select_sql = ADMIN_SELECT_SQL + sql_body

        rows = app.db.execute(text(select_sql), q).fetchall()
        cnt = app.db.execute(text(count_sql), q).fetchone()
        resp = []
        for row in rows:
            r = {}
            r['id'] = row['id']
            r['admin_id'] = row['admin_id']
            r['name'] = row['name']
            r['email'] = row['email']
            r['phone'] = row['phone']
            r['create_date'] = row['create_date'].strftime('%Y-%m-%d %H:%M:%S')
            if row['last_login'] == None:
                r['last_log'] = '-'
            else:
                r['last_login'] = row['last_login'].strftime('%Y-%m-%d %H:%M:%S')
            resp.append(r)

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'count': cnt['cnt'],
                'List': resp
            }
        }, 200
