import os
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import psycopg2
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv()

# Function to scrape website
def scrape_website(url):
    try:
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text from all paragraphs
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        
        # Split the text into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        docs = text_splitter.split_text(text)
        
        return [{"url": url, "content": doc} for doc in docs]
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

# Function to insert data into PostgreSQL
def insert_into_postgres(documents):
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    cur = conn.cursor()

    for doc in documents:
        cur.execute(
            "INSERT INTO website_data (url, content) VALUES (%s, %s)",
            (doc["url"], doc["content"])
        )

    conn.commit()
    cur.close()
    conn.close()

# Main execution
if __name__ == "__main__":
    # URL of the website you want to scrape
    url = "https://hyperfocusconsulting.ca"
    
    # Scrape the website
    scraped_docs = scrape_website(url)
    
    if scraped_docs:
        # Insert the scraped data into PostgreSQL
        insert_into_postgres(scraped_docs)
        print(f"Inserted {len(scraped_docs)} documents into the database.")
    else:
        print("No documents were scraped.")
