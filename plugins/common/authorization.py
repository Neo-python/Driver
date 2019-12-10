from flask import g
from plugins.HYplugins.error import ViewException


class LoginVerify:
    """login权限装饰器验证逻辑"""

    def demo(self, args):
        """示例验证逻辑"""
        raise Exception()

    def verify_status(self, status: bool):
        """检查驾驶员验证状态"""
        user = g.user
        if user.verify == status:
            return True
        else:
            raise ViewException(error_code=5011, message='您无此功能使用权限,请联系管理员开通.')
