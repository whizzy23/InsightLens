
import os
import time

from document_processor import process_documents
from section_extractor import extract_sections
from semantic_analyzer import analyze_sections
from output_generator import generate_json_output

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, '..', 'input')
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'output')

DOCS_DIR = os.path.join(INPUT_DIR, "documents")
PERSONA_FILE = os.path.join(INPUT_DIR, "persona.txt")
JOB_FILE = os.path.join(INPUT_DIR, "job_to_be_done.txt")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "output.json")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    start_time = time.time()

    try:
        with open(PERSONA_FILE, 'r', encoding='utf-8') as f:
            persona = f.read().strip()
        with open(JOB_FILE, 'r', encoding='utf-8') as f:
            job_to_be_done = f.read().strip()
    except FileNotFoundError as e:
        print(f"Error: Input file not found. Make sure persona.txt and job_to_be_done.txt are in the input directory.")
        print(e)
        persona = ""
        job_to_be_done = ""

    all_sections = []
    documents = process_documents(DOCS_DIR)
    if documents:
        for doc in documents:
            sections = extract_sections(doc['pages'])
            for section in sections:
                section['document'] = doc['name']
            all_sections.extend(sections)

        ranked_sections = analyze_sections(all_sections, persona, job_to_be_done, summarize_top_n=5)
    else:
        ranked_sections = []

    def clean_text(text):
        return text.replace('\n', ' ').replace('\r', '').strip()

    top_ranked_for_display = ranked_sections[:5]
    final_extracted_sections = []
    for i, section in enumerate(top_ranked_for_display):
        final_extracted_sections.append({
            "document": section.get('document', 'N/A'),
            "section_title": clean_text(section.get('section_title', 'Untitled Section')),
            "importance_rank": i + 1,
            "page_number": section.get('page_number', 1)
        })

    final_subsection_analysis = []
    summarized_sections = [s for s in ranked_sections if 'refined_text' in s]
    for section in summarized_sections:
        final_subsection_analysis.append({
            "document": section.get('document', 'N/A'),
            "refined_text": clean_text(section['refined_text']),
            "page_number": section.get('page_number', 1)
        })

    output_data = {
        "metadata": {
            "input_documents": [doc['name'] for doc in documents] if documents else [],
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        },
        "extracted_sections": final_extracted_sections,
        "subsection_analysis": final_subsection_analysis
    }

    generate_json_output(output_data, OUTPUT_FILE)

    processing_time = time.time() - start_time
    print(f"\nProcessing complete in {processing_time:.2f} seconds.")
    print(f"Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
