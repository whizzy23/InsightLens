import argparse
import time

from document_processor import process_documents
from section_extractor import extract_sections
from semantic_analyzer import analyze_sections
from output_generator import generate_json_output

def main():
    parser = argparse.ArgumentParser(description="Intelligent Document Analyst")
    parser.add_argument("--docs_dir", type=str, default="documents", help="Directory containing PDF documents")
    parser.add_argument("--persona_file", type=str, default="persona.txt", help="Path to the persona definition file")
    parser.add_argument("--job_file", type=str, default="job_to_be_done.txt", help="Path to the job-to-be-done file")
    parser.add_argument("--output_file", type=str, default="output.json", help="Path for the output JSON file")
    args = parser.parse_args()

    start_time = time.time()

    with open(args.persona_file, 'r', encoding='utf-8') as f:
        persona = f.read().strip()
    with open(args.job_file, 'r', encoding='utf-8') as f:
        job_to_be_done = f.read().strip()

    all_sections = []
    documents = process_documents(args.docs_dir)
    for doc in documents:
        sections = extract_sections(doc['pages'])
        for section in sections:
            section['document'] = doc['name']
        all_sections.extend(sections)

    ranked_sections = analyze_sections(all_sections, persona, job_to_be_done, summarize_top_n=5)

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
            "input_documents": [doc['name'] for doc in documents],
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        },
        "extracted_sections": final_extracted_sections,
        "subsection_analysis": final_subsection_analysis
    }

    generate_json_output(output_data, args.output_file)
    
    processing_time = time.time() - start_time
    print(f"\nProcessing complete in {processing_time:.2f} seconds.")
    print(f"Results saved to {args.output_file}")

if __name__ == "__main__":
    main()
