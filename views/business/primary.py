import config
from flask import g, request
from views import Order, DriverOrder
from views.business import api
from forms import business as forms
from plugins import core_api
from plugins.HYplugins.common.authorization import login
from plugins.HYplugins.common.ordinary import orm_func, join_key
from plugins.HYplugins.common.ordinary import result_format, paginate_info
from plugins.HYplugins.error import ViewException


@api.route('/factory/order/list/')
@login(verify_status={'status': True})
def factory_order_list():
    """厂家订单列表
    司机可以接的订单列表
    :return:
    """

    form = forms.AcceptOrderListForm(request.args).validate_()

    query = Order.query.filter_by(schedule=0)
    if form.create_time_sort is not None:
        if form.create_time_sort.data == 0:
            query = query.order_by(Order.id.desc())
    paginate = query.paginate(form.page.data, form.limit.data, error_out=False)

    data = paginate_info(paginate, items=[item.driver_serialization() for item in paginate.items])

    return result_format(data=data)


@api.route('/factory/order/info/')
@login(verify_status={'status': True})
def factory_order_info():
    """厂家订单详情
    :return:
    """

    form = forms.AcceptOrderInfoForm(request.args).validate_()

    return result_format(data=form.order.driver_serialization())


@api.route('/order/accept/')
@login(verify_status={'status': True})
def order_accept():
    """接受订单,绑定厂家订单"""

    form = forms.AcceptOrderForm(request.args).validate_()
    user = g.user

    # 更新订单状态
    form.order.schedule = 1
    # 生成驾驶员订单,生成驾驶员订单编号,迁移厂家订单信息
    driver_order = DriverOrder(driver_uuid=user.uuid, factory_order_uuid=form.order.order_uuid,
                               contact_phone=form.order.contact_phone).direct_flush_()
    # 绑定驾驶员订单编号
    form.order.driver_order_uuid = driver_order.order_uuid

    order_data = form.order.serialization(remove={'create_time', 'id', 'status', 'order_uuid'})

    driver_order.set_attrs(order_data)
    driver_order.direct_commit_()

    # 通知厂家
    core_api.send_sms(template_id=config.SMS_TEMPLATE_REGISTERED['driver_accept_order'],
                      phone=form.order.factory.phone, code=form.order.order_uuid)

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

    items = [item.serialization() for item in paginate.items]

    data = paginate_info(paginate, items=items)

    return result_format(data=data)


@api.route('/order/info/')
@login()
def order_info():
    """订单详情"""

    form = forms.OrderInfoForm(request.args).validate_()

    order = DriverOrder.query.filter_by(order_uuid=form.order_uuid.data, driver_uuid=g.user.uuid).first_or_404()

    return result_format(data=order.customize_serialization())


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
    if 4 > driver_order.driver_schedule > 0:
        driver_order.driver_schedule = driver_order.driver_schedule + 1
        driver_order.direct_update_()
        return result_format(data={"driver_schedule": driver_order.driver_schedule})
    elif driver_order.driver_schedule == 4:  # 订单完成,修改厂家订单状态
        driver_order.driver_schedule = 6
        driver_order.order.schedule = 2
        driver_order.direct_update_()
        return result_format(data={"driver_schedule": driver_order.driver_schedule}, message="订单已完成")
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
    # OrderEntrust.query.filter_by(order_uuid=driver_order.factory_order_uuid).update({OrderEntrust.entrust_status: 0})

    driver_order.direct_update_()
    return result_format()
