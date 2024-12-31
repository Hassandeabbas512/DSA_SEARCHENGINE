import gradio as gr
import json
import os
from .indexer import process_news_csv_large
from .search import search_engine_with_barrels

def setup_and_process_data():
    """Set up data processing and create barrels if not already processed."""
    file_path = "CNN_Articels_clean.csv"
    num_barrels = 10
    if not os.path.exists("barrel_0.json"):
        print("Processing data and creating barrels...")
        process_news_csv_large(file_path, num_barrels)
    else:
        print("Barrels already exist. Skipping data processing...")

def create_gradio_interface():
    """Create the Gradio interface for the search engine."""
    with open("lexicon.json", "r", encoding="utf-8") as f:
        lexicon = json.load(f)
    with open("forward_index.json", "r", encoding="utf-8") as f:
        forward_index = json.load(f)

    def search_wrapper(query):
        """Handles the search and prepares the Gradio-compatible output."""
        # Call the search engine
        results, details, error = search_engine_with_barrels(query, lexicon, forward_index)

        # Check for errors
        if error:
            return [], f"Error: {error}"

        # Prepare dataframe output
        dataframe_results = [
            (result["Document"], result["Score"], result["Preview"]) for result in results
        ]

        # Prepare markdown output for details
        details_markdown = "\n\n".join(
            f"### {doc_id}\n\n{content}" for doc_id, content in details.items()
        )
        details_markdown = ""

        return dataframe_results, details_markdown

    return gr.Interface(
        fn=search_wrapper,
        inputs=gr.Textbox(label="Enter your search query:"),
        outputs=[
            gr.Dataframe(
                headers=["Document", "Score", "Preview"],
                label="Search Results"
            ),
            gr.Markdown(label="Document Details")
        ],
        title="ABC News Search Engine",
        description="Enter a search query to find news articles from the ABC News archive."
    )

if __name__ == "__main__":
    setup_and_process_data()
    print("Launching search engine...")
    app = create_gradio_interface()
    app.launch()
