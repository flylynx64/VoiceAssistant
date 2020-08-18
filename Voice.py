from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import playsound
import speech_recognition as sr 
from gtts import gTTS
import subprocess
import wolframalpha #GH3P6E-3T45T6446U Test1
from selenium import webdriver
import webbrowser
import requests
import json
import math as m
import speedtest
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import copy

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october","november", "december"]
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
dayExten = ["st", "nd", "rd", "th"]

WAappID = "GH3P6E-3T45T6446U" #wolframalpha
OWMappID = "9144b4e98289658a7eed0a55a622e987" #open weather map
count = 0
SID = "d0ed361606ec4bc9b73f513ddbe768aa"
 
# text to speech
def speak(text):
	tts = gTTS(text = text, lang = "en")
	global count
	filename = "voice" + str(count) + ".mp3"
	count += 1
	tts.save(filename)
	playsound.playsound(filename)

# get input audio and convert to string
def getAudio():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		audio = r.listen(source)
		said = ""
		try:
			said = r.recognize_google(audio)
			print(said)
		except Exception as e:
			 print("Exception: " + str(e))
	return said

# open a certain program using subprocess
def openProgram(text):
	word = text.split()[1]
	if word == "chrome":
		chrome = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
		subprocess.Popen([chrome])
	elif word == "spotify": #doesn't work "cannot find file specified"
		spotify = r"C:\Users\flyly\Desktop\Spotify.exe"
		subprocess.Popen([spotify])
	elif word == "discord": #doesn't work "not recognized as command"
		discord = r"C:\Users\flyly\AppData\Local\Discord\app.exe"
		subprocess.Popen([discord], shell = True)
	elif word == "val": #doesn't work "Access is denied"
		valorant = r"C:\Riot Games\VALORANT\live\VALORANT.exe"
		subprocess.Popen([valorant], shell = True)
	elif word == "minecraft":
		minecraft = r"C:\Program Files (x86)\Minecraft Launcher\MinecraftLauncher.exe"
		subprocess.Popen([minecraft])
	elif word == "stardew":
		stardew = r"C:\Program Files (x86)\Steam\steamapps\common\Stardew Valley\Stardew Valley.exe"
		subprocess.Popen([stardew])
	elif word == "hearthstone":
		hearthstone = r"C:\Program Files (x86)\Battle.net\Battle.net.exe"
		subprocess.Popen([hearthstone])

# open a certain file
def openFile(text):
#def find_files(filename, search_path):
	filename = ""
	for word in text.split():
		if word == "open" or word == "file":
			continue
		else:
			filename = filename + word
	print(filename)
	search_path = r"C:\Users\flyly\Documents"
	result = []
	for root, dir, files in os.walk(search_path):
		x = copy.deepcopy(files)
		for file in x:
			file = file.lower()
		if filename in x:
			i = x.index(filename)
			result.append(os.path.join(root, files[i]))
	subprocess.Popen(["C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", result[0]])

# make a note using speech to text
def note(text):
	index = text.split().index("note")
	note = text.split()[index + 1:]
	text1 = " ".join(note)
	date = datetime.datetime.now()
	file_name = str(date).replace(":", "-") + "-note.txt"
	with open(file_name, "w") as f:
		f.write(text1)
	subprocess.Popen(["notepad.exe", file_name])

# open chrome and google an input
def google(text):
	#driver = webdriver.Chrome("C:\Program Files\CDriver\chromedriver.exe")
	#driver.maximize_window()
	index = text.split().index("google")
	query = text.split()[index + 1:]
	url = "https://www.google.com/search?q=" + '+'.join(query)
	print(url)
	webbrowser.open_new_tab(url)
	#driver.get("https://www.google.com/search?q=" + '+'.join(query))

# use wolframalpha api to search a query
def search(text):
	client = wolframalpha.Client(WAappID)
	result = client.query(text)
	speak(next(result.results).text)

# split a word into character list
def spell(text):
	index = text.split().index("spell")
	word = text.split()[index + 1]
	return list(word)

