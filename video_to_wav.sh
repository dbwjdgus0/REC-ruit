video_path=$1
ffmpeg -i $video_path.mp4 -ab 160k -ac 2 -ar 44100 -vn $video_path.wav
