from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .notice import Notice
import app
from sqlalchemy import text

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('notice_id', help='공지사항 ID(pk)', location='json', type=int, required=True)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'
SELECT_NOTICE_SQL = 'SELECT * FROM notice WHERE id=:notice_id'
DELETE_NOTICE_SQL = 'DELETE FROM notice WHERE id=:notice_id'
DELETE_NOTICE_FILE_SQL = 'DELETE FROM notice_file WHERE notice_id=:notice_id'


@Notice.route('/delete')
class Delete(Resource):
    @Notice.expect(parser)
    @Notice.response(200, 'Success')
    @Notice.response(401, 'Unauthorized')
    @Notice.response(500, 'Internal Server Error')
    def delete(self):
        """공지사항 글 삭제 API"""
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
        q['notice_id'] = args['notice_id']

        row = app.db.execute(text(SELECT_NOTICE_SQL), q).fetchone()

        if row == None:
            return {
                'code': 'fail',
                'message': '잘못된 공지사항 ID입니다'
            }, 500

        app.db.execute(text(DELETE_NOTICE_SQL), q)
        if row['is_file'] == '1':
            app.db.execute(text(DELETE_NOTICE_FILE_SQL), q)

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'flag': True
            }
        }, 200
