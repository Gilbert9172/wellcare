from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .notice import Notice
import app
from sqlalchemy import text

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('id', help='공지사항 ID(pk)', location='json', type=int, required=True)
parser.add_argument('title', help='글 제목', location='json', required=False)
parser.add_argument('content', help='글 내용', location='json', required=False)
parser.add_argument('attachment', help='업로드 된 파일 이름', location='json', required=False)
parser.add_argument('important', help='Top 공지 설정', type=int, location='json', required=False)

TOKEN_CHECK_SQL = 'SELECT * FROM admin_account_token WHERE token=:token'
NOTICE_UPDATE_SQL = 'UPDATE notice SET '
NOTICE_UPDATE_WHERE = 'WHERE id=:id'
NOTICE_FILE_DELETE_SQL = 'DELETE FROM notice_file WHERE notice_id=:notice_id'
NOTICE_FILE_INSERT_SQL = 'INSERT INTO notice_file(notice_id, file_name, file_path) VALUES(:notice_id, :file_name, :file_path)'


@Notice.route('/modify')
class Modify(Resource):
    @Notice.expect(parser)
    @Notice.response(200, 'Success')
    @Notice.response(401, 'Unauthorized')
    @Notice.response(500, 'Internal Server Error')
    def put(self):
        """공지사항 글 업데이트 API"""
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
        sql = NOTICE_UPDATE_SQL
        flag = False
        if args['title'] != None:
            q['title'] = args['title']
            sql += 'title=:title,'
            flag = True
        if args['content'] != None:
            q['content'] = args['content']
            sql += 'content=:content,'
            flag = True
        if args['attachment'] != None:
            if args['attachment'] == '':
                q['is_file'] = 0
            else:
                q['is_file'] = 1
            sql += 'is_file=:is_file,'
            flag = True
        else:
            q['is_file'] = None
        if args['important'] != None:
            q['important'] = 1
            sql += 'important=:important,'
            flag = True

        if flag == False:
            return {
                'code': 'fail',
                'message': '업데이트 내용을 입력하세요',
                'response': {}
            }, 500

        sql = sql[:-1] + " "
        sql += NOTICE_UPDATE_WHERE

        app.db.execute(text(sql), q)

        if q['is_file'] != None:
            if q['is_file'] == 1:
                q2 = dict()
                q2['notice_id'] = q['id']
                q2['file_name'] = args['attachment']
                q2['file_path'] = args['attachment']
                app.db.execute(text(NOTICE_FILE_DELETE_SQL), q2)
                app.db.execute(text(NOTICE_FILE_INSERT_SQL), q2)
            elif q['is_file'] == 0:
                q2 = dict()
                q2['notice_id'] = q['id']
                app.db.execute(text(NOTICE_FILE_DELETE_SQL), q2)

        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'flag': True
            }
        }, 200
