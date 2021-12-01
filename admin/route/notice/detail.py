from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .notice import Notice
import app
from sqlalchemy import text

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('id', help='공지사항 ID(pk)', type=int, required=True)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'
SELECT_NOTICE_SQL = 'SELECT * FROM notice WHERE id=:id'
SELECT_NOTICE_FILE_SQL = 'SELECT * FROM notice_file WHERE notice_id=:id'


@Notice.route('/detail')
class Detail(Resource):
    @Notice.expect(parser)
    @Notice.response(200, 'Success')
    @Notice.response(401, 'Unauthorized')
    @Notice.response(500, 'Internal Server Error')
    def get(self):
        """공지사항 글 상세 API"""
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
        q['id'] = args['id']

        row = app.db.execute(text(SELECT_NOTICE_SQL), q).fetchone()

        if row == None:
            return {
                'code': 'fail',
                'message': '잘못된 공지사항 ID입니다'
            }, 500

        resp = dict()
        resp['id'] = row['id']
        resp['title'] = row['title']
        resp['content'] = row['content']
        resp['important'] = row['important']
        resp['is_file'] = row['is_file']
        resp['author'] = row['author']
        resp['createDate'] = row['create_date'].strftime('%Y-%m-%d %H:%M:%S')
        resp['modifiedDate'] = row['modified_date'].strftime(
            '%Y-%m-%d %H:%M:%S')
        resp['file'] = []

        if row['is_file'] == '1':
            row2 = app.db.execute(text(SELECT_NOTICE_FILE_SQL), q).fetchall()
            for r in row2:
                resp['file'].append(r['file_path'])

        return {
            'code': 'success',
            'message': 'success',
            'response': resp
        }, 200
