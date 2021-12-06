from flask import Blueprint, render_template, request  # request : 파일 업로드를 위해 사용
from werkzeug.utils import secure_filename             # secrue_filename : 업로드할 파일이 실제 시스템에 저장되기 전 이름을 보호하기 위해 사용
import os                                              # 용량 제한 단위는 바이트임에 유의하자, 즉 다음 예제코드는 16MB 용량을 최대 제한으로 둔다.
import subprocess
#import text_to_summary
                  # app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 16MB

bp = Blueprint('main', __name__, url_prefix='/')
file_list = []
text = ""
summed_text = ""
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
    
    #요약
    #키워드?
    global file_list
    global text
    #test = '/Users/hyunn/Allen_WIP/competitions/ai_idea/recruit/REC-ruit/recruit_front/static/recording_h'
    subprocess.call(f"python /Users/hyunn/Allen_WIP/competitions/ai_idea/recruit/REC-ruit/KorBertSum/src/text_to_summary.py < {file_list[0]+'.txt'}", shell=True)
    #subprocess.call(f"python /Users/hyunn/Allen_WIP/competitions/ai_idea/recruit/REC-ruit/recruit_front/static/KorBertSum/src/text_to_summary.py < {test+'.txt'}", shell=True)
    
    #summed = text_to_summary.main(text)
    #print(summed)
    return render_template('manage1.html', file_list=file_list, text=text)

@bp.route('/manage2')
def manage2():

    

    return render_template('manage2.html', file_list=file_list)

@bp.route('/upload_check2.html')
def upload_check():
    return render_template('upload_check2.html', file_list=file_list)


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
            fname = '/Users/hyunn/Allen_WIP/competitions/ai_idea/recruit/REC-ruit/recruit_front/static/' + secure_filename(f.filename)
            f.save(fname)
            file_list.append(secure_filename(f.filename)[:-4])
        print(file_list)
        
        subprocess.call(f'ffmpeg -i {fname} -ab 160k -ac 1 -ar 16000 -vn {fname[:-4]}.wav', shell=True)

        #여기서 음성인식
        #cmd = "/Users/hyunn/Allen_WIP/competitions/ai_idea/recruit/REC-ruit/recruit_front/video_to_text.sh " #+ fname 
        #cmd = "/Users/hyunn/Allen_WIP/competitions/ai_idea/recruit/REC-ruit/recruit_front/views/static/video_to_text.sh " #+ fname[:-4]
        #cmd = '../static/video_to_text.sh'
        #print(cmd)
        #subprocess.call([cmd])
        global text 
        text = transcribe_file(fname[:-4] +'.wav').strip()
        text_path = fname[:-4]+'.txt'
        with open(text_path, 'w') as f:
            f.write(text)

        subprocess.call(f"python /Users/hyunn/Allen_WIP/competitions/ai_idea/recruit/REC-ruit/recruit_front/static/KorBertSum/src/text_to_summary.py < {text_path}", shell=True)


    return render_template('upload_check.html',
                            text = text)



import sys
import os
import re
from google.cloud import speech
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/hyunn/Downloads/gcp_key.json"

# [START speech_transcribe_async]
def transcribe_file(speech_file):

    client = speech.SpeechClient()

    # [START speech_python_migration_async_request]
    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ko-KR",
    )

    # [START speech_python_migration_async_response]
    operation = client.long_running_recognize(config=config, audio=audio)
    # [END speech_python_migration_async_request]

    #print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    res = ""
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        res += result.alternatives[0].transcript + " "

    return res
        #print("Confidence: {}".format(result.alternatives[0].confidence))
    # [END speech_python_migration_async_response]

# [END speech_transcribe_async]

# def test_transcribe(capsys):
#     transcribe_file(os.path.join(RESOURCES, "audio.raw"))
#     out, err = capsys.readouterr()

#     assert re.search(r"how old is the Brooklyn Bridge", out, re.DOTALL | re.I)

# RESOURCES = os.path.join(os.path.dirname(__file__), "resources")
