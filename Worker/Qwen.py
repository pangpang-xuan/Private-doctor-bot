import json
from copy import deepcopy

from langchain.llms.base import LLM
from transformers import AutoTokenizer, AutoModel, AutoConfig
from typing import List, Optional
from utils import tool_config_from_file
import dashscope


class Qwen(LLM):
    max_token: int = 8192
    do_sample: bool = False
    temperature: float = 0.8
    top_p = 0.8
    tokenizer: object = None
    model: object = None
    history: List = []
    tool_names: List = []
    has_search: bool = False
    api_key: str = None



    def __init__(self, api_key):
        super().__init__()
        self.api_key=api_key

    @property
    def _llm_type(self) -> str:
        return "Qwen"

    def _tool_history(self, prompt: str):
        ans = []
        tool_prompts = prompt.split(
            "You have access to the following tools:\n\n")[1].split("\n\nUse a json blob")[0].split("\n")

        tool_names = [tool.split(":")[0] for tool in tool_prompts]
        self.tool_names = tool_names
        tools_json = []
        for i, tool in enumerate(tool_names):
            tool_config = tool_config_from_file(tool)
            if tool_config:
                tools_json.append(tool_config)
            else:
                ValueError(
                    f"Tool {tool} config not found! It's description is {tool_prompts[i]}"
                )

        ans.append({
            "role": "system",
            "content": "Answer the following questions as best as you can. You have access to the following tools:",
            "tools": tools_json
        })
        query = f"""{prompt.split("Human: ")[-1].strip()}"""
        return ans, query

    def _extract_observation(self, prompt: str):
        return_json = prompt.split("Observation: ")[-1].split("\nThought:")[0]
        self.history.append({
            "role": "observation",
            "content": return_json
        })
        return

    def _extract_tool(self):
        if len(self.history[-1]["metadata"]) > 0:
            metadata = self.history[-1]["metadata"]
            content = self.history[-1]["content"]
            if "tool_call" in content:
                for tool in self.tool_names:
                    if tool in metadata:
                        input_para = content.split("='")[-1].split("'")[0]
                        action_json = {
                            "action": tool,
                            "action_input": input_para
                        }
                        self.has_search = True
                        return f"""
Action: 
```
{json.dumps(action_json, ensure_ascii=False)}
```"""
        final_answer_json = {
            "action": "Final Answer",
            "action_input": self.history[-1]["content"]
        }
        self.has_search = False
        return f"""
Action: 
```
{json.dumps(final_answer_json, ensure_ascii=False)}
```"""

    def _call(self, prompt: str, history: List = [], stop: Optional[List[str]] = ["<|user|>"], role: str = "user"):
        print("======输入======")
        print(prompt)
        print("===============")
        if self.history is None:
            self.history = []
        if not self.has_search:
            self.history, query = self._tool_history(prompt)
        else:
            self._extract_observation(prompt)
            query = ""


        self.history.append({"role": role, "content": query})
        # print("============")
        # print(self.history)
        # print("============")


        messages = [{'role': role, 'content': query}]
        # print(messages)
        # print(">>>>>信息<<<<<<")

        swap = dashscope.Generation.call(
            dashscope.Generation.Models.qwen_turbo,
            messages=messages,
            api_key=self.api_key,
            # set the random seed, optional, default to 1234 if not set
            result_format='message',  # set the result to be "message" format.
        )
        # print(swap) 使用 json.loads() 方法把 JSON 字符串转换成 Python 字典
        obj = json.loads(str(swap))
        # 使用点号或者方括号来访问字典的键，找到 content 键的值
        response= "\n "+obj["output"]["choices"][0]["message"]["content"]

        _, self.history = self.process_response(response, self.history)

        response = self._extract_tool()
        history.append((prompt, response))
        return response

    def process_response(self, output, history):
        content = ""
        history = deepcopy(history)
        for response in output.split("<|assistant|>"):
            metadata, content = response.split("\n", maxsplit=1)
            if not metadata.strip():
                content = content.strip()
                history.append({"role": "assistant", "metadata": metadata, "content": content})
                content = content.replace("[[训练时间]]", "2023年")
            else:
                history.append({"role": "assistant", "metadata": metadata, "content": content})
                if history[0]["role"] == "system" and "tools" in history[0]:
                    content = "\n".join(content.split("\n")[1:-1])
                    def tool_call(**kwargs):
                        return kwargs
                    parameters = eval(content)
                    content = {"name": metadata.strip(), "parameters": parameters}
                else:
                    content = {"name": metadata.strip(), "content": content}
        return content, history


