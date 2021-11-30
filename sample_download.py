from pytube import YouTube
import os.path 
import ffmpeg 
from getpass import getuser 

class tube:
    def __init__(self, link):
        self.parent_dir = "/Users/hyunn/Allen_WIP/competitions/ai_idea/recruit/REC-ruit/"
        self.yt = YouTube(link)

    def getVideoName(self):
        name = self.yt.title
        return name

    def my(self):
        stream = self.yt.streams.filter(only_audio=True).first()
        stream.download(self.parent_dir)

    def downloadMp3(self):
        stream = self.yt.streams.filter(only_audio=True).first()
        stream.download(self.parent_dir)
        src = stream.default_filename 
        dst = stream.default_filename[0:-3] + 'mp3' 
       
        ffmpeg.input(os.path.join(self.parent_dir, src)).output(os.path.join(self.parent_dir, dst)).run(overwrite_output=True)

        os.remove(os.path.join(self.parent_dir, src))
        return dst 

    def downloadMp4(self):
        audio = self.downloadMp3() 
        video = self.yt.streams.filter(adaptive=True, file_extension='mp4', fps = 30).first()
        print(video)
        video.download(self.parent_dir) 
 
        inputAudio = ffmpeg.input(os.path.join(self.parent_dir, audio))
        inputVideo = ffmpeg.input(os.path.join(self.parent_dir, video.default_filename))
        ffmpeg.output(inputAudio, inputVideo, os.path.join(self.parent_dir, "new.mp4"), vcodec='copy', acodec='aac').run(overwrite_output=True)
        os.remove(os.path.join(self.parent_dir, video.default_filename))
        os.remove(os.path.join(self.parent_dir, audio))
        os.rename(os.path.join(self.parent_dir, "new.mp4"),
            os.path.join(self.parent_dir, video.default_filename))
            
        return video.default_filename

test = tube('https://www.youtube.com/watch?v=vVfO_QPQFjQ')
test.my()