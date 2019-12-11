import config
from flask import jsonify
from plugins import create_app
from plugins.HYplugins.error import ViewException

app = create_app()


@app.route('/index/')
def index():
    return 'hello neo'


@app.errorhandler(ViewException)
def view_error(error):
    """视图错误"""
    return jsonify(error.info)


@app.errorhandler(500)
def server_error(error):
    """服务器错误"""
    return jsonify({"error_code": 5099, "message": "服务器出现异常,请联系管理员.", "system_message": str(error)})


if __name__ == '__main__':
    app.run(port=config.server_port, debug=True)
