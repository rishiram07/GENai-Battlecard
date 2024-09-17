import streamlit as st
import os
from data_collection import collect_data
from data_analysis import analyze_data
from battlecard_generation import generate_battlecards
from battlecard_design import design_battlecards, TEMPLATES

# Function to clear old battlecards
def clear_old_battlecards():
    battlecards_dir = 'battlecards'
    if os.path.exists(battlecards_dir):
        for file in os.listdir(battlecards_dir):
            os.remove(os.path.join(battlecards_dir, file))

# Function to handle the 'Collect, Analyze, and Generate Battlecards' page
def show_collect_analyze_generate_page():
    st.title("Strategic Battlecard Generator ")

    st.write(
        """
        Welcome to the Battlecard Generator!

        This application helps you to:
        1. **Collect Data**: Input competitor names and industry keywords to gather relevant data.
        2. **Analyze Data**: Process and analyze the collected data to derive insights.
        3. **Generate Battlecards**: Create detailed battlecards based on the analysis.

        ### Instructions:
        - **Enter Competitor Names**: Provide a comma-separated list of competitor names. For example: `Competitor A, Competitor B`.
        - **Enter Industry Keywords**: Provide a comma-separated list of industry keywords relevant to your analysis. For example: `AI, Machine Learning, Data Science`.

        Click the "Process Data" button to start the data collection, analysis, and battlecard generation process. The application will handle all steps and display the results once completed.
        """
    )

    # Collect user inputs
    competitor_names = st.text_input("Enter competitor names (comma-separated):")
    industry_keywords = st.text_input("Enter industry keywords (comma-separated):")

    if st.button("Process Data"):
        if competitor_names and industry_keywords:
            # Convert inputs to appropriate formats
            competitor_names_list = [name.strip() for name in competitor_names.split(",")]
            industry_keywords_list = [keyword.strip() for keyword in industry_keywords.split(",")]

            # Clear old results
            clear_old_battlecards()

            # Call the collect_data function with the inputs
            collect_data(competitor_names_list, industry_keywords_list)
            
            # Call the analyze_data function
            analyze_data()
            
            # Call the generate_battlecards function
            generate_battlecards()
            
            # Display success message
            st.success("Data collected, analyzed, and battlecards generated successfully!")
        else:
            st.error("Please fill out all fields.")

# Function to handle the 'Design Battlecards' page
def show_design_battlecards_page():
    st.title("Design Battlecards")
    
    st.write(
        """
        After generating the battlecards, you can customize their appearance.

        ### Instructions:
        - **Select a Template**: Choose from the available design templates to style your battlecards. The options are `modern`, `classic`, and `professional`.
        - **Design Battlecards**: Click the "Design Battlecards" button to apply the selected template.

        Once the design process is complete, you will be able to download the customized battlecards.
        """
    )

    # Template selection
    selected_template = st.selectbox("Select Template", options=list(TEMPLATES.keys()))

    if st.button("Design Battlecards"):
        # Call the design_battlecards function with the selected template
        design_battlecards(template_name=selected_template)
        
        st.success("Battlecards designed successfully!")
        
        # Provide download link for battlecards
        st.write("Download the generated battlecards:")
        for file in os.listdir('battlecards'):
            if file.endswith('.pdf'):
                st.download_button(
                    label=f"Download {file}",
                    data=open(os.path.join('battlecards', file), 'rb').read(),
                    file_name=file
                )

# Streamlit page selection
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page", ["Collect, Analyze, and Generate Battlecards", "Design Battlecards"])

    if page == "Collect, Analyze, and Generate Battlecards":
        show_collect_analyze_generate_page()
    elif page == "Design Battlecards":
        show_design_battlecards_page()

if __name__ == "__main__":
    main()