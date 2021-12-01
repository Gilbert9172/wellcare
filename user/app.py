from flask import Flask
from flask_restx import Resource, Api
from flask_cors import CORS
from route.root.root import Root
from route.reservation.reservation import Reservation
import sqlalchemy.pool as pool

URL_PREFIX = '/wdw/api/v1'

app = Flask(__name__)
CORS(app)
api = Api(
  app,
  version='0.1',
  title='웰케어 backend API Server',
  description='웰케어 backend API Server'
)

api.add_namespace(Root, URL_PREFIX)
api.add_namespace(Reservation, URL_PREFIX + '/reservation')

# DB 연결
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = 'mysql+pymysql://' + os.getenv('MYSQL_USER') + ':' + os.getenv('MYSQL_PASSWORD') + '@' + os.getenv('MYSQL_HOST') + ':' + os.getenv('MYSQL_PORT') + '/' + os.getenv('MYSQL_DATABASE') + '?charset=' + os.getenv('MYSQL_CHARSET')

from sqlalchemy import create_engine, text
db = create_engine(DB_URL, encoding='utf8', pool_recycle=500)

# app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
# app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
# app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True

# app.config['UPLOAD_DIRECTORY'] = os.getenv('UPLOAD_DIRECTORY')
# app.config['NOTICE_UPLOAD_DIRECTORY'] = os.getenv('NOTICE_UPLOAD_DIRECTORY')
# app.config['LOGO_DIRECTORY'] = os.getenv('LOGO_DIRECTORY')
# app.config['COMPARES_DIRECTORY'] = os.getenv('COMPARES_DIRECTORY')

# app.config['FCM_API_KEY'] = os.getenv('FCM_API_KEY')

app.db = db

# port = 9000
port = int(os.getenv('PORT'))

# from flask_apscheduler import APScheduler

# app.scheduler = APScheduler()
# app.scheduler.add_job(id='FCM_Worker', func=fcmworker, trigger='interval', seconds=60)
# app.scheduler.start()

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=port)
