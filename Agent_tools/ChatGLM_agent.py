from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.vectorstores.faiss import FAISS

from semantic_kernel.Worker.ChatGLM3 import ChatGLM3
from semantic_kernel.Worker.Qwen import Qwen
from semantic_kernel.Rubbish.testwordtoyuyin import text_to_speech, API_KEY, SECRET_KEY


class ChatGLM_agent():

    def __init__(self, api_key, file_path, embedding_path, model_path):
        super().__init__()
        self.api_key = api_key
        self.file_path = file_path
        self.embedding_path = embedding_path
        self.model_path = model_path
        self.llm = ChatGLM3().load_model(model_name_or_path=self.model_path)



    def chat(self, query):

        print("....")

        text_to_speech(response, API_KEY, SECRET_KEY)






