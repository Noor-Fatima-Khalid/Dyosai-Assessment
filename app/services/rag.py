import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class RAGPipeline:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        # Use HuggingFaceEmbeddings with all-MiniLM-L6-v2
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},  # Use 'cuda' if GPU is available
            encode_kwargs={'normalize_embeddings': True}
        )
        # Use Google GenAI for LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.vectorstore = self._init_vectorstore()

    def _load_docs(self):
        loader = DirectoryLoader(self.data_dir, glob="*.md", loader_cls=TextLoader)
        return loader.load()

    def _split_docs(self, docs):
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return splitter.split_documents(docs)

    def _init_vectorstore(self):
        docs = self._load_docs()
        split_docs = self._split_docs(docs)
        return FAISS.from_documents(split_docs, self.embeddings)

    def retrieve(self, query: str, k=3):
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
        return retriever.invoke(query)

    def answer(self, query: str):
        # Check for ambiguity (e.g., too vague)
        if self._is_ambiguous(query):
            return {
                "final_answer": "",
                "sources": [],
                "classification": "AMBIGUOUS",
                "clarification_message": "Your query is too vague. Could you please provide more details?"
            }

        # Get the retriever object, do NOT invoke it yet
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

        # Check for unsupported queries (e.g., no relevant docs)
        docs = retriever.invoke(query)
        if not docs:
            return {
                "final_answer": "",
                "sources": [],
                "classification": "UNSUPPORTED",
                "clarification_message": "Sorry, I don't have enough information to answer your question."
            }

        # Proceed with normal RAG
        template = """
        Answer the question using only the following context:
        {context}
        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        answer = chain.invoke(query)
        sources = [doc.metadata["source"] for doc in docs]
        return {
            "final_answer": answer,
            "sources": sources,
            "classification": "ANSWERED",
            "clarification_message": None
        }

    def _is_ambiguous(self, query: str) -> bool:
        # Example: if query is less than 3 words, consider it ambiguous
        return len(query.split()) < 3