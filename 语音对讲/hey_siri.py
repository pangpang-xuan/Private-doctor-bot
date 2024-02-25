import os
import struct

import pvporcupine
import pyaudio
import pygame
import requests
from mutagen.mp3 import MP3

from semantic_kernel.Agent_tools.Qwen_agent import Qwen_agent
from semantic_kernel.Rubbish.testwordtoyuyin import fetch_token, TTS_URL, FORMATS, play_mp3
from semantic_kernel.server.Qwen_llm import Qwen_llm


def here(text, api_key, secret_key, per=3, spd=5, pit=5, vol=5, aue=3):
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
            save_file = 'here.' + format_type
            with open(save_file, 'wb') as of:
                for chunk in response.iter_content(chunk_size=1024):
                    of.write(chunk)
            print("result saved as: " + save_file)
            if os.path.exists(save_file):
                play_mp3(save_file)
                audio = MP3(save_file)
                duration_in_seconds = audio.info.length
                return duration_in_seconds
            else:
                print("File not found:", save_file)
                return None

def play_mp3(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue





PICOVICE_APIKEY=""
embedding_path="E:\ChatGLM3-6B\embedding\\bge-large-zh"
file_path="data/data.txt"
qwen_api=""

# 本地知识库的llm
LLm=Qwen_llm(api_key=qwen_api,file_path=file_path,embedding_path=embedding_path)

# agent的llm
#LLm=Qwen_agent(api_key=qwen_api)

pvporcupine=pvporcupine.create(
    access_key=PICOVICE_APIKEY,
    keyword_paths=['F:\pythonProject1\semantic_kernel\语音对讲\da-bai-da-bai_en_windows_v2_2_0.ppn'], #这个地方需要修改为自己的路径
)
myaudio=pyaudio.PyAudio()
stream = myaudio.open(
    input_device_index=0,
    rate=pvporcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=pvporcupine.frame_length
)


while True:
    audio_obj=stream.read(pvporcupine.frame_length,exception_on_overflow=False)
    audio_obj_unpacked=struct.unpack_from("h"*pvporcupine.frame_length,audio_obj)

    keyword_idx=pvporcupine.process(audio_obj_unpacked)
    if keyword_idx>=0:
        '''here("我在",API_KEY, SECRET_KEY)'''
        play_mp3("F:\pythonProject1\semantic_kernel\语音对讲\here.mp3") # 这个地方需要进行修改为自己当前的路径
        from semantic_kernel.Rubbish.kedatest import run
        run()   #调用的是Rubbish中的kedatest.py



