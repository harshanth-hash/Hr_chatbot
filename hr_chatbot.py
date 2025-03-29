from IPython import get_ipython
from IPython.display import display
# %%
import os
from groq import Groq
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from sentence_transformers import SentenceTransformer
import gradio as gr
import traceback

# Step 1: Set up Groq API environment
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

print("Starting script...")

# Helper functions
def call_groq_chat(prompt):
    print(f"Calling Groq API with prompt: {prompt[:100]}...")
    try:
        completion = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        response = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            print(f"Chunk received: {content}")
            response += content
        if not response:
            print("No response content received from Groq API")
            return "Sorry, I couldn’t generate a response. Please try again."
        print(f"Groq response: {response}")
        return response
    except Exception as e:
        print(f"Error calling Groq API: {str(e)}")
        return f"Error: Unable to get a response from the API ({str(e)}). Please try again or consult an HR representative."

# Step 2: Load documents
def load_documents():
    pdf_path = "nestle_hr_policy.pdf"
    print(f"Loading PDF from {pdf_path}...")
    if not os.path.exists(pdf_path):
        print(f"PDF not found at {pdf_path}")
        raise FileNotFoundError(f"PDF file not found at {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from PDF")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks

# Step 3: Create vector store with real embeddings
class RealEmbeddings:
    def __init__(self):
        print("Loading sentence-transformer model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Sentence-transformer model loaded")

    def embed_documents(self, texts):
        print(f"Embedding {len(texts)} documents...")
        # Access the text content directly using 'text' instead of 'text.page_content'
        embeddings = [self.model.encode(text) for text in texts]  
        print("Documents embedded")
        return embeddings

    def embed_query(self, text):
        print(f"Embedding query: {text[:50]}...")
        embedding = self.model.encode(text)
        print("Query embedded")
        return embedding

# Initialize vector store with detailed debugging
print("Initializing vector store...")
vector_store = None
try:
    # Step 3.1: Load and split documents
    chunks = load_documents()
    print(f"Loaded {len(chunks)} document chunks")

    # Step 3.2: Initialize embeddings
    embeddings = RealEmbeddings()
    print("Embeddings class initialized")

    # Step 3.3: Create Chroma vector store
    print("Creating Chroma vector store...")
    vector_store = Chroma.from_documents(chunks, embeddings)
    print("Vector store initialized successfully")
except Exception as e:
    print(f"Error initializing vector store: {str(e)}")
    print("Full stack trace:")
    traceback.print_exc()
    # Raise the exception to stop execution, remove this if you want to continue:
    raise e

# Step 4: Chatbot logic
prompt_template = """
You are an AI-powered HR Assistant for Nestlé. Use the following HR policy information to answer the user's question accurately and professionally. If the answer is not found in the provided documents, say so politely and suggest consulting an HR representative.

Context: {context}
Question: {question}

Answer:
"""

def chatbot(query, chat_history):
    print(f"Chatbot received query: {query}")
    if vector_store is None:
        print("Vector store is None")
        return "Error: Vector store not initialized.", chat_history
    retriever = vector_store.as_retriever()
    relevant_docs = retriever.get_relevant_documents(query)
    print(f"Retrieved {len(relevant_docs)} relevant documents")
    context = "\n".join([doc.page_content for doc in relevant_docs])
    print(f"Context: {context[:200]}...")
    prompt = prompt_template.format(context=context, question=query)
    response = call_groq_chat(prompt)
    chat_history.append((query, response))
    return response, chat_history

# Step 5: Gradio interface
def gradio_chatbot(query, history):
    print(f"Gradio processing query: {query}")
    response, updated_history = chatbot(query, history if history else [])
    print(f"Gradio response: {response}")
    chat_display = response if response else "No response generated."
    return chat_display, updated_history

# Launch Gradio interface
print("Launching Gradio interface...")
interface = gr.Interface(
    fn=gradio_chatbot,
    inputs=[gr.Textbox(label="Ask a question about Nestlé's HR policies"), gr.State()],
    outputs=[gr.Textbox(label="HR Assistant Response"), gr.State()],
    title="Nestlé HR Assistant Chatbot",
    description="Ask questions about Nestlé's HR policies."
)

# Use share=True for Colab to get a public URL
interface.launch(share=True)