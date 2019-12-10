import config
import redis
from flask import Flask
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from pymysql import install_as_MySQLdb
from plugins.HYplugins.orm import db
from plugins.HYplugins.core.primary import CoreApi

# core
core_api = CoreApi()

# 应用
install_as_MySQLdb()
""" 已废弃-> HYcore
# 微信
wechat_api = wechat.WechatApi(app_id=config.APP_ID, app_secret=config.APP_SECRET)
"""

# redis
pool = redis.ConnectionPool(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True)
Redis = redis.StrictRedis(connection_pool=pool)
serializer = Serializer(secret_key=config.SECRET_KEY, expires_in=60 * 60 * 24 * 30)


def register_blueprint(app):
    """注册蓝图"""
    from views.user import api
    app.register_blueprint(api)

    from views.common import api
    app.register_blueprint(api)

    from views.business import api
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