# poll internet speed
def internet(text):
	st = speedtest.Speedtest()
	servernames = []
	st.get_servers(servernames)
	ping = round(st.results.ping, 2)
	dl = round(st.download()/1000000, 2)
	up = round(st.upload()/1000000, 2)
	print("Ping: " + str(ping) +"\nDownload Speed: " + str(dl) + "\nUpload Speed: " + str(up))
	if dl > 100:
		print("Internet is fast")
	else:
		print("Internet is slow")

# play a song using spotify
def spotify(text):
	scope = "user-library-read"
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
	results = sp.current_user_saved_tracks()
	for idx, item in enumerate(results['items']):
		track = item['track']
		print(idx, track['artists'][0]['name'], " – ", track['name'])

# return string of weather of a certain location
def weather(text):
	if text.count("in") > 0:
		index = text.split().index("in")
		query = text.split()[index + 1:]
		base_url = "http://api.openweathermap.org/data/2.5/weather?"
		complete_url = base_url + "appid=" + OWMappID + "&q=" + query[0]
	if text.count("today") > 0 or text.count("today's") > 0:
		base_url = "http://api.openweathermap.org/data/2.5/weather?"
		complete_url = base_url + "appid=" + OWMappID + "&q=katy"
	response = requests.get(complete_url)
	data = json.loads(response.text)
	curr_temp = round(data["main"]["temp"] * 9 / 5 - 459.67)
	feel = round(data["main"]["feels_like"] * 9 / 5 - 459.67)
	cond = data["weather"][0]["description"]
	temp_max = round(data["main"]["temp_max"] * 9 / 5 - 459.67)
	temp_min = round(data["main"]["temp_min"] * 9 / 5 - 459.67)
	out = "The current temperature is " + str(curr_temp) + " while it feels like " + str(feel) + ". The high for today will be " + str(temp_max) + " and the low will be " + str(temp_min) + ". Current conditions are " + str(cond) + "."
	return out

# authentication for google calendar
def authenticateGoogle():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

#def getEvents(n, service):
# get events from google calendar
def getEvents(service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    '''if n == 1:
    	print('Getting the upcoming event')
    elif n > 1:
    	print(f'Getting the upcoming {n} events')
    else:
    	print("Not a valid number")
    	return'''
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        speak(event['summary'])

# parse a date from speech
def getDate(text):
	text = text.lower()
	currentDate = datetime.date.today()
	if text.count("today") > 0:
		return currentDate
	day = -1
	DoW = -1
	month = -1
	year = currentDate.year

	for word in text.split():
		if word in months:
			month = months.index(word) + 1
			print(month)
		elif word in days:
			DoW = days.index(word)
		elif word.isdigit():
			day = int(word)
		else: 
			for ext in dayExten:
				found = word.find(ext)
				if found > 0:
					try:
						day = int(word[:found])
					except:	
						pass
	if month < currentDate.month and month != -1:
		year = year + 1
	if day < currentDate.day and month != -1 and day != -1:
		month = month + 1
	if month == -1 and day == -1 and DoW != -1:
		currentDoW = currentDate.weekday()
		diff = DoW - currentDoW
		if diff < 0 :
			diff += 7
			if text.count("next") >= 1:
				diff += 7
		return currentDate + datetime.timedelta(diff)
	return datetime.date(month = month, day = day, year = year) 

def main():
	global count
	count = 0
	while(True):
		speak("Hello. Choose speech or text.")
		text = "text" #getAudio().lower()
		if text == "speech":
			speak("What would you like to do?")
			text = getAudio().lower()
			print(text)
		elif text == "text":
			speak("What would you like to do?")
			text = input("What would you like to do?\n")
		if text.count("stop") > 0:
			break
		if text.count("open") > 0:
			if text.count("file") > 0:
				openFile(text)
			else:
				openProgram(text)
		elif text.count("events") > 0:
			speak("Your events are")
			getEvents(authenticateGoogle())
		elif text.count("note") > 0:
			note(text)
		elif text.count("google") > 0:
			google(text)
		elif text.count("weather") > 0:
			out = weather(text)
			print(out)
			speak(out)
		elif text.count("spell") > 0:
			out1 = spell(text)
			for i in out1:
				speak(str(i))
		elif text.count("speed") > 0:
			internet(text)
		elif text.count("listen") > 0:
			spot(text)
		else:
			search(text)

if __name__ == '__main__':
	main()
