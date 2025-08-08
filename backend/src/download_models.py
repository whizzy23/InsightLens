
from sentence_transformers import SentenceTransformer

def main():
    print("Downloading Sentence Transformer model...")
    SentenceTransformer('all-MiniLM-L6-v2')
    print("Model downloaded successfully.")

if __name__ == "__main__":
    main()
