from flask import Flask, render_template, request, Blueprint
from werkzeug.utils import secure_filename
from .main_views import bp

# 업로드 HTML 렌더링
@bp.route('/upload')
def render_file():
    return render_template('upload.html')

# 파일 업로드 처리
@bp.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # 저장할 경로 + 파일명
        f.save(secure_filename(f.filename))
        return 'uploads 디렉토리 -> 파일 업로드 성공'