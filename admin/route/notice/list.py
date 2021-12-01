from flask import request
from flask_restx import Resource, reqparse
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null
from .notice import Notice
import app
from sqlalchemy import text

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('start', help='시작 index', type=int, required=True, default=0)
parser.add_argument('size', help='페이지 수', type=int, required=True, default=10)
parser.add_argument('startdate', help='작성일자 시작', required=False)
parser.add_argument('enddate', help='작성일자 끝', required=False)
parser.add_argument('q', help='검색(제목)', required=False)
parser.add_argument('sort', help='없음(0), 번호(1), 제목(2), 작성자(3)', type=int, required=True, default=0)
parser.add_argument('order', help='내림차순(0), 오름차순(1)', type=int, required=True, default=0)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'

# SQL문 HEAD
NOTICE_COUNT_SQL = 'SELECT count(*) as cnt '
NOTICE_SELECT_SQL = 'SELECT * '

# SQL문 BODY
NOTICE_SELECT_BODY = 'FROM notice WHERE 1 '

# SQL문 조건
MIN_DATE_SQL = 'AND create_date >= str_to_date(:startdate, \'%Y-%m-%d\') '
MAX_DATE_SQL = 'AND create_date <= str_to_date(:enddate, \'%Y-%m-%d %H:%i:%s\') '
NOTICE_Q_SQL = 'AND title LIKE :q1 '
LIMIT_SQL = 'LIMIT :start, :size '


@Notice.route('/list')
class List(Resource):
    @Notice.expect(parser)
    @Notice.response(200, 'Success')
    @Notice.response(401, 'Unauthorized')
    @Notice.response(500, 'Internal Server Error')
    def get(self):
        """공지사항 리스트 API"""
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
        sql_body = NOTICE_SELECT_BODY
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
            sql_body += NOTICE_Q_SQL
        
        count_sql = NOTICE_COUNT_SQL + sql_body

        if args['sort'] == 0:
            sql_body += 'ORDER BY important DESC, id DESC '
        elif args['sort'] == 1:
            sql_body += 'ORDER BY important DESC, id '
            if args['order'] == 0:
                sql_body += 'DESC '
            elif args['order'] == 1:
                sql_body += 'ASC '
            else:
                return {
                    'code': 'fail',
                    'message': 'order가 잘못되었습니다.'
                }, 500
            sql_body += ", modified_date DESC "
        elif args['sort'] == 2:
            sql_body += 'ORDER BY important DESC, title '
            if args['order'] == 0:
                sql_body += 'DESC '
            elif args['order'] == 1:
                sql_body += 'ASC '
            else:
                return {
                    'code': 'fail',
                    'message': 'order가 잘못되었습니다.'
                }, 500
            sql_body += ", modified_date DESC "
        elif args['sort'] == 3:
            sql_body += 'ORDER BY important DESC, author '
            if args['order'] == 0:
                sql_body += 'DESC '
            elif args['order'] == 1:
                sql_body += 'ASC '
            else:
                return {
                    'code': 'fail',
                    'message': 'order가 잘못되었습니다.'
                }, 500
            sql_body += ", modified_date DESC "
        else:
            return {
                'code': 'fail',
                'message': 'sort가 잘못되었습니다.'
            }, 500
        
        sql_body += LIMIT_SQL

        select_sql = NOTICE_SELECT_SQL + sql_body
        print(select_sql)
        rows = app.db.execute(text(select_sql), q).fetchall()
        cnt = app.db.execute(text(count_sql), q).fetchone()
        resp = []
        for row in rows:
            r = {}
            r['id'] = row['id']
            r['important'] = row['important']
            r['title'] = row['title']
            if row['is_file'] == None or row['is_file'] == '':
                r['is_file'] = '-'
            else:
                r['is_file'] = row['is_file']
            r['author'] = row['author']
            r['create_date'] = row['create_date'].strftime('%Y-%m-%d %H:%M:%S')
            resp.append(r)

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'count': cnt['cnt'],
                'List': resp
            }
        }, 200
