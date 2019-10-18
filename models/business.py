from .HYModels import business


class Order(business.OrderBase):
    """厂家订单"""
    _privacy_fields = {'factory_uuid', 'status', 'id'}


class DriverOrder(business.DriverOrderBase):
    """驾驶员订单"""


class DriverOrderScheduleLog(business.DriverOrderScheduleLogBase):
    """驾驶员订单记录"""


class OrderEntrust(business.OrderEntrustBase):
    """订单委托"""

    def order_info(self, result: dict, orders: dict, *args, **kwargs):
        """加入订单信息"""
        result.update({'order_info': orders[self.order_uuid]})
