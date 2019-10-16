import datetime
from flask import g, request
from views.business import api
from plugins.HYplugins.common.authorization import login


@api.route('/driver/order/list/')
@login()
def driver_order_list():
    """驾驶员订单列表
    只展示已经处理完成的订单或已取消的订单
    :return:
    """
    #
    # schedule = request.args.get('schedule', type=int, default=None)
    #
    # page = request.args.get('page', default=1, type=int)
    # limit = 10
    #
    # # 筛选当前用户数据
    # query = DriverOrder.query.filter_by(user_id=g.user['id']).filter(DriverOrder.driver_schedule > 4)
    #
    # # 筛选订单进度
    # if schedule:
    #     query = query.filter(DriverOrder.driver_schedule == schedule)
    #
    # # 排序,进度最少,最新
    # query = query.order_by(DriverOrder.driver_schedule, DriverOrder.id.desc())
    #
    # # 分页数据
    # paginate = query.paginate(page=page, per_page=limit, error_out=True)
    #
    # # 序列化当前页数据
    #
    # items = [item.serialization(remove={'driver_schedule', 'images'},
    #                             funcs=[('order_infos', tuple(), dict())]) for item in paginate.items]
    #
    # # 封装分页数据
    # data = common.paginate_info(paginate=paginate, items=items)
    #
    # return common.result_format(data=data)


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