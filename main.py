from data_collection import collect_data
from data_analysis import main as analyze_data
from battlecard_generation import main as generate_battlecards
from battlecard_design import main as design_battlecards

def main():
    # Step 1: Collect data
    competitors = ["Apple", "Samsung", "Google", "Vivo"]
    keywords = ["Smartphones", "Artificial Intelligence", "Consumer Electronics"]
    urls = {
        "Apple": "https://www.apple.com",
        "Samsung": "https://www.samsung.com",
        "Google": "https://www.google.com",
        "Vivo": "https://www.vivo.com"
    }
    collect_data(competitors, keywords, urls)
    
    # Step 2: Analyze data
    analyze_data()
    
    # Step 3: Generate battlecards
    generate_battlecards()
    
    # Step 4: Design and save battlecards
    design_battlecards()

if __name__ == "__main__":
    main()