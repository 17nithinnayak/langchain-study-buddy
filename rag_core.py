import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

def create_rag_chain(pdf_path: str, model_name: str = "llama3-8b-8192") -> RetrievalQA:
    """
    Creates and returns a RetrievalQA chain from a given PDF document.
    """
    print("Loading document for RAG chain...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    print("Splitting document...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)
    
    print("Creating embeddings and vector store...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embeddings)
    
    print("Initializing LLM...")
    llm = ChatGroq(temperature=0, model=model_name)
    
    print("Creating RAG chain...")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(),
    )
    print("RAG chain created successfully.")
    return qa_chain