from flask import request
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .admin import Admin
import app
from sqlalchemy import text

parser = reqparse.RequestParser()
parser.add_argument('Authorization', help='Bearer 토큰', location='headers', required=True)
parser.add_argument('id', help='관리자 ID', location='json', type=int, required=True)

TOKEN_CHECK_SQL = 'SELECT AT.* FROM admin_account_token AS AT, admin_account AS A WHERE AT.token=:token AND AT.aid = A.id'
ADMIN_SELECT_SQL = 'SELECT * FROM admin_account WHERE id=:id'
DELETE_ADMIN_SQL = 'DELETE FROM admin_account WHERE id=:id'
DELETE_ADMIN_TOKEN_SQL = 'DELETE FROM admin_account_token WHERE aid=(SELECT aid FROM admin_account WHERE id=:id)'

@Admin.route('/delete')
class Delete(Resource):
    @Admin.expect(parser)
    @Admin.response(200, 'Success')
    @Admin.response(401, 'Unauthorized')
    @Admin.response(500, 'Internal Server Error')
    def delete(self):
        """관리자 정보 삭제 API"""
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

        q = {}
        q['id'] = args['id']
        row2 = app.db.execute(text(ADMIN_SELECT_SQL),q).fetchone()
        if row2['id'] == row['aid']:
            return{
                'code' : 'fail',
                'message' : "본인은 삭제할 수 없습니다",
                'response': {
                    'flag' : False
                }
            },500


        row = app.db.execute(text(ADMIN_SELECT_SQL),q).fetchone()
        if row == None:
            return {
                'code':'fail',
                'message':'존재하지 않는 아이디 입니다.',
                'response' : {
                    'flag' : False
                }
            },500

        app.db.execute(text(DELETE_ADMIN_SQL),q)
        app.db.execute(text(DELETE_ADMIN_TOKEN_SQL),q)

        return {
            'code':'success',
            'message':'succes',
            'response': {
                'flag' : True
            }
        }
