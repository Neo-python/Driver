import datetime
from flask import g, request
from views.business import api
from plugins.HYplugins.common.authorization import login


@api.route('/factory/order/list/')
@login()
def factory_order_list():
    """厂家订单列表
    司机可以接的订单列表
    :return:
    """


@api.route('/order/accept/')
@login()
def order_accept():
    """接受订单"""


@api.route('/driver/order/checking/')
@login()
def driver_order_checking():
    """驾驶员订单检查"""
    # driver_order_id = request.args.get('driver_order_id', default=None, type=int)
    # driver_order = DriverOrder.query.filter_by(id=driver_order_id, user_id=g.user['id']).first_or_404()
    #
    # data = driver_order.serialization(remove={'driver_schedule'}, funcs=[('order_infos', tuple(), dict())])
    # return common.result_format(data=data)


@api.route('/driver/order/advance/', methods=['POST'])
@login()
def driver_order_advance():
    """驾驶员订单状态推进
    检查订单进度是否未达到已送达状态,并且不处于"已取消"的订单状态
    订单进度+1
    :return: 返回订单进度
    """
    # driver_order_id = request.get_json(force=True).get('driver_order_id')
    # driver_order = DriverOrder.query.with_for_update(of=DriverOrder).filter_by(id=driver_order_id,
    #                                                                            user_id=g.user['id']).first_or_404()
    # if driver_order.driver_schedule < 5:
    #     driver_order.driver_schedule = driver_order.driver_schedule + 1
    #     driver_order.direct_update_()
    #     return common.result_format(data={"driver_schedule": driver_order.driver_schedule})
    # else:
    #     return common.result_format(error_code=4011, message="订单进度无法推进!")


@api.route('/driver/order/cancel/', methods=['DELETE'])
@login()
def driver_order_cancel():
    """驾驶员订单取消
    修改驾驶员订单状态
    修改驾驶员订单进度
    "driver_order_receive_set"触发器将会:
    恢复厂家订单状态
    增加驾驶员订单状态日志
    :return:
    """
    # driver_order_id = request.args.get('driver_order_id', default=None, type=int)
    # driver_order = DriverOrder.query.filter_by(id=driver_order_id, user_id=g.user['id']).first_or_404()
    # driver_order.driver_schedule = 99
    # driver_order.direct_update_()
    # return common.result_format()
