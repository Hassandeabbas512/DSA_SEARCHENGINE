import gradio as gr
import json  # Fix: Import the JSON module
from .indexer import process_news_csv_large
from .search import search_engine_with_barrels
import os

def setup_and_process_data():
    """Set up data processing and create barrels if not already processed."""
    file_path = "abcnews-date-text.csv"
    num_barrels = 10
    if not os.path.exists("barrel_0.json"):
        print("Processing data and creating barrels...")
        process_news_csv_large(file_path, num_barrels)
    else:
        print("Barrels already exist. Skipping data processing...")

def create_gradio_interface():
    """Create the Gradio interface for the search engine."""
    with open("lexicon.json", "r") as f:
        lexicon = json.load(f)
    with open("forward_index.json", "r") as f:
        forward_index = json.load(f)

    def search_wrapper(query):
        # This function receives the user query, calls the search engine, and returns results
        return search_engine_with_barrels(query, lexicon, forward_index)

    return gr.Interface(
        fn=search_wrapper,
        inputs=gr.Textbox(label="Enter your search query:"),
        outputs=gr.Markdown(label="Search Results"),
        title="ABC News Search Engine",
        description="Enter a search query to find news articles from the ABC News archive."
    )


if __name__ == "__main__":
    setup_and_process_data()
    print("Launching search engine...")
    app = create_gradio_interface()
    app.launch()
