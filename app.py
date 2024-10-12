from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS to handle cross-origin requests
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


def spacy_sentiment(text):
    # Load SpaCy's small English model
    nlp = spacy.load("en_core_web_sm")
    # Add the SpacyTextBlob component to the pipeline
    nlp.add_pipe("spacytextblob")
    # Process the text
    doc = nlp(text)
    
    # Filter out stop words, special characters, and meaningless words (words not recognized by SpaCy)
    word_sentiments = {
        token.text: token._.blob.polarity 
        for token in doc 
        if not token.is_stop and token.is_alpha and token.pos_ not in ["X", "SYM", "PUNCT"]
    }
    
    # Calculate overall sentiment polarity of the entire text
    overall_polarity = doc._.blob.polarity
    return overall_polarity, word_sentiments


@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.get_json()

    if not text or 'query' not in text:
        return jsonify({'error': 'No text provided'}), 400  # Handle missing key

    sentiment = sentiment_analyzer.spacy_sentiment(text['query'])
    return jsonify({'sentiment': sentiment[0], 'word_sentiment' :sentiment[1]})

if __name__ == '__main__':
    app.run(port=5000)
