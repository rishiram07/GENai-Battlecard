import requests
import json
import os
import spacy

# Initialize SpaCy NLP model
nlp = spacy.load('en_core_web_sm')

# Load API keys from a file
def load_api_keys():
    with open('data/api_keys.json') as f:
        return json.load(f)

# Perform a search using NewsAPI
def newsapi_search(query, api_key):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    response = requests.get(url)
    return response.json()

# Save collected data to a JSON file
def save_data_to_json(data, filename='collected_data.json'):
    os.makedirs('output', exist_ok=True)  # Create 'output' directory if it doesn't exist
    filepath = os.path.join('output', filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filepath}")

# Extract products from NewsAPI data
def extract_products(news_data):
    products = []
    for article in news_data.get('articles', []):
        doc = nlp(article.get('title', ''))
        for ent in doc.ents:
            if ent.label_ in ['PRODUCT']:
                products.append(ent.text)
    return products

# Extract market trends from NewsAPI data
def extract_market_trends(news_data):
    trends = []
    for article in news_data.get('articles', []):
        doc = nlp(article.get('title', ''))
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT']:
                trends.append(ent.text)
    return trends

# Extract and organize competitor details, products, and market trends
def extract_competitor_details(competitor_data, keyword_data):
    organized_data = {}
    
    for competitor, data in competitor_data.items():
        news_data = data.get('newsapi', {})
        
        organized_data[competitor] = {
            'details': news_data,
            'products': extract_products(news_data),
            'market_trends': []
        }
        
        for keyword, news_data in keyword_data.items():
            trends = extract_market_trends(news_data.get('newsapi', {}))
            if trends:
                organized_data[competitor]['market_trends'].append({
                    'keyword': keyword,
                    'trends': trends
                })
    
    return organized_data

# Collect data using different APIs
def collect_data(competitor_names, industry_keywords):
    # Load API keys
    api_keys = load_api_keys()
    
    data = {}
    
    # Collect data using NewsAPI for competitors
    competitor_data = {}
    for name in competitor_names:
        competitor_data[name] = {
            'newsapi': newsapi_search(name, api_keys['newsapi'])
        }
    
    # Collect data from NewsAPI for industry trends
    keyword_data = {}
    for keyword in industry_keywords:
        keyword_data[keyword] = {
            'newsapi': newsapi_search(keyword, api_keys['newsapi'])
        }
    
    # Save the collected data to a JSON file
    save_data_to_json({
        'competitor_data': competitor_data,
        'keyword_data': keyword_data
    })
    
    # Extract and organize relevant details
    organized_details = extract_competitor_details(competitor_data, keyword_data)
    
    # Save the organized details to a JSON file
    save_data_to_json(organized_details, filename='organized_details.json')
    
    return organized_details

# Example usage
if __name__ == "__main__":
    competitors = ["Apple", "Samsung", "Google`", "Vivo"]
    keywords = ["Smartphones", "Artificial Intelligence", "Consumer Electronics"]
    details = collect_data(competitors, keywords)
    print(json.dumps(details, indent=4))