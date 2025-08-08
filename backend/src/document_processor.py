import os
import pdfplumber

def process_documents(docs_dir):
    documents = []
    print(f"Reading documents from: {docs_dir}")
    for filename in os.listdir(docs_dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(docs_dir, filename)
            doc_pages = []
            try:
                with pdfplumber.open(filepath) as pdf:
                    print(f"Processing {filename}...")
                    for i, page in enumerate(pdf.pages):
                        page_text = page.extract_text()
                        if page_text:
                            doc_pages.append({
                                "page_number": i + 1,
                                "text": page_text
                            })
                if doc_pages:
                    documents.append({"name": filename, "pages": doc_pages})
            except Exception as e:
                print(f"Could not read or process {filename}. Error: {e}")
    return documents