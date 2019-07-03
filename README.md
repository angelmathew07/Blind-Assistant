The project aims to provide a comprehensive set of assistance features to aid a visually impaired person by converting the image characteristics to a sound pattern. The system uses Google Cloud Vision API and Google Text-to-Speech (gTTS). The Google Cloud Vision API detects a broad set of objects in the image, from flowers, animals and other object categories commonly found within images. In addition, it also performs Optical Character Recognition (OCR) and detects text within the image, along with automatic language identification. The extracted objects and texts in the image are stored in a file. gTTS is a Python library and CLI tool to interface with Google Translate’s text-to-speech API. It converts the text stored in the file to audio data and saves it to an mp3 file.When the input file in jpg, jpeg, png or gif format is given, the labels and text in the image are extracted and displayed on the CLI, moreover, it is also stored on a text file. The contents of the text file are converted to audio data and saved to an mp3 file by gTTS.The mp3 file is then played by calling vlc player.

FINAL CODE : cloudvisreq2.py

To run the project: python cloudvisreq2.py <google api key> <image file>
