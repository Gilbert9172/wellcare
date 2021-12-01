from flask import send_from_directory
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .root import Root
from sqlalchemy import text
import app

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'

@Root.route('/<filename>')
class Photos(Resource):
    @Root.expect(parser)
    @Root.response(200, 'Success')
    @Root.response(401, 'Unauthorized')
    def get(self, filename):
        """업로드 파일 가져오기"""
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

        photo_path = app.app.config['UPLOAD_DIRECTORY']
        return send_from_directory(photo_path, filename)
