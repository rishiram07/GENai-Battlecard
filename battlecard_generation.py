import json
import os
from groq import Groq

# Load API keys and competitor profiles
def load_api_keys(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        raise
    except json.JSONDecodeError:
        print(f"Error: File '{filename}' is not a valid JSON file.")
        raise

def load_competitor_profiles(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        raise
    except json.JSONDecodeError:
        print(f"Error: File '{filename}' is not a valid JSON file.")
        raise

def generate_battlecard(competitor_name, competitor_profile, products, api_key):
    client = Groq(api_key=api_key)
    prompt = f"""
    Generate a detailed battlecard for {competitor_name} using the following competitor profile and product information:

    Competitor Profile:
    {json.dumps(competitor_profile, indent=2)}

    Products:
    {json.dumps(products, indent=2)}

    The battlecard should include the following sections in this order:

    1. **Competitor Overview**: Provide a summary of the competitor's background and key information.
    2. **Products**: List and describe the competitor's products.
    3. **Market Trends**: Discuss relevant market trends affecting the competitor.
    4. **Pricing**: Outline the competitor's pricing strategy.
    5. **Strengths**: Highlight the competitor's strengths.
    6. **Weaknesses**: Identify the competitor's weaknesses.
    7. **Market Positioning**: Explain how the competitor is positioned in the market.
    8. **Additional Insights**: Offer any other pertinent information.
    9. **Conclusion**: Summarize the key takeaways from the battlecard.

    Ensure each section is clear and well-structured.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating battlecard for {competitor_name}: {e}")
        return None

# Wrapper function to generate multiple battlecards
def generate_battlecards():
    # Load API keys and competitor profiles
    api_keys = load_api_keys('data/api_keys.json')
    competitor_profiles = load_competitor_profiles('competitor_profiles.json')

    print("Competitor Profiles:", competitor_profiles)  # Debugging line

    battlecards = {}
    for competitor, profile in competitor_profiles.items():
        print(f"Processing {competitor}")  # Debugging line

        products = profile.get('products', [])
        if not products:
            print(f"Warning: No products found for {competitor}.")
        
        battlecard = generate_battlecard(competitor, profile, products, api_keys.get('groq', ''))
        if battlecard:
            battlecards[competitor] = battlecard
        else:
            print(f"Skipping {competitor} due to error in battlecard generation.")

    try:
        with open('battlecards.json', 'w') as file:
            json.dump(battlecards, file, indent=2)
        print("Battlecards saved to battlecards.json")
    except IOError:
        print("Error: Could not write to 'battlecards.json'.")
        raise

    return battlecards

if __name__ == "__main__":
    generate_battlecards()