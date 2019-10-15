import wtforms
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired, Optional
from init import Redis
from forms.fields.main import *
from plugins.HYplugins.form import BaseForm
from plugins.HYplugins.form.fields import PhoneField


class SMSCodeForm(BaseForm, PhoneField):
    """短信发送表单"""
    genre = wtforms.SelectField(validators=[DataRequired()],
                                choices=[('registered', 'registered'), ('edit_phone', 'edit_phone')])
