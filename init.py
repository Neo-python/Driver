import sys
import config
import logging
import redis
from flask import Flask
from pymysql import install_as_MySQLdb
from plugins.HYplugins.sms import SMS
from plugins.HYplugins.orm import db
from plugins.HYplugins import wechat
from sts.sts import Sts
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

# 短信
sms = SMS(app_id=config.SMS_APP_ID, app_key=config.SMS_APP_KEY)
# 应用
install_as_MySQLdb()
# cos
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
cos_config = CosConfig(Region=config.region, SecretId=config.SecretId, SecretKey=config.SecretKey, Token=config.token,
                       Scheme=config.scheme)
client = CosS3Client(cos_config)
# cos token
cos_sts = Sts(config.sts_config)
# 微信
wechat_api = wechat.WechatApi(app_id=config.APP_ID, app_secret=config.APP_SECRET)
# redis
pool = redis.ConnectionPool(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True)
Redis = redis.StrictRedis(connection_pool=pool)

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def register_blueprint(app):
    """注册蓝图"""
    from views.user import api
    app.register_blueprint(api)

    from views.common import api
    app.register_blueprint(api)


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    register_blueprint(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    # app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
    with app.app_context():
        db.create_all(app=app)
    return app
