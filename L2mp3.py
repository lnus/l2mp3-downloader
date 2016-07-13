import os, time, shutil
from colorama import Fore
from pytube import YouTube
from pprint import pprint
import moviepy.editor as mp

def downloadVideo(url):
	global videoOnly
	#Settings
	yt = YouTube(url)
	print(Fore.LIGHTGREEN_EX + "[L2mp3] Found video: " + yt.filename)
	filename = yt.filename.replace("!", "")
	yt.set_filename(filename)

	#Sets the resolution
	resInfo = yt.filter("mp4")[-1]
	resSettings = ["1080p", "720p", "480p", "360p", "240p", "144p"]
	for i in resSettings:
		if i in str(resInfo): res = i
	print("[L2mp3] Trying to download in " + res + "...")
	video = yt.get("mp4", res)

	#Downloads the video
	try:
		video.download("Video/")
		if not videoOnly: 
			audioConvert(filename)
		else:
			videoOnly = False
			startSearch()
	except Exception as e:
		print(Fore.LIGHTRED_EX + "\a[L2mp3] File already in directory!")
		print(e)
		startSearch()

def audioConvert(filename):
	global audioOnly

	#Converts the video to an audio file
	clip = mp.VideoFileClip("Video/" + filename + ".mp4")
	clip.audio.write_audiofile("Audio/" + filename + ".mp3")
	clip = None
	time.sleep(0.5)

	#Deletes the video if "--a" is set to True
	if audioOnly: 
		os.remove("Video/" + filename + ".mp4")
		audioOnly = False

	#Returns user to interface	
	startSearch()

def startSearch():
	print("\n")
	global audioOnly, videoOnly
	#Prompts the user to enter an url
	try:
		dlUrl = input(Fore.LIGHTYELLOW_EX + "[L2mp3] URL> " + Fore.LIGHTBLACK_EX)
		if "--a" in dlUrl: 
			audioOnly = True
			dlUrl = dlUrl.replace("--a", "", 1)
		elif "--v" in dlUrl:
			videoOnly = True
			dlUrl = dlUrl.replace("--v", "", 1)
		dlUrl = dlUrl.replace(" ", "")	
		downloadVideo(dlUrl)
	except Exception as e:
		print(Fore.LIGHTRED_EX + "\a[L2mp3] Parsing error or URL does not exist...")
		startSearch()

if __name__ == "__main__":
	#Introduction
	print(Fore.LIGHTCYAN_EX + "Welcome L2mp3 donwloader!\n\n" +
			"To download only audio put '--a' after your URL.\n" +
			"To download only video put '--v' after your URL.\n" +
			"To download both, don't put any arguments.\n\n" +
			"Enjoy! :^)")

	#Some stupid arguments
	audioOnly = False
	videoOnly = False

	#Creates directories if they do not already exist
	if not os.path.exists("Video"):
		os.mkdir("Video")
	if not os.path.exists("Audio"):
		os.mkdir("Audio")

	#Starts the user interaction	
	startSearch()
