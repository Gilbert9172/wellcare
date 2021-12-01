from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .notice import Notice
import app
from sqlalchemy import text
import secrets
import werkzeug
import os
import time

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('attachment', help='첨부파일', type=werkzeug.datastructures.FileStorage, location='files', required=True)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'


@Notice.route('/upload')
class Upload(Resource):
    @Notice.expect(parser)
    @Notice.response(200, 'Success')
    @Notice.response(401, 'Unauthorized')
    def post(self):
        """공지사항 첨부파일 Upload API"""
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


        attachment = args['attachment']
        filename = attachment.filename
        filepath = app.app.config['NOTICE_UPLOAD_DIRECTORY'] + "/" + filename
        if os.path.isfile(filepath) == True:
            return {
                'code': 'fail',
                'message': '같은 이름의 파일이 존재합니다. 다른 이름으로 변경 후, 업로드해주세요',
                'response': {}
            }, 500

        attachment.save(filepath)
        attachment_url = '/admin/api/v1/notice/' + filename

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'filePath': attachment_url
            }
        }, 200
