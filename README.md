# HyperFocus Consulting AI Chatbot

This project implements an AI-powered chatbot for HyperFocus Consulting, designed to answer questions about the company's services and encourage lead generation.

## Project Structure

- `scrape_and_populate.py`: Scrapes the HyperFocus Consulting website and populates a PostgreSQL database with the content.
- `create_vectorstore.py`: Creates a vector store from the scraped data for efficient querying.
- `query_vectorstore.py`: Implements the chatbot logic, allowing users to interact with the AI assistant.

## Setup

1. Clone the repository:
   ```
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```
   DB_HOST=<your-db-host>
   DB_PORT=<your-db-port>
   DB_NAME=<your-db-name>
   DB_USER=<your-db-user>
   DB_PASSWORD=<your-db-password>
   OPENAI_API_KEY=<your-openai-api-key>
   ```

4. Run the scraping and population script:
   ```
   python scrape_and_populate.py
   ```

5. Create the vector store:
   ```
   python create_vectorstore.py
   ```

6. Start the chatbot:
   ```
   python query_vectorstore.py
   ```

## Usage

After starting the chatbot, you can interact with it by typing questions or statements. The AI will respond based on the information from the HyperFocus Consulting website.

## Deployment

This project is set up to be deployed on Render. Connect your GitHub repository to Render and set up the environment variables in the Render dashboard.

## Contributing

For any improvements or issues, please open an issue or submit a pull request.
