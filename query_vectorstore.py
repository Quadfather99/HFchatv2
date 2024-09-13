import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Initialize OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def load_vectorstore():
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    return vectorstore

def setup_qa_chain(vectorstore):
    llm = ChatOpenAI(temperature=0.7, model_name="gpt-4", openai_api_key=OPENAI_API_KEY)
    
    # Custom prompt template
    prompt_template = """
    You are an engaging and helpful AI assistant for HyperFocus Consulting. Your goal is to provide valuable information about our services and ultimately encourage users to submit their contact information for a personalized consultation. Remember these key points:

    1. Be friendly, professional, and enthusiastic about HyperFocus Consulting's services.
    2. Highlight the benefits of working with HyperFocus Consulting.
    3. If the user shows interest, suggest they provide their contact information for a free consultation.
    4. Don't be pushy, but look for opportunities to mention the value of speaking with a HyperFocus consultant.
    5. Use the following pieces of context to answer the human's questions:
    {context}

    Current conversation:
    {chat_history}
    Human: {question}
    AI Assistant: Let me help you with that!
    """
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "chat_history", "question"]
    )
    
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": PROMPT}
    )
    return qa_chain

def main():
    print("Loading vector store...")
    vectorstore = load_vectorstore()
    
    print("Setting up QA chain...")
    qa_chain = setup_qa_chain(vectorstore)
    
    print("Welcome to HyperFocus Consulting's AI Assistant! How can I help you today?")
    while True:
        query = input("\nYou: ")
        if query.lower() in ['quit', 'exit', 'bye']:
            print("AI: Thank you for your interest in HyperFocus Consulting. If you'd like to learn more or schedule a consultation, please visit our website or provide your contact information. Have a great day!")
            break
        
        result = qa_chain({"question": query})
        print(f"\nAI: {result['answer']}")

if __name__ == "__main__":
    main()