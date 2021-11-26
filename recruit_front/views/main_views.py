from flask import Blueprint, render_template

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def employee():
    return render_template('employee.html')

@bp.route('/employer')
def employer():
    return render_template('employer.html')

@bp.route('/company1')
def company1():
    return render_template('company1.html')

@bp.route('/company2')
def company2():
    return render_template('company2.html')

@bp.route('/company1-1')
def company1_1():
    return render_template('company1-1.html')
