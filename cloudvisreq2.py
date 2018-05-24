from base64 import b64encode
from os import makedirs
from os.path import join, basename
from sys import argv
import json
import requests
import string
from subprocess import call
import os
from gtts import gTTS
URL = 'https://vision.googleapis.com/v1/images:annotate'
RESULTS_DIR = 'jsons'
makedirs(RESULTS_DIR, exist_ok=True)

def image_requests(imgname):
	"""imgname is the name of the given image file"""
	img_requests_text = []
	img_requests_label=[]
	with open(imgname, 'rb') as f:
		txt = b64encode(f.read()).decode()
		img_requests_text.append({
                    'image': {'content': txt},
                    'features': [{
                        'type': 'TEXT_DETECTION',
                        'maxResults': 1
                    }]
            })
	with open(imgname, 'rb') as f:
                txt = b64encode(f.read()).decode()
                img_requests_label.append({
                    'image': {'content': txt},
                    'features': [{
                        'type': 'LABEL_DETECTION',
                        'maxResults': 1
                    }]
            })
	return img_requests_text,img_requests_label




def get_response(api_key, image_filenames):
	"""Returns the response"""
	imgdict_text,imgdict_label = image_requests(image_filenames)
	"""The image data lists as bytes"""
	data_text=json.dumps({"requests": imgdict_text}).encode()
	data_label=json.dumps({"requests": imgdict_label}).encode()
	
	response_text = requests.post(URL,
                             data_text,
                             params={'key': api_key},
                             headers={'Content-Type': 'application/json'})
	response_label = requests.post(URL,
                             data_label,
                             params={'key': api_key},
                             headers={'Content-Type': 'application/json'})
	return response_text,response_label

def main():
	api_key, image_filenames = argv[1:]
	fin=open("text.txt","r+")
	fin.truncate()
	if not api_key or not image_filenames:
		print("""Please supply an api key, and an image file""")
	else:
		response,response1 = get_response(api_key, image_filenames)
		if response.status_code != 200 or response.json().get('error'):
			print(response.text)
		else:
			for idx,resp in enumerate(response.json()['responses']):
				print("-------------TEXT DETECTION------------------------------")
				try:
					t = resp['textAnnotations'][0]
					#print(resp['textAnnotations'][0])
					print(t['description'].strip())
					fin.write("Text detected is : ")
					fin.write(t['description'])
				except:
					print("TEXT IS NOT DETECTED IN THE IMAGE")
					fin.write("TEXT IS NOT DETECTED IN THE IMAGE") 
		if response1.status_code != 200 or response.json().get('error'):
			print(response1.text)
		else:
			print("-------------LABEL DETECTION-------------------------------")
			for idx,resp in enumerate(response1.json()['responses']):
				try:
					#print(resp['labelAnnotations'][0])
					t = resp['labelAnnotations'][0]
					print(t['description'])
					fin.write("Label detected is : ")
					fin.write(t['description'])
				except:
					print("LABEL IS NOT DETECTED IN THE IMAGE")
					fin.write(".LABEL  IS NOT DETECTED IN THE IMAGE")
		fin.close()
		f=open("text.txt","r")
		txt = f.read()
		tts = gTTS(text=txt, lang='en')
		tts.save("test.mp3")
		call(["vlc", "test.mp3"])
main()
