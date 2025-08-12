from flask import Flask, request, render_template
from transformers import pipeline
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Initialize Hugging Face sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Function to fetch news article text (simulating data pipeline)
def fetch_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        article_text = ' '.join([p.get_text() for p in paragraphs])
        return article_text[:1000]  # Limit to 1000 characters for demo
    except Exception as e:
        return f"Error fetching article: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    sentiment_result = None
    input_text = ""
    
    if request.method == 'POST':
        input_type = request.form.get('input_type')
        
        if input_type == 'url':
            url = request.form.get('url')
            input_text = fetch_article_text(url)
        else:
            input_text = request.form.get('text')
        
        # Analyze sentiment
        if input_text and not input_text.startswith("Error"):
            result = sentiment_analyzer(input_text)
            sentiment_result = {
                'label': result[0]['label'],
                'score': round(result[0]['score'], 4)
            }
    
    return render_template('index.html', sentiment_result=sentiment_result, input_text=input_text)

if __name__ == '__main__':
    app.run(debug=True)
