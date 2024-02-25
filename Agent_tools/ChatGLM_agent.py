from semantic_kernel.Agent_tools.Tools.Weather import Weather
from semantic_kernel.Worker.ChatGLM3 import ChatGLM3
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent, load_tools


class ChatGLM_agent():

    def __init__(self, api_key, model_path):
        super().__init__()
        self.api_key = api_key
        self.model_path = model_path
        self.llm = ChatGLM3().load_model(model_name_or_path=self.model_path)
        self.prompt=hub.pull("hwchase17/structured-chat-agent")



    def chat(self, query):

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

        return response






