import os
import logging
from dotenv import load_dotenv
import psycopg2
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database connection details
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def fetch_data_from_postgres():
    """Load scraped data from PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        logger.info("Successfully connected to the database")
        
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM website_data")
            count = cur.fetchone()[0]
            logger.info(f"Number of rows in website_data: {count}")
            
            cur.execute("SELECT url, content FROM website_data")
            rows = cur.fetchall()
        
        documents = [Document(page_content=row[1], metadata={"source": row[0]}) for row in rows]
        logger.info(f"Loaded {len(documents)} documents from PostgreSQL.")
        return documents
    except Exception as e:
        logger.error(f"Error loading data from PostgreSQL: {e}")
        return []
    finally:
        if conn:
            conn.close()

def create_vector_store(documents):
    """Create and populate the Chroma vector store."""
    try:
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory="./chroma_db"  # This line specifies where Chroma will store its files
        )
        vectorstore.persist()  # This line ensures the vectorstore is saved to disk
        logger.info(f"Vector store created and saved to ./chroma_db")
        return vectorstore
    except Exception as e:
        logger.error(f"Error creating vector store: {e}")
        return None

if __name__ == "__main__":
    documents = fetch_data_from_postgres()
    if documents:
        vectorstore = create_vector_store(documents)
        if vectorstore:
            logger.info("Vector store created successfully.")
            
            # Optional: Perform a test query
            query = "What services does HyperFocus Consulting offer?"
            results = vectorstore.similarity_search(query, k=2)
            logger.info("\nTest Query Results:")
            for doc in results:
                logger.info(f"Content: {doc.page_content[:100]}...")
                logger.info(f"Source: {doc.metadata['source']}\n")
        else:
            logger.error("Failed to create vector store.")
    else:
        logger.error("No data processed for vector store.")
