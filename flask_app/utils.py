
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai
import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Retrieve API keys
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def search_article_urls(query):
    """
    Searches for articles related to the query using the Serper API.
    Returns a list of URLs.
    """
    formatted_query = urllib.parse.quote_plus(query)
    url = f"https://google.serper.dev/search?q={formatted_query}&apiKey={SERPER_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print("Error fetching URLs:", response.status_code, response.text)
            return []

        search_results = response.json().get("organic", [])
        urls = [result.get("link") for result in search_results if result.get("link")]
        return urls
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def fetch_single_article_content(url):
    """
    Fetches the article content from a single URL, extracting relevant text only.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all(["h1", "h2", "p"])]
        content = " ".join(paragraphs)
        return content[:15000]  # Limit to avoid token issues
    except Exception as e:
        print(f"Error fetching content from {url}: {e}")
        return ""

def concatenate_content(urls):
    """
    Fetches and concatenates content from each URL into a single string.
    """
    contents = []
    for url in urls:
        content = fetch_single_article_content(url)
        if content:
            contents.append(content)
    return " ".join(contents)

def generate_answer(content, query):
    """
    Generates an answer from the concatenated content using GPT-3.5-turbo.
    """
    prompt = f"Context: {content}\nAnswer the question: {query}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )

    return response.choices[0].message['content'].strip()


