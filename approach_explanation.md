# Approach Explanation: Persona-Driven Document Intelligence

Our solution is an automated document analysis pipeline designed to extract and prioritize information from a collection of PDFs based on a user's specific persona and goal. The system is built to be generic, robust, and fully compliant with the hackathon's offline and performance constraints. The methodology is centered around a multi-stage process involving document parsing, semantic analysis, and relevance ranking.

## 1. Document Processing and Section Extraction

The first stage involves ingesting the raw PDF documents. We use the pdfplumber library for this task due to its superior ability to parse documents based on their visual layout. This allows us to accurately reconstruct lines, paragraphs, and structural elements, overcoming common issues like fragmented text. The system processes each document to extract its core structural components, identifying potential sections based on typographical cues such as font size, boldness, and spacing. This step produces a clean, structured representation of the content from all documents in the collection.

## 2. Semantic Analysis and Relevance Scoring

The core of our solution is its ability to understand the semantic relationship between the user's request and the document content. We employ a pre-trained all-MiniLM-L6-v2 Sentence Transformer model to convert both the user's query (a combination of the persona and job-to-be-done) and the extracted document sections into high-dimensional vector embeddings.

Relevance is determined by calculating the cosine similarity between the query embedding and each section's embedding. This allows the system to move beyond simple keyword matching and identify sections that are contextually and conceptually related to the user's goal. To further refine the results, we use a positive/negative query strategy, where the final relevance score is a composite of similarity to the desired topics and dissimilarity to irrelevant ones.

## 3. Section Ranking and Summarization

Once scored, all sections from the document collection are ranked by their relevance. The top-ranked sections are identified as the most important for the user's task. For these key sections, a final analysis is performed to provide a concise summary. We use the spaCy library for robust sentence tokenization. The sentences within each top-ranked section are themselves embedded and scored against the user's query, and the most relevant sentences are extracted to form a "refined text" summary.

## 4. Offline Execution and Dependency Management

The entire system is packaged within a Docker container to ensure portability and adherence to the offline constraint. All necessary models, including the Sentence Transformer and the spaCy language model, are downloaded and cached during the docker build process. We explicitly install a CPU-only version of torch to keep the image size minimal and compliant with the "CPU-only" rule. At runtime, environment variables (HF_HUB_OFFLINE, TRANSFORMERS_OFFLINE) are set to force the Hugging Face libraries into a true offline mode, guaranteeing that no network calls are made during execution.