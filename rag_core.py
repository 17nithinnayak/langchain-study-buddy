import os
from dotenv import load_dotenv

# --- SETUP ---
# This line MUST be at the top to load the API key from the .env file
load_dotenv()

# Updated imports to fix the deprecation warnings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

# 1. LOAD THE DOCUMENT
print("Loading document...")
loader = PyPDFLoader("my_document.pdf")
documents = loader.load()
print(f"Loaded {len(documents)} page(s) from the document.")

# 2. SPLIT THE DOCUMENT INTO CHUNKS
print("Splitting document into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
docs = text_splitter.split_documents(documents)
print(f"Split document into {len(docs)} chunks.")

# 3. CREATE EMBEDDINGS AND STORE IN VECTOR DB
print("Creating embeddings and storing in FAISS Vector DB...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_documents(docs, embeddings)
print("Vector DB created successfully.")

# 4. INITIALIZE THE LLM
print("Initializing LLM with Groq...")
llm = ChatGroq(
    api_key = os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192",
    temperature=0.1
    )
print("LLM initialized.")

# 5. CREATE THE RETRIEVALQA CHAIN
print("Creating RetrievalQA chain...")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": 2}),
    
)
print("Chain created.")


query = "What are the properties of a Binary Search Tree?"
print(f"\nQuerying the chain with: '{query}'")
result = qa_chain.invoke({"query": query})


print("\n--- Answer ---")
print(result["result"])