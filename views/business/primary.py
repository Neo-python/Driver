from flask import g, request
from views.business import api
from models.business import OrderEntrust, Order, DriverOrder
from forms import business as forms
from plugins.HYplugins.common.authorization import login
from plugins.HYplugins.common.ordinary import orm_func, join_key
from plugins.HYplugins.common.ordinary import result_format, paginate_info


@api.route('/factory/order/list/')
@login()
def factory_order_list():
    """厂家订单列表
    司机可以接的订单列表
    :return:
    """
    user = g.user
    form = forms.AcceptOrderListForm(request.args).validate_()

    query = OrderEntrust.query.filter_by(driver_uuid=user.uuid)

    if form.create_time_sort is not None:
        if form.create_time_sort.data == 0:
            query = query.order_by(OrderEntrust.id.desc())

    paginate = query.paginate(form.page.data, form.limit.data, error_out=False)

    orders = Order.query.filter(Order.order_uuid.in_([item.order_uuid for item in paginate.items])).all()
    orders = join_key('order_uuid', orders)

    remove = {'order_uuid'}
    funcs = [orm_func('batch_order_info', orders=orders)]
    data = paginate_info(paginate, items=[item.serialization(funcs=funcs, remove=remove) for item in paginate.items])

    return result_format(data=data)


@api.route('/order/accept/')
@login()
def order_accept():
    """接受订单"""
    user = g.user
    form = forms.AcceptOrderForm(formdata=request.args, user_uuid=user.uuid).validate_()
    form.entrust.entrust_status = 1
    OrderEntrust.query.filter(OrderEntrust.id != form.entrust.id).update({OrderEntrust.entrust_status: -1})
    OrderEntrust.static_commit_()

    DriverOrder(driver_uuid=user.uuid, factory_order_uuid=form.entrust.order_uuid)

    return result_format()


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
