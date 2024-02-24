from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.vectorstores.faiss import FAISS
from semantic_kernel.Worker.Qwen import Qwen
from semantic_kernel.Rubbish.testwordtoyuyin import text_to_speech, API_KEY, SECRET_KEY

class Qwen_llm():

    def __init__(self,api_key,file_path,embedding_path):
        super().__init__()
        self.api_key=api_key
        self.file_path=file_path
        self.embedding_path=embedding_path
        self.llm=Qwen(api_key=api_key)

        # ----------------------------------------加载本地知识库------------------------------------
        loader = UnstructuredFileLoader(file_path=self.file_path)
        docs = loader.load()
        # 文件分割
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=200)
        docs = text_splitter.split_documents(docs)
        # 构建向量数据库
        model_kwargs = {'device': 'cuda:0'}
        encode_kwargs = {'normalize_embeddings': True}  # set True to compute cosine similarity
        embedding = HuggingFaceBgeEmbeddings(
            model_name=self.embedding_path,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )
        db = FAISS.from_documents(docs, embedding)
        self.retriever = db.as_retriever()

    def chat(self,query):

        qa = RetrievalQA.from_chain_type(self.llm, chain_type="stuff", retriever=self.retriever)

        response = qa.run(query)

        print(response)

        text_to_speech(response, API_KEY, SECRET_KEY)






