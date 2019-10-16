import wtforms
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired, Optional
from init import Redis
from forms.fields.primary import *
from plugins.HYplugins.form import BaseForm
from plugins.HYplugins.form.fields import PhoneField, CodeField, OpenIdField


class RegisteredForm(BaseForm, PhoneField, CodeField, DriverNameField, NumberPlateField, OpenIdField):
    """注册"""

    def validate_code(self, *args):
        """验证手机验证码"""
        phone = self.phone.data
        self.redis_key = f'validate_phone_registered_{phone}'
        if self.code.data == Redis.get(self.redis_key):
            return True
        else:
            raise wtforms.ValidationError(message='code error')


class DriverEditForm(BaseForm, PhoneField, DriverNameField, NumberPlateField):
    """信息修改"""

    code = wtforms.StringField(validators=[Optional(), Length(min=4, max=4, message=VM.say('length_unite', '验证码', 4))])

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def validate_phone(self, *args):
        """验证手机验证码"""
        phone = self.phone.data
        self.redis_key = f'validate_phone_edit_phone_{self.user.phone}'
        if self.user.phone != phone:
            if self.code.data == Redis.get(self.redis_key):
                return True
            else:
                raise wtforms.ValidationError(message='code error')
        else:
            return True