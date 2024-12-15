import json
import os
from db_operations import initialize_database, insert_document

def load_arxiv_dataset(folder_path):
    """
    Load the arXiv dataset from the specified folder and insert documents into the database.
    """
    # Initialize the database
    initialize_database()
    
    # Iterate through all JSON files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line)  # Parse each line as a JSON object
                        title = entry.get('title', '')
                        abstract = entry.get('abstract', '')
                        if title and abstract:
                            full_content = f"{title} {abstract}"  # Combine title and abstract
                            embedding = None  # Or create an actual embedding if needed
                            
                            # Insert into the database
                            insert_document(full_content, embedding)
                            print(f"Inserted document: {title}")
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON in file {filename}: {e}")

if __name__ == "__main__":
    arxiv_folder = "/home/bealthguy/Public/projects/web/plagiarism-detection/datasets/"  # Change to the actual path of your dataset
    load_arxiv_dataset(arxiv_folder)