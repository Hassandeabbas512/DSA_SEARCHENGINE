import json
from .text_processor import tokenize
 
# Ensure this import is correct

# Load and inspect a specific barrel
barrel_index = 0  # Adjust this to inspect different barrels
filename = f"barrel_{barrel_index}.json"

try:
    with open(filename, "r", encoding="utf-8") as f:
        barrel = json.load(f)

    print(f"Barrel {barrel_index} contains {len(barrel)} terms.")
    print("Sample data from the barrel:")
    for term, docs in list(barrel.items())[:10]:  # Display the first 10 terms and their documents
        print(f"Term: {term}, Docs: {docs}")

except FileNotFoundError:
    print(f"Error: {filename} not found.")

