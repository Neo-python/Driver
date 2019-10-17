from .HYModels import business


class Order(business.OrderBase):
    """厂家订单"""


class DriverOrder(business.DriverOrderBase):
    """驾驶员订单"""


class DriverOrderScheduleLog(business.DriverOrderScheduleLogBase):
    """驾驶员订单记录"""
