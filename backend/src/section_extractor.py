
import re

def extract_sections(pages):
    all_sections = []
    for page in pages:
        page_chunks = _create_chunks_from_text(page['text'])
        
        for chunk in page_chunks:
            chunk['page_number'] = page['page_number']
            all_sections.append(chunk)

    return all_sections

def _create_chunks_from_text(text, paragraphs_per_chunk=8):
    sections = []
    
    paragraphs = re.split(r'\n\s*\n', text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    if not paragraphs:
        return []

    for i in range(0, len(paragraphs), paragraphs_per_chunk):
        chunk_paragraphs = paragraphs[i:i + paragraphs_per_chunk]
        chunk_text = "\n\n".join(chunk_paragraphs)
        
        title = "Untitled Section"
        found_title = False
        for paragraph in chunk_paragraphs:
            lines = paragraph.split('\n')
            first_line = lines[0].strip()
            if len(lines) == 1 and first_line.isupper() and len(first_line.split()) < 10:
                title = first_line
                found_title = True
                break
        
        if not found_title:
             title = chunk_paragraphs[0].split('\n')[0].strip()

        title = re.sub(r'^[\s\W]*', '', title)
        
        sections.append({
            "section_title": title,
            "text": chunk_text
        })
        
    return sections
