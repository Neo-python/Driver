from flask import jsonify
from init import create_app
from plugins.HYplugins.error import ViewException

app = create_app()


@app.route('/index/')
def index():
    return 'hello neo'


@app.errorhandler(ViewException)
def view_error(error):
    """视图错误"""
    return jsonify(error.info)


if __name__ == '__main__':
    app.run(port=8092, host='0.0.0.0', debug=True)