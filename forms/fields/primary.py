import wtforms
from wtforms.validators import DataRequired, Length
from plugins.HYplugins.form.validators_message import ValidatorsMessage as VM


class DriverNameField:
    """驾驶员名称字段"""
    name = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '驾驶员名称')),
        Length(max=10, message=VM.say('length', '驾驶员名称', 1, 10))
    ])


class NumberPlateField:
    """车牌号字段"""

    number_plate = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '车牌号')),
        Length(min=5, max=10, message=VM.say('length', '车牌号', 5, 10))
    ])
