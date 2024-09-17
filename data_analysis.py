import json
import spacy
from collections import defaultdict

# Initialize SpaCy NLP model
nlp = spacy.load('en_core_web_sm')

# Load JSON data
def load_json(filename):
    with open(filename) as f:
        return json.load(f)

# Save JSON data
def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Extract and analyze text using SpaCy
def analyze_text(text):
    doc = nlp(text)
    entities = defaultdict(list)
    
    for ent in doc.ents:
        entities[ent.label_].append(ent.text)
    
    return entities

# Process and structure competitor profiles
def process_competitor_profiles(collected_data, organized_details):
    profiles = {}
    
    for competitor, data in organized_details.items():
        articles = data.get('details', {}).get('articles', [])
        products = []
        trends = []
        
        # Analyze each article
        for article in articles:
            title = article.get('title', '')
            description = article.get('description', '')
            content = article.get('content', '')
            
            # Extract products and trends from title and content
            entities = analyze_text(f"{title} {description} {content}")
            
            if 'PRODUCT' in entities:
                products.extend(entities['PRODUCT'])
            if 'ORG' in entities:
                trends.extend(entities['ORG'])
        
        profiles[competitor] = {
            'products': list(set(products)),  # Remove duplicates
            'market_trends': list(set(trends))  # Remove duplicates
        }
    
    return profiles

# Main function to perform data analysis
def analyze_data():
    collected_data = load_json('output/collected_data.json')
    organized_details = load_json('output/organized_details.json')
    
    # Process competitor profiles
    competitor_profiles = process_competitor_profiles(collected_data, organized_details)
    
    # Save competitor profiles to a JSON file
    save_json(competitor_profiles, 'competitor_profiles.json')
    print(f"Competitor profiles saved to competitor_profiles.json")
    return competitor_profiles  # Return profiles for app display

if __name__ == "__main__":
    analyze_data()