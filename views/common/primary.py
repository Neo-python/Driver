import config
from flask import request, g
from views.common import api
from init import Redis, core_api
from forms.common.primary import SMSCodeForm
from plugins.HYplugins.common import ordinary
from plugins.HYplugins.common.authorization import login, auth
from plugins.HYplugins.error import ViewException


@api.route('/upload_url/')
@auth.login_required
def upload_url():
    """获取上传图片授权地址"""
    genre = request.args.get('genre', default=None)
    suffix = request.args.get('suffix', default=None)

    return core_api.upload_url(user_uuid=g.user.uuid, genre=genre, suffix=suffix)


@api.route('/upload_credentials/')
@auth.login_required
def upload_credentials():
    """腾讯cos上传凭证
    文档:https://github.com/tencentyun/qcloud-cos-sts-sdk/tree/master/python
    """

    return core_api.upload_credentials()


@api.route('/send_sms/code/', methods=['POST'])
def send_sms():
    """发送短信接口
    params:统一规范 验证码 + 时效(分钟)
    """
    sms_validity_period = 100

    form = SMSCodeForm().validate_()
    code = ordinary.generate_verify_code()

    key = f'validate_phone_{form.genre.data}_{form.phone.data}'
    Redis.set(key, code, ex=60 * sms_validity_period)  # 设置缓存

    return core_api.send_sms(phone=form.phone.data, code=code,
                             template_id=config.SMS_TEMPLATE_REGISTERED[form.genre.data])
