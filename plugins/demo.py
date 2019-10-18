# 查询orm类名
from main import app
from models.business import OrderEntrust
app.app_context().push()

factory = OrderEntrust.query.first()

factory.order