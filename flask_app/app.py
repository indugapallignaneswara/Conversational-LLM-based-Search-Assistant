
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from utils import search_article_urls, fetch_single_article_content, concatenate_content, generate_answer

# Load environment variables from .env file
load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    """
    Endpoint to process a user query, search for articles, fetch content, and generate an answer.
    """
    data = request.get_json()
    query = data.get("query", "")
    
    # Step 1: Search for relevant article URLs
    urls = search_article_urls(query)
    if not urls:
        return jsonify({"error": "No URLs found for the query."}), 404
    
    # Step 2: Concatenate content from the URLs
    content = concatenate_content(urls)
    
    # Step 3: Generate an answer using the concatenated content and the query
    answer = generate_answer(content, query)
    
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host='localhost', port=5001)


