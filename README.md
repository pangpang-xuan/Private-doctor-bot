# **Private-doctor-bot**

基于离线大模型ChatGLM3-6B和在线API，langchain以及vllm加速，实现了LLM成为你的助手，快速可以让每一个人听到。

---

## 目录

* [介绍](README.md#介绍)
* [usage](README.md#usage)
  * [1.环境安装](README.md#环境安装)
  * [2.正常聊天](README.md#语音对讲)
  * [3.langchain本地知识库](README.md#离线知识库)
  * [4.langchain-agent](README.md#agent)
  * [5.vllm加速模型](README.md#vllm)
* [痛点](README.md#痛点)

## 介绍
💡使用语音唤醒技术，以及文字转语音，语音转文字，让大模型的回答不只是看，还有听

🤖️ 一种利用 langchain 思想实现的基于本地知识库的问答应用以及agent工具调用，实现助手的知识库化以及智能化。

🔥 使用市面上比较流行的vllm框架，对本项目进行模型的加速推理，实现单卡4090可能部署大基座模型

---
### 仓库迭代
- [2024/01] ``我们项目接触了vllm框架，并将vllm框架简单接入了项目``
- [2023/11] ``我们项目受到了ChatGLM3-6B官方仓库的启发开始了langchain的融合``
- [2023/10] ``我们将我们微调之后的本地模型投入项目的使用``
- [2023/07] ``我们项目调用api实现了语音对讲的功能，让文字可以进入耳朵``
- _后续我们将紧跟LLM的发展进一步,进行功能的完善添加_

---
## usage

### 环境安装
+ 运行环境
```
python=3.10 cuda=11.8 torch=2.1
```
+ 安装依赖
```
git clone https://github.com/jayofhust/Private-doctor-bot.git
pip install -r requirements.txt
```
+ 配置api-key与模型路径
```
语音对讲文件夹中的hey_siri.py
PICOVICE_APIKEY=""              #申请方式在https://picovoice.ai/
```
```
Rubbish文件夹中的kedatest.py
wsParam = Ws_Param(APPID='', 
      APIKey='',APISecret='')   #可以在科大讯飞的官网进行申请
```
```
Rubbish文件夹中的testwordtoyuyin.py
API_KEY = ''
SECRET_KEY = ''                 #可以在百度官网进行申请
```
```
Rubbish文件夹中的chat_all_tasks.py
ZhipuAI_api_key=""              #可以去智谱AI官网(https://open.bigmodel.cn/)进行申请
语音对讲文件夹中的hey_siri.py
qwen_api=""                     #可以去https://account.aliyun.com/ 进行申请
```
```
大语言模型以及embedding模型路径，知识库文件路径
语音对讲文件夹中的hey_siri.py
model_path=""                   #切换成本地大模型路径
embedding_path=""               #切换成本地向量模型路径
file_path="data/data.txt"       #切换成本地txt知识库路径
```
### 语音对讲
+ 启动语音对讲里面的主入口hey_siri.py
+ 选择调用api还是本地大模型配置不同的LLm初始化
+ 在Rubbish文件夹里面kedatest.py选择想要的chat函数
+ 实现了用户不说话6s自动关闭 再次使用的话需要重新唤醒大白（若修改，到kedatest.py进行适合自己的参数修改）
```bash
cd 语音对讲
python hey_siri.py
```
### 离线知识库
+ _**data文件夹存放着本地知识库，本项目本地知识库只支持txt文件**_
+ data文件夹中提供各种格式转txt的代码，请根据自己的文件格式自行进行转换
+ samples 为转换样例
+ 在server文件提供Qwen和ChatGLM3-6B本地两种使用方式为例
+ _**自行更换hey_siri.py文件中的LLM加载方式以及kedatest文件中的chat函数**_
### agent
+ 在Agent_Tools子文件夹Tools加入自定义的功能函数
  + 一定要在函数中实现 **_run** 函数
+ 调用函数时候可以进行单工具和多工具，自定义工具和系统工具的加载
+ _**自行更换hey_siri.py文件中的LLM加载方式以及kedatest文件中的chat函数**_
### vllm
关于vllm的注意事项请移步：[vllm加速模型](vllm/README.md)

## 痛点

+ **import时候，自行删除semantic_kernel**
+ **文字转语音的时候输出字数如果过长的话，将无法转为语音进行播放**
+ **langchain_agent有可能模型有的时候不能很好的进行理解，有的时候无法进行function calling**
+ **vllm对于模型的加速本项目测试阶段只在服务器上面运行，不知道对于电脑的Linux效果如何**







