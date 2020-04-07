from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    # default 200 code 넘긴다.
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    # default 200 code 넘긴다.
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    # default 200 code 넘긴다.
    return render_template('errors/500.html'), 500