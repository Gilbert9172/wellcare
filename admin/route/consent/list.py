from flask import request
from flask_restx import Resource, reqparse
from io import BytesIO
# from PIL import Image
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null
from .consent import Consent
import app
from sqlalchemy import text

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('start', help='시작 index', type=int, required=True, default=0)
parser.add_argument('size', help='페이지 수', type=int, required=True, default=10)
parser.add_argument('q', help='검색(이름, 생년월일)', required=False)
parser.add_argument('sort', help='없음(0), 작성일시(1)', type=int, required=True, default=0)
parser.add_argument('order', help='내림차순(0), 오름차순(1)', type=int, required=True, default=0)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'

# SQL문 HEAD
CONSENT_COUNT_SQL = 'SELECT count(*) as cnt '
CONSENT_SELECT_SQL = 'SELECT * '

# SQL문 BODY
CONSENT_SELECT_BODY = 'FROM agree A LEFT OUTER JOIN(SELECT agree_id, agree_image1, agree_image2, agree_image3, agree_image4, agree_image5, agree_image6, agree_image7, agree_image8, agree_image9 FROM agree_photos) AP ON AP.agree_id=A.id WHERE 1 '

# SQL문 조건
AGREE_Q_SQL = 'AND (agree_name LIKE :q1 or agree_birth LIKE :q1) '
LIMIT_SQL = 'LIMIT :start, :size '


@Consent.route('/list')
class List(Resource):
    @Consent.expect(parser)
    @Consent.response(200, 'Success')
    @Consent.response(401, 'Unauthorized')
    @Consent.response(500, 'Internal Server Error')
    def get(self):
        """동의서 리스트 API"""
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
        sql_body = CONSENT_SELECT_BODY
        q['start'] = args['start']
        q['size'] = args['size']
        if args['q'] != None:
            q['q1'] = '%' + args['q'] + '%'
            sql_body += AGREE_Q_SQL
        
        count_sql = CONSENT_COUNT_SQL + sql_body

        if args['sort'] == 0:
            sql_body += 'ORDER BY create_date DESC '
        elif args['sort'] == 1:
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
        else:
            return {
                'code': 'fail',
                'message': 'sort가 잘못되었습니다.'
            }, 500
        
        sql_body += LIMIT_SQL

        select_sql = CONSENT_SELECT_SQL + sql_body

        rows = app.db2.execute(text(select_sql), q).fetchall()
        cnt = app.db2.execute(text(count_sql), q).fetchone()
        resp = []
        for row in rows:
            r = {}
            re = []
            re2 = []
            r['aid'] = row['id']
            r['agree_name'] = row['agree_name']
            r['agree_birth'] = row['agree_birth']
            r['agree_gender'] = row['agree_gender']
            r['create_date'] = row['create_date'].strftime('%Y-%m-%d %H:%M:%S')
            re.append(row['agree_image1'])
            re.append(row['agree_image2'])
            re.append(row['agree_image3'])
            re.append(row['agree_image4'])
            re.append(row['agree_image5'])
            re.append(row['agree_image6'])
            re.append(row['agree_image7'])
            r['img_list_1'] = re 
            re2.append(row['agree_image8'])
            re2.append(row['agree_image9'])
            r['img_list_2'] = re2
            resp.append(r)

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'count': cnt['cnt'],
                'List': resp
            }
        }, 200
