import os, time
from colorama import Fore
from pytube import YouTube

class Downloader():
    def __init__(self):
        # Makes the dirs
        if not os.path.exists("Video"):
            os.system("Video")
        if not os.path.exists("Audio"):
            os.system("mkdir Audio")

        # Mainloop
        self.start_search()

    def download_video(self,url):
        # Settings
        yt = YouTube(url)
        print("Found video: " + yt.filename)
        filename = yt.filename.replace("!", "").replace("&","").replace(" ","-")

        # Finds the correct resolution
        res_info = yt.filter("mp4")[-1]
        res_settings = ["1080p", "720p", "480p", "360p", "240p", "144p"]
        for i in res_settings:
            if i in str(res_info): res = i
        print("Found video resolution: " + res)    
        video = yt.get("mp4", res)
        
        # Downloads the video in the correct resolution
        video.download("Video/"+filename+".mp4")
        
        # Gets the audio
        self.audio_convert(filename)

    def audio_convert(self, filename):
        # Converts a video to an mp3 file using FFmpeg
        os.system("ffmpeg -i {} {}".format("Video/"+filename+".mp4", "Audio/"+filename+".mp3"))

    def start_search(self):        
        while True:
            dl_url = input("Video URL: ")
            self.download_video(dl_url)

if __name__ == "__main__":
    d = Downloader()
