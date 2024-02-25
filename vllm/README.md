# 使用vllm进行模型的加速
vLLM is a Python library that also contains pre-compiled C++ and CUDA (12.1) binaries.
## 环境需要
+ OS: Linux
+ Python: 3.8 – 3.11
+ GPU: compute capability 7.0 or higher (e.g., V100, T4, RTX20xx, A100, L4, H100, etc.)
## 下载
```bash
pip install vllm
```
+ 因为vllm库基于cuda12.1，但是有些环境cuda可能是11.8，可以通过下面的方式进行安装
```bash
# Install vLLM with CUDA 11.8.
export VLLM_VERSION=0.2.4
export PYTHON_VERSION=39
pip install https://github.com/vllm-project/vllm/releases/download/v${VLLM_VERSION}/vllm-${VLLM_VERSION}+cu118-cp${PYTHON_VERSION}-cp${PYTHON_VERSION}-manylinux1_x86_64.whl

# Re-install PyTorch with CUDA 11.8.
pip uninstall torch -y
pip install torch --upgrade --index-url https://download.pytorch.org/whl/cu118

# Re-install xFormers with CUDA 11.8.
pip uninstall xformers -y
pip install --upgrade xformers --index-url https://download.pytorch.org/whl/cu118
```
## 对于vllm加速模型可以进行OpenAI-Compatible Server和离线加速
### 对于离线加速的demo代码在offline.py中
### 对于OpenAI-Compatible Server加速
+ 打开server
```bash
python -m vllm.entrypoints.openai.api_server \
    --model facebook/opt-125m
```
可以通过访问本地8000端口进行调用
```bash
curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "facebook/opt-125m",
        "prompt": "San Francisco is a",
        "max_tokens": 7,
        "temperature": 0
    }'
```
python代码在Rubbish/chat_all_tasks.py中进行展示
