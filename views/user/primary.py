import time
from flask import g
from init import Redis, core_api
from views.user import api
from plugins.HYplugins.common import result_format
from plugins.HYplugins.common.authorization import login, auth
from models.user import Driver
from forms import user as forms


@api.route('/sign_in/', methods=['POST'])
def sign_in():
    """登录"""
    form = forms.SignInForm().validate_()
    user = Driver.query.filter_by(open_id=form.open_id).first()

    if user:  # 用户信息存在,并且用户类型已经选择

        return result_format(data={'token': user.generate_token(), 'user_info': user.serialization()})
    else:
        return result_format(error_code=4000, message='客户未注册')


@api.route('/refresh_token/')
@auth.login_required
def refresh_token():
    """刷新token"""

    day = 20

    iat = g.user.get('iat')

    if time.time() - time.mktime(time.localtime(iat)) > (60 * 60 * 24 * day):
        user = Driver.query.filter_by(uuid=g.user.uuid).first_or_404()
        return result_format(data={'token': user.generate_token(), 'user_info': user.serialization()})
    else:
        return result_format(error_code=5009, message='token刷新失败.')


@api.route('/registered/', methods=['POST'])
def registered():
    """注册成为驾驶员
    注册完成 删除Redis中的短信验证码信息
    :return:
    """

    form = forms.RegisteredForm().validate_()

    data = form.data

    data.pop('code')
    data.pop('wechat_code')

    Driver(open_id=form.open_id, **data).direct_commit_()
    Redis.delete(form.redis_key)  # 删除验证码
    core_api.notice_sms(template_id="484145", params=[form.name.data, form.number_plate.data])  # 通知管理员注册完成
    return result_format()


@api.route('/driver/info/')
@login()
def driver_info():
    """驾驶员信息查询"""
    user = Driver.query.filter_by(uuid=g.user.uuid).first_or_404()
    return result_format(data=user.serialization())


@api.route('/driver/info/edit/', methods=['POST'])
@login()
def driver_info_edit():
    """驾驶员信息修改"""
    user = Driver.query.filter_by(uuid=g.user.uuid).first_or_404()
    form = forms.DriverEditForm(user=user).validate_()
    user.set_attrs(form.data).direct_update_()
    Redis.delete(form.redis_key)
    return result_format()
