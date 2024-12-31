
import json
import os
import pandas as pd
from collections import defaultdict
from .text_processor import tokenize  # Ensure consistent tokenization

def process_news_csv_large(file_path, num_barrels):
    """
    Process large CSV files to create barrels, lexicon, and forward index.
    Each barrel is saved as a separate JSON file.

    Args:
        file_path (str): Path to the CSV file.
        num_barrels (int): Number of barrels to split the data into.

    Returns:
        None
    """
    # Lexicon and forward index placeholders
    lexicon = defaultdict(list)  # Maps words to document IDs
    forward_index = {}  # Maps document IDs to word lists

    # Initialize empty barrels
    barrels = [{} for _ in range(num_barrels)]
    barrel_size = 100000  # Approximate number of lines per chunk
    total_docs = 0

    print(f"Processing {file_path} in chunks of {barrel_size} lines...")

    # Process the CSV file in chunks
    for chunk in pd.read_csv(file_path, chunksize=barrel_size):
        for index, row in chunk.iterrows():
            doc_id = total_docs
            text = row['Article text']
            words = tokenize(text)  # Use tokenized words for indexing

            # Update forward index
            forward_index[doc_id] = words

            # Update lexicon and barrels
            for word in set(words):
                lexicon[word].append(doc_id)
                barrel_index = hash(word) % num_barrels  # Hash for even distribution
                if word not in barrels[barrel_index]:
                    barrels[barrel_index][word] = []
                barrels[barrel_index][word].append(doc_id)

            total_docs += 1

        print(f"Processing chunk... {total_docs} documents processed so far.")

    # Save barrels, lexicon, and forward index
    save_barrels(barrels, num_barrels)
    save_lexicon_and_forward_index(lexicon, forward_index)

    print(f"Processing complete. {total_docs} documents processed.")

def save_barrels(barrels, num_barrels):
    """Save each barrel as a JSON file."""
    for i in range(num_barrels):
        filename = f"barrel_{i}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(barrels[i], f, ensure_ascii=False, indent=4)
    print("Barrels saved successfully.")

def save_lexicon_and_forward_index(lexicon, forward_index):
    """Save the lexicon and forward index as JSON files."""
    with open("lexicon.json", "w", encoding="utf-8") as f:
        json.dump(lexicon, f, ensure_ascii=False, indent=4)
    with open("forward_index.json", "w", encoding="utf-8") as f:
        json.dump(forward_index, f, ensure_ascii=False, indent=4)
    print("Lexicon and forward index saved successfully.")

def load_lexicon_and_forward_index():
    """Load lexicon and forward index from JSON files."""
    with open("lexicon.json", "r", encoding="utf-8") as f:
        lexicon = json.load(f)
    with open("forward_index.json", "r", encoding="utf-8") as f:
        forward_index = json.load(f)
    print("Lexicon and forward index loaded.")
    return lexicon, forward_index

def load_barrels(num_barrels):
    """Load all barrel files into a list."""
    barrels = []
    for i in range(num_barrels):
        with open(f"barrel_{i}.json", "r", encoding="utf-8") as f:
            barrels.append(json.load(f))
    print("All barrels loaded.")
    return barrels

def process_news_csv_with_barrels(file_path, num_barrels):
    """
    Wrapper function to process the CSV file and create barrels.

    Args:
        file_path (str): Path to the CSV file.
        num_barrels (int): Number of barrels to split the data into.

    Returns:
        None
    """
    if not os.path.exists("lexicon.json") or not os.path.exists("forward_index.json"):
        process_news_csv_large(file_path, num_barrels)
    else:
        print("Lexicon and forward index already exist. Skipping processing.")

if __name__ == "__main__":
    file_path = "CNN_Articels_clean.csv"  # Input CSV file
    num_barrels = 10  # Number of barrels to create

    # Process and create barrels
    process_news_csv_with_barrels(file_path, num_barrels)

    # Load data (testing purposes)
    lexicon, forward_index = load_lexicon_and_forward_index()
    barrels = load_barrels(num_barrels)

    # Output sample data for verification
    print("Sample lexicon:", dict(list(lexicon.items())[:5]))
    print("Sample forward index:", dict(list(forward_index.items())[:5]))
    print("Sample barrel 0:", list(barrels[0].items())[:5])