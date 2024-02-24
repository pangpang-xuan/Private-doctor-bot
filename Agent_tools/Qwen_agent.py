from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.vectorstores.faiss import FAISS
from semantic_kernel.Worker.Qwen import Qwen
from semantic_kernel.Rubbish.testwordtoyuyin import text_to_speech, API_KEY, SECRET_KEY

class Qwen_agent():

    def __init__(self,api_key,file_path,embedding_path):
        super().__init__()
        self.api_key=api_key
        self.file_path=file_path
        self.embedding_path=embedding_path
        self.llm=Qwen(api_key=api_key)



    def chat(self,query):

        qa = RetrievalQA.from_chain_type(self.llm, chain_type="stuff", retriever=self.retriever)

        response = qa.run(query)

        print(response)

        text_to_speech(response, API_KEY, SECRET_KEY)






