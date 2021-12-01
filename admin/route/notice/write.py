from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .notice import Notice
import app
from sqlalchemy import text

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('author', help='작성자', location='json', required=True)
parser.add_argument('title', help='글 제목', location='json', required=True)
parser.add_argument('content', help='글 내용', location='json', required=True)
parser.add_argument('attachment', help='업로드 된 파일 이름', location='json', required=False)
parser.add_argument('important', help='Top 공지 설정', type=int, location='json', required=False)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'
NOTICE_INSERT_SQL = 'INSERT INTO notice(title, content, important, is_file, author) VALUES(:title, :content, :important, :is_file, :author)'
NOTICE_FILE_INSERT_SQL = 'INSERT INTO notice_file(notice_id, file_name, file_path) VALUES(:notice_id, :file_name, :file_path)'
NOTICE_ADMIN_SELECT_SQL = 'SELECT id FROM admin_account WHERE admin_id=:author'
@Notice.route('/write')
class Write(Resource):
    @Notice.expect(parser)
    @Notice.response(200, 'Success')
    @Notice.response(401, 'Inauthorized')
    @Notice.response(500, 'Server Error')
    def post(self):
        """공지사항 글 작성 API"""
        args = parser.parse_args()
        token = args['Authorization']
        if token == None:
            return{
                'code' : 'fail',
                'message' : "토큰정보가 없습니다",
                'response' : {}
            },401
        
        token = token.split(' ')[1]
        row = app.db.execute(text(TOKEN_CHECK_SQL),{
            'token':token
        }).fetchone()
        if row == None:
            return{
                "code" : "fail",
                "message" : "토큰이 유효하지 않습니다",
                "response" : {}
            },401
        
        aq = {}
        aq['author'] = args['author']
        row2 = app.db.execute(text(NOTICE_ADMIN_SELECT_SQL),aq).fetchone()
        
        q={}
        q['title'] = args['title']
        q['content'] = args['content']

        if row['aid'] == row2['id']:
            q['author'] = args['author']
        else:
            return{
                "code": "fail",
                "message": "작성자가 유효하지 않습니다",
                "response": {}
            }, 500

        if args['attachment'] == None:
            q['is_file'] = 0
        else:
            q['is_file'] = 1
        if args['important'] == None:
            q['important'] = 0
        else:
            q['important'] = args['important']

        row_id = app.db.execute(text(NOTICE_INSERT_SQL),q).lastrowid

        if q['is_file'] == 1:
            q2 = {}
            q2['notice_id'] = row_id
            print(args['attachment'][0:21])
            q2['file_name'] = args['attachment'][22:]
            q2['file_path'] = args['attachment']
            app.db.execute(text(NOTICE_FILE_INSERT_SQL),q2)

        return{
            'code': 'success',
            'message':'success',
            'responce': {
                'flag' : True
            }
        }
