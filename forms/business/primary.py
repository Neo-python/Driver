import wtforms
from wtforms.validators import NumberRange, DataRequired
from models.business import Order
from plugins.HYplugins.form import BaseForm, ListPage, InputRequired
from plugins.HYplugins.form.fields import IdSortField, OrderUuidField
from plugins.HYplugins.form.validators_message import ValidatorsMessage as VM
from plugins.HYplugins.error import ViewException, FormException


class AcceptOrderListForm(BaseForm, ListPage, IdSortField):
    """厂家委托单列表"""


class AcceptOrderInfoForm(BaseForm, OrderUuidField):
    """订单详情"""

    def validate_order_uuid(self, *args):
        """检查订单编号"""

        self.order = Order.query.filter_by(order_uuid=self.order_uuid.data, schedule=0).first()

        if not self.order:
            raise ViewException(error_code=5110, message="订单状态发生改变,已无法查看,请刷新后重新尝试.")


class AcceptOrderForm(BaseForm, OrderUuidField):
    """驾驶员接单"""

    def validate_order_uuid(self, *args):
        """检查订单编号"""

        self.order = Order.query.with_for_update(read=False, of=Order).filter_by(order_uuid=self.order_uuid.data,
                                                                                 schedule=0).first()

        if not self.order:
            raise ViewException(error_code=5110, message="订单状态发生改变,已无法接单,请刷新后重新尝试.")


class OrderAdvanceForm(BaseForm, OrderUuidField):
    """订单跟进"""


class OrderCancelForm(BaseForm, OrderUuidField):
    """订单取消"""


class OrderInfoForm(BaseForm, OrderUuidField):
    """订单详情"""


class OrderListForm(BaseForm, ListPage):
    """订单列表"""

    order_status = wtforms.IntegerField(validators=[
        InputRequired(message=VM.say('required', '订单状态')),
        NumberRange(min=-1, max=2, message=VM.say('system_number', -1, 2))
    ])
