video_path=$1
ffmpeg -i $video_path.mp4 -ab 160k -ac 1 -ar 16000 -vn $video_path.wav
python google_stt.py $video_path.wav
