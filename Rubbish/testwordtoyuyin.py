
from mutagen.mp3 import MP3

import pygame as pygame
import requests


API_KEY = ''
SECRET_KEY = ''


FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
TTS_URL = 'http://tsn.baidu.com/text2audio'
TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'
SCOPE = 'audio_tts_post'

def fetch_token(api_key, secret_key):
    params = {
        'grant_type': 'client_credentials',
        'client_id': api_key,
        'client_secret': secret_key
    }
    response = requests.post(TOKEN_URL, data=params)
    result = response.json()
    if 'access_token' in result and 'scope' in result:
        if SCOPE not in result['scope'].split(' '):
            #raise DemoError('scope is not correct')
            pass
        return result['access_token']
    else:
        pass
        #raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

def text_to_speech(text, api_key, secret_key, per=3, spd=5, pit=5, vol=5, aue=3):
    token = fetch_token(api_key, secret_key)
    tex = text.encode('utf-8')
    params = {
        'tok': token, 'tex': tex, 'per': per, 'spd': spd,
        'pit': pit, 'vol': vol, 'aue': aue, 'cuid': '123456PYTHON',
        'lan': 'zh', 'ctp': 1
    }

    with requests.post(TTS_URL, data=params, stream=True) as response:
        if response.headers['content-type'].find('audio/') < 0:
            result_str = response.text
            print("tts api error: " + result_str)
            return None
        else:
            format_type = FORMATS[aue]
            save_file = 'result.' + format_type
            with open(save_file, 'wb') as of:
                for chunk in response.iter_content(chunk_size=1024):
                    of.write(chunk)
            print("result saved as: " + save_file)
            play_mp3(save_file)
            audio = MP3("semantic_kernel/语音对讲/result.mp3") #需要进行修改
            duration_in_seconds = audio.info.length
            return duration_in_seconds




def play_mp3(file_path):
    print("路径为:" + file_path)
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    #pygame.mixer.music.fadeout(1000)  # Fade out over 1000 milliseconds (1 second)
    pygame.mixer.quit()  # Close the mixer




