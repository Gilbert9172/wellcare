from flask import request
from sqlalchemy.sql.expression import true
from flask_restx import Resource, Api, Namespace, fields, reqparse, inputs
from .root import Root
import app
from sqlalchemy import text
from io import BytesIO
from PIL import Image
import secrets
import werkzeug
import os
import time
parser = reqparse.RequestParser()
parser.add_argument('agree_id', help='참여자 ID',location='form', required=True)
parser.add_argument('agree_image1', help='동의서 파일1', type=werkzeug.datastructures.FileStorage, location='files',required=True)
parser.add_argument('agree_image2', help='동의서 파일2', type=werkzeug.datastructures.FileStorage, location='files',required=True)
parser.add_argument('agree_image3', help='동의서 파일3', type=werkzeug.datastructures.FileStorage, location='files',required=True)
parser.add_argument('agree_image4', help='동의서 파일4', type=werkzeug.datastructures.FileStorage, location='files',required=True)
parser.add_argument('agree_image5', help='동의서 파일5', type=werkzeug.datastructures.FileStorage, location='files',required=True)
parser.add_argument('agree_image6', help='동의서 파일6', type=werkzeug.datastructures.FileStorage, location='files',required=True)
parser.add_argument('agree_image7', help='동의서 파일7', type=werkzeug.datastructures.FileStorage, location='files',required=True)
parser.add_argument('agree_image8', help='동의서 파일8', type=werkzeug.datastructures.FileStorage, location='files',required=True)
parser.add_argument('agree_image9', help='동의서 파일9', type=werkzeug.datastructures.FileStorage, location='files', required=True)
AGREEE_PHOTOS_INSERT_SQL = 'INSERT INTO agree_photos(agree_id, agree_image1, agree_image2, agree_image3, agree_image4,agree_image5, agree_image6, agree_image7, agree_image8, agree_image9) VALUES(:agree_id, :agree_image1, :agree_image2, :agree_image3, :agree_image4, :agree_image5, :agree_image6, :agree_image7, :agree_image8, :agree_image9) '
@Root.route('/upload')
class file_upload(Resource):
    @Root.expect(parser)
    @Root.response(200, 'Success')
    @Root.response(500, 'Internal Server Error')
    def post(self):
        """사진 Upload API"""
        args = parser.parse_args()
        # try:
        q={}
        q['agree_id'] = args['agree_id']
        q['agree_image1'] = args['agree_image1']
        q['agree_image2'] = args['agree_image2']
        q['agree_image3'] = args['agree_image3']
        q['agree_image4'] = args['agree_image4']
        q['agree_image5'] = args['agree_image5']
        q['agree_image6'] = args['agree_image6']
        q['agree_image7'] = args['agree_image7']
        q['agree_image8'] = args['agree_image8']
        q['agree_image9'] = args['agree_image9']
        
        image_list =[]
        image_list.append(args['agree_image1'])
        image_list.append(args['agree_image2'])
        image_list.append(args['agree_image3'])
        image_list.append(args['agree_image4'])
        image_list.append(args['agree_image5'])
        image_list.append(args['agree_image6'])
        image_list.append(args['agree_image7'])
        image_list.append(args['agree_image8'])
        image_list.append(args['agree_image9'])

        for index in range(len(image_list)):
            name, ext = os.path.splitext(image_list[index].filename)
            photo_name = name + '_' + str(int(time.time())) + ext
            photo_path = app.app.config['UPLOAD_DIRECTORY'] + "/" + photo_name
            image_list[index].save(photo_path)
            photo_url = '/api/v1/agree/' + photo_name
            q['agree_image'+str((index+1))] = photo_url
        rows = app.db2.execute(text(AGREEE_PHOTOS_INSERT_SQL),q).lastrowid
    
        return {
            'code': 'success',
            'message': 'success',
            'response': {
                'agree_images1': q['agree_image1'],
                'agree_images2': q['agree_image2'],
                'agree_images3': q['agree_image3'],
                'agree_images4': q['agree_image4'],
                'agree_images5': q['agree_image5'],
                'agree_images6': q['agree_image6'],
                'agree_images7': q['agree_image7'],
                'agree_images8': q['agree_image8'],
                'agree_images9': q['agree_image9'],
            }
        }, 200
