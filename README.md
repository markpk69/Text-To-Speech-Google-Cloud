# Text-To-Speech-Google-Cloud
A Text to Speech to Audiofile using Google Cloud's library written using python. 

I  couldn't find any text to speech's that allowed large files that didn't cost money so I create a simple one to solve that problem. 

Google does still limit it,Here is the quotas: https://cloud.google.com/text-to-speech/quotas

# Installation
[Setup a Google Cloud account](https://console.cloud.google.com/) then Go To Console and create a new project, then [Add Text to Speech](https://console.cloud.google.com/speech/text-to-speech) to your project.

[Install Google Clound CLI](https://cloud.google.com/sdk/docs/install).

Follow these instructions to [Setup Google Cloud and TTS](https://cloud.google.com/text-to-speech/docs/libraries).

[Install python 3.12](https://www.python.org/downloads/release/python-3127/) and be sure to check Add To Path during installation.

Run powershell as admin and input 
```
pip install --upgrade google-cloud-texttospeech
pip install tkinter 
pip install requests
pip install charset-normalizer
```

Run python idle as Admin and File-new file(Ctrl+N) paste code from 

[Text to Speech GUI.py](https://github.com/markpk69/Text-To-Speech-Google-Cloud/blob/496486fe762e9a4879206e6bd29a02c67f7508b5/Text%20to%20Speech%20GUI.py)

Enjoy!
There is some farts between the meshing of the audio files, but not annoying.
