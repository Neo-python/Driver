import wtforms
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired, Optional
from plugins.HYplugins.form import BaseForm, ListPage
from plugins.HYplugins.form.fields import IdSortField
from plugins.HYplugins.form.validators_message import ValidatorsMessage as VM


class AcceptOrder(BaseForm, ListPage, IdSortField):
    """驾驶员接单"""
