import config
from flask import g, request
from init import core_api
from views import OrderEntrust, Order, DriverOrder
from views.business import api
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

    query = OrderEntrust.query.filter_by(driver_uuid=user.uuid, entrust_status=0)

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
    entrust = form.entrust

    # 更新委托记录状态
    entrust.entrust_status = 1
    OrderEntrust.query.filter(OrderEntrust.id != form.entrust.id).update({OrderEntrust.entrust_status: -1})
    OrderEntrust.static_commit_()

    # 生成驾驶员订单,生成驾驶员订单编号,迁移厂家订单信息
    driver_order = DriverOrder(driver_uuid=user.uuid, factory_order_uuid=entrust.order_uuid).direct_flush_()
    data = entrust.order.serialization()
    data.pop('create_time', '')
    data.pop('id', '')
    data.pop('status', '')
    data.pop('order_uuid', '')
    driver_order.set_attrs(data)

    # 记录驾驶员订单编号
    entrust.order.driver_order_uuid = driver_order.order_uuid
    entrust.order.schedule = 1

    driver_order.direct_commit_()

    core_api.batch_sms(template_id=config.SMS_TEMPLATE_REGISTERED['driver_accept_order'],
                       phone_list=[entrust.order.factory.phone, entrust.managers.phone],
                       params=[entrust.order_uuid]
                       )

    return result_format()


@api.route('/order/list/')
@login()
def order_list():
    """订单列表"""
    form = forms.OrderListForm(request.args).validate_()

    order_status = form.order_status.data

    query = DriverOrder.query.filter_by(driver_uuid=g.user.uuid)

    if order_status == -1:
        query = query.filter(DriverOrder.driver_schedule == -1)

    elif order_status == 0:
        # 查询全部订单
        pass

    elif order_status == 1:
        # 订单正在处理中
        query = query.filter(DriverOrder.driver_schedule > 0, DriverOrder.driver_schedule < 6)

    elif order_status == 2:
        # 订单已完成
        query = query.filter(DriverOrder.driver_schedule == 6)

    paginate = query.paginate(page=form.page.data, per_page=form.limit.data, error_out=False)

    items = [item.serialization(funcs=[('order_infos', tuple(), dict())]) for item in paginate.items]

    data = paginate_info(paginate, items=items)

    return result_format(data=data)


@api.route('/order/info/')
@login()
def order_info():
    """订单详情"""

    form = forms.OrderInfoForm(request.args).validate_()

    order = DriverOrder.query.filter_by(order_uuid=form.order_uuid.data, driver_uuid=g.user.uuid).first_or_404()

    data = order.serialization(funcs=[('order_infos', tuple(), dict())])
    return result_format(data=data)


@api.route('/order/advance/', methods=['POST'])
@login()
def order_advance():
    """驾驶员订单状态推进
    检查订单进度是否未达到已送达状态,并且不处于"已取消"的订单状态
    订单进度+1
    :return: 返回订单进度
    """

    form = forms.OrderAdvanceForm().validate_()

    driver_order = DriverOrder.query.with_for_update(of=DriverOrder).filter_by(order_uuid=form.order_uuid.data,
                                                                               driver_uuid=g.user.uuid).first_or_404()
    if driver_order.driver_schedule < 5:
        driver_order.driver_schedule = driver_order.driver_schedule + 1
        driver_order.direct_update_()
        return result_format(data={"driver_schedule": driver_order.driver_schedule})
    else:
        return result_format(error_code=5200, message="订单进度无法推进!")


@api.route('/order/cancel/', methods=['DELETE'])
@login()
def order_cancel():
    """驾驶员订单取消
    修改驾驶员订单状态
    修改驾驶员订单进度
    恢复委托订单所有驾驶员订单的接待状态为0
    "driver_order_receive_set"触发器将会:
    恢复厂家订单状态
    增加驾驶员订单状态日志
    :return:
    """
    form = forms.OrderCancelForm(request.args).validate_()

    driver_order = DriverOrder.query.filter_by(order_uuid=form.order_uuid.data, driver_uuid=g.user.uuid).first_or_404()
    driver_order.driver_schedule = -1

    # 恢复委托订单所有驾驶员订单的接待状态为0
    OrderEntrust.query.filter_by(order_uuid=driver_order.factory_order_uuid).update({OrderEntrust.entrust_status: 0})

    driver_order.direct_update_()
    return result_format()
