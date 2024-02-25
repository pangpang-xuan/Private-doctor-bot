from semantic_kernel.Agent_tools.Tools.Weather import Weather
from semantic_kernel.Worker.Qwen import Qwen
from semantic_kernel.Rubbish.testwordtoyuyin import text_to_speech, API_KEY, SECRET_KEY
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent, load_tools

class Qwen_agent():

    def __init__(self,api_key):
        super().__init__()
        self.api_key=api_key
        self.llm=Qwen(api_key=api_key)
        self.prompt=hub.pull("hwchase17/structured-chat-agent")



    def chat(self,query):


        # 调用模块的仓库
        # tools = load_tools(["arxiv"], llm=self.llm)
        # agent = create_structured_chat_agent(llm=self.llm, tools=tools, prompt=self.prompt)
        # agent_executor = AgentExecutor(agent=agent, tools=tools)
        # ans = agent_executor.invoke({"input": "Describe the paper about GLM 130B"})
        # response = ans['output']

        # 使用自定义函数
        tools = [Weather()]
        agent = create_structured_chat_agent(llm=self.llm, tools=tools, prompt=self.prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools)
        ans = agent_executor.invoke({"input": query})
        response = ans['output']
        text_to_speech(response, API_KEY, SECRET_KEY)


        text_to_speech(response, API_KEY, SECRET_KEY)






