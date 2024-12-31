import json
from collections import defaultdict
import math
from .text_processor import tokenize, highlight_query_terms

def load_barrels(num_barrels):
    """Load all barrels from files."""
    barrels = []
    for i in range(num_barrels):
        filename = f"barrel_{i}.json"
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                barrel = json.load(f)
                barrels.append(barrel)  # Properly load each JSON file
                print(f"Barrel {i} loaded successfully with {len(barrel)} terms.")
        except FileNotFoundError:
            print(f"Warning: Barrel {i} not found.")
            barrels.append({})
    return barrels

def search_in_barrel(query_tokens, barrel, forward_index, total_docs):
    scores = defaultdict(float)

    for token in query_tokens:
        print(f"Searching for token: {token}")

        if token in barrel:
            print(f"Token '{token}' found in barrel.")

            doc_list = barrel[token]
            print(f"Docs for token '{token}': {doc_list}")

            df = len(doc_list)  # Document frequency
            idf = math.log((1 + total_docs) / (1 + df))  # Calculate IDF

            for doc in doc_list:
                if str(doc) in forward_index:
                    tf = forward_index[str(doc)].count(token)  # Term frequency
                    scores[doc] += tf * idf  # Add to score
                else:
                    print(f"Warning: Document {doc} not found in forward_index!")
        else:
            print(f"Token '{token}' not found in this barrel.")

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def search_engine_with_barrels(query, lexicon, forward_index, num_barrels=10):
    """Search across all barrels for the query."""
    try:
        # Tokenize the query
        query_tokens = tokenize(query)
        if not query_tokens:
            return [], {}, "Invalid query. Please provide valid search terms."

        # Load barrels
        barrels = load_barrels(num_barrels)
        results = []
        total_docs = len(forward_index)

        # Search in all barrels
        for barrel in barrels:
            results.extend(search_in_barrel(query_tokens, barrel, forward_index, total_docs))

        # Sort results by score in descending order
        results = sorted(results, key=lambda x: x[1], reverse=True)
        if not results:
            return [], {}, "No results found."

        # Prepare output and details
        output = []
        details = {}
        for doc, score in results[:10]:  # Top 10 results
            if str(doc) not in forward_index:
                continue

            # Generate preview and full article
            preview = " ".join(forward_index[str(doc)][:50])
            highlighted_preview = highlight_query_terms(preview, query_tokens)
            full_article = " ".join(forward_index[str(doc)])

            output.append({
                "Document": f"Document {doc}",
                "Score": f"{score:.2f}",
                "Preview": highlighted_preview,
                "Full": full_article
            })
            details[f"Document {doc}"] = full_article

        return output, details, ""

    except Exception as e:
        # Handle unexpected errors
        return [], {}, f"An error occurred: {str(e)}"

if __name__ == "__main__":
    query = input("Enter your search query: ").strip()
    num_barrels = 10

    try:
        with open("lexicon.json", "r", encoding="utf-8") as f:
            lexicon = json.load(f)

        with open("forward_index.json", "r", encoding="utf-8") as f:
            forward_index = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)

    print("\nSearching...\n")
    search_results = search_engine_with_barrels(query, lexicon, forward_index, num_barrels)
    print(search_results)
