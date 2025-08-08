
import spacy
from sentence_transformers import SentenceTransformer, util
import numpy as np

print("Loading NLP models...")
nlp = spacy.load("en_core_web_md")
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
print("Models loaded successfully.")


def analyze_sections(sections, persona, job_to_be_done, summarize_top_n=5):
    if not sections:
        return []

    positive_query = (
        f"As a {persona}, I need to {job_to_be_done}. "
        "I am looking for actionable ideas about fun activities, nightlife, "
        "restaurants, local cuisine, city guides, and social events for young adults."
    )
    negative_query = "family-friendly activities, content for children, quiet museum guides, historical deep dives, packing lists"

    print(f"\nPositive Query: {positive_query}")
    print(f"Negative Query: {negative_query}")

    section_texts = [section['text'] for section in sections]
    corpus_embeddings = sentence_model.encode(section_texts, convert_to_tensor=True, show_progress_bar=True)

    positive_embedding = sentence_model.encode(positive_query, convert_to_tensor=True)
    negative_embedding = sentence_model.encode(negative_query, convert_to_tensor=True)

    positive_scores = util.cos_sim(positive_embedding, corpus_embeddings)[0]
    negative_scores = util.cos_sim(negative_embedding, corpus_embeddings)[0]

    final_scores = positive_scores - (negative_scores * 0.5)

    for i, section in enumerate(sections):
        section['importance_rank_score'] = final_scores[i].item()

    ranked_sections = sorted(sections, key=lambda x: x['importance_rank_score'], reverse=True)

    print(f"\nGenerating refined text for top {summarize_top_n} sections...")

    for section in ranked_sections[:summarize_top_n]:
        doc = nlp(section['text'])
        sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

        if len(sentences) > 0:
            sentence_embeddings = sentence_model.encode(sentences, convert_to_tensor=True)
            sentence_scores = util.cos_sim(positive_embedding, sentence_embeddings)[0]
            top_sentence_indices = np.argsort(sentence_scores.cpu().numpy())[-3:][::-1]

            refined_text = " ".join([sentences[i] for i in sorted(top_sentence_indices)])
            section['refined_text'] = refined_text
        else:
            section['refined_text'] = "Could not extract key sentences from this section."

    return ranked_sections
