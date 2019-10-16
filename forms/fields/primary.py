import wtforms
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired, Optional
from plugins.HYplugins.form.validators_message import ValidatorsMessage as VM





class FactoryNameField:
    """驾驶员名称字段"""
    name = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '驾驶员名称')),
        Length(max=50, message=VM.say('length', '驾驶员名称', 1, 50))
    ])
