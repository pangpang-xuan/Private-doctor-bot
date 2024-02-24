import threading

import numpy as np
import pyaudio
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime

from semantic_kernel.Rubbish.chat_all_tasks import *

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


stopnums = 0  # 确保在函数外部定义stopnums为一个全局变量
status=0



class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"domain": "iat", "language": "zh_cn", "accent": "mandarin", "vinfo":1,"vad_eos":10000}

    # 生成url
    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url


# 收到websocket消息的处理
def on_message(ws, message):
    try:
        code = json.loads(message)["code"]
        sid = json.loads(message)["sid"]
        if code != 0:
            errMsg = json.loads(message)["message"]
            print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))

        else:
            data = json.loads(message)["data"]["result"]["ws"]
            # print(json.loads(message))
            result = ""
            for i in data:
                for w in i["cw"]:
                    result += w["w"]
            print("翻译结果: %s" % (result))
            chat_langchain(result)
            # chat_usual(result)
            #openagain()
            #print("sid:%s call success!,data is:%s" % (sid, json.dumps(data, ensure_ascii=False)))
    except Exception as e:
        print("receive msg,but parse exception:", e)



# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws, a, b):
    global stopnums,status

    print("### closed ###")
    if status == 0: # 表示没有说话，无效计时+1
        stopnums += 1

    if stopnums != 3:
        print("### 重新连接 ###")
        print("现在重连的次数为："+str(stopnums))
        thread_obj = threading.Thread(target=run)
        thread_obj.start()
    else:
        stopnums=0

    status=0 #关闭时候复原

def openagain(ws,*args):
    print("### 重连 ###")
    # 添加重连逻辑
    thread_obj = threading.Thread(target=run())
    thread_obj.start()



# 收到websocket连接建立的处理
def on_open(ws):
    def run(*args):
        try:
            global result
            status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧
            CHUNK = 520  # 定义数据流块
            FORMAT = pyaudio.paInt16  # 16bit编码格式
            CHANNELS = 1  # 单声道
            RATE = 16000  # 16000采样频率
            p = pyaudio.PyAudio()
            # 创建音频流
            stream = p.open(format=FORMAT,  # 音频流wav格式
                            channels=CHANNELS,  # 单声道
                            rate=RATE,  # 采样率16000
                            input=True,
                            frames_per_buffer=CHUNK)

            first_iteration = True  # 判断是否为第一次迭代
            SILENCE_THRESHOLD = 1000  # 你可以根据实际情况调整这个值

            print("- - - - - - - Start Recording ...- - - - - - - ")

            silent_count = 0  # 没有声音的计数器
            max_silent_count = int(RATE / CHUNK * 2)  # 最大无声音计数，例如1秒

            for i in range(0, int(RATE / CHUNK * 20)):  # 一次识别20s
                buf = stream.read(CHUNK)
                if not buf:
                    status = STATUS_LAST_FRAME
                # 获取音量
                data = np.frombuffer(buf, dtype=np.int16)
                volume = np.max(np.abs(data))

                if volume < SILENCE_THRESHOLD:
                    silent_count += 1
                    if silent_count > max_silent_count:
                        print("没声音了")
                        break
                else:
                    silent_count = 0
                if status == STATUS_FIRST_FRAME:
                    try:
                        d = {"common": wsParam.CommonArgs,
                             "business": wsParam.BusinessArgs,
                             "data": {"status": 0, "format": "audio/L16;rate=16000",
                                      "audio": str(base64.b64encode(buf), 'utf-8'),
                                      "encoding": "raw"}}
                        d = json.dumps(d)
                        ws.send(d)
                        status = STATUS_CONTINUE_FRAME
                    except Exception as e:
                        print("Error in sending audio data:", e)
                        break
                    # 中间帧处理
                elif status == STATUS_CONTINUE_FRAME:
                    try:
                        d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                      "audio": str(base64.b64encode(buf), 'utf-8'),
                                      "encoding": "raw"}}
                        ws.send(json.dumps(d))
                    except Exception as e:
                        print("Error in sending audio data:", e)
                        break


                # 最后一帧处理
                elif status == STATUS_LAST_FRAME:
                    try:
                        d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                      "audio": str(base64.b64encode(buf), 'utf-8'),
                                      "encoding": "raw"}}
                        ws.send(json.dumps(d))
                        time.sleep(1)  # 说话截止停顿时间
                        break
                    except Exception as e:
                        print("Error in sending audio data:", e)
                        break

            stream.stop_stream()
            stream.close()
            p.terminate()
            ws.close()
        except Exception as e:
            print("Error in run():", e)

        # thread.start_new_thread(run, ())
    thread_obj = threading.Thread(target=run)
    thread_obj.start()


def run():
    global wsParam
    global result
    # 测试时候在此处正确填写相关信息即可运行
    time1 = datetime.now()
    wsParam = Ws_Param(APPID='', APIKey='',
                       APISecret='')
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    time2 = datetime.now()
    print(time2 - time1)



if __name__ == "__main__":
    run()
