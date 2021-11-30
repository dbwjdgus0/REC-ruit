from flask import Blueprint, render_template, request  # request : 파일 업로드를 위해 사용
from werkzeug.utils import secure_filename             # secrue_filename : 업로드할 파일이 실제 시스템에 저장되기 전 이름을 보호하기 위해 사용
import os                                              # 용량 제한 단위는 바이트임에 유의하자, 즉 다음 예제코드는 16MB 용량을 최대 제한으로 둔다.
                                                       # app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 16MB

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

@bp.route('/company1-2')
def company1_2():
    return render_template('company1-2.html')

@bp.route('/manage1')
def manage1():
    return render_template('manage1.html')


# 파일 리스트
@bp.route('/list')
def list_page():
	file_list = os.listdir("aidea/templates/uploads/")
	html = """<center><a href="/">홈페이지</a><br><br>"""
	html += "file_list: {}".format(file_list) + "</center>"
	return html

# 업로드 HTML 렌더링
@bp.route('/company_upload')
def company_upload():
    return render_template('company_upload.html')


# 파일 업로드 처리
@bp.route('/fileUpload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        upload = request.files.getlist("file[]")
        for f in upload:
        # 저장할 경로 + 파일명
            f.save('aidea/templates/uploads/' + secure_filename(f.filename))
    return render_template('upload_check.html')