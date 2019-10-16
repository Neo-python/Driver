# 查询orm类名
from main import app
from models.HYModels.user import Factory
app.app_context().push()

factory = Factory.query.first()

print(factory.__class__.__name__)