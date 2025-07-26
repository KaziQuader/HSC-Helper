# HSC-Helper
Multilingual RAG System to Answer HSC Bangla Questions

# Setup Guide
## 1. Virtual Environment
- python3.11 -m venv venv (Used Python 3.11 if this version is not installed please install it)
- source venv/bin/activate

## 2. Python Requirements
- pip install -r requirements.txt

## 3. Set Up Tesseract for Bengali OCR
### MacOS
- Install homebrew
- Run terminal 
- brew install tesseract
- brew install tesseract-lang
- brew install poppler
- To check if installed properly: ls /opt/homebrew/share/tessdata | grep ben (ben.traineddata output)
- If its still missing:
    - cd /opt/homebrew/share/tessdata
    - curl -O https://github.com/tesseract-ocr/tessdata/raw/main/ben.traineddata
- Set TESSDATA_PREFIX and POPPLER_PATH in .env file. (Paths may vary please try to locate) **Only do this if neccessary.**

### Windows
- Download and install Tesseract from:
https://github.com/UB-Mannheim/tesseract/wiki
- During installation, select Bengali language in the language options.
- Default installation path: C:/Program Files/Tesseract-OCR/
- To check if installed properly:
Open Command Prompt and run: dir "C:\Program Files\Tesseract-OCR\tessdata" | findstr ben
- if its still missing open command prompt and run:
    - cd "C:\Program Files\Tesseract-OCR\tessdata"
    - curl -O https://github.com/tesseract-ocr/tessdata/raw/main/ben.traineddata
- Download and extract Poppler for Windows:
https://github.com/oschwartz10612/poppler-windows/releases
- Extract the ZIP file, e.g. to C:/poppler-24.08.0/Library/bin
- Set TESSDATA_PREFIX and POPPLER_PATH in .env file. (Paths may vary please try to locate) **Only do this if neccessary.**

### Ubuntu/Linux
- On your terminal run the following commands:
    - sudo apt update
    - sudo apt install tesseract-ocr
    - sudo apt install tesseract-ocr-ben
    - sudo apt install poppler-utils
- To check if Bengali installed: ls /usr/share/tesseract-ocr/4.00/tessdata/ | grep ben
- If ben.traineddata is missing, download manually:
    - cd /usr/share/tesseract-ocr/4.00/tessdata/
    - sudo curl -O https://github.com/tesseract-ocr/tessdata/raw/main/ben.traineddata
- Set TESSDATA_PREFIX and POPPLER_PATH in .env file. (Paths may vary please try to locate) **Only do this if neccessary.**

## 5. Setup Qdrant VectorDB
- Install Docker Desktop
- In your Terminal Run:
    - docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant
- Verify Qdrant is running by visiting http://localhost:6333/dashboard#/welcome

## 4. Setup your Google Api Key in the .env file.
- GOOGLE_API_KEY=your_gemini_api_key


# Used Tools, Library, Package
| Step           | Tool Used                                 | Package / Library                            |
|--------------  |-------------------------------------------|----------------------------------------------|
| PDF Extraction | PyTesseract                               | pytesseract, pdf2image                       |
| Chunking       | RecursiveCharacterTextSplitter            | langchain.text_splitter                      |
| Embedding      | paraphrase-multilingual-MiniLM-L12-v2     | sentence_transformer                         |
| Storage        | Qdrant VectorDB                           | qdrant_client                                |
| Generation     | Gemini-2.5-pro                            | langchain_google_genai                       |


# Sample Queries & Outputs


# Project Related Questions
## What method or library did you use to extract the text, and why? Did you face any formatting challenges with the PDF content?
- Initially pymupdf, pdfmine, and pdfplumber were used. However, copy-pasting some texts from the pdf generated gibberish. Due to the fact that the pdf was converted from powerpoint slides to pdf the encoding for the language was different. As a result, pdf2image and pytesserect were used, which uses OCR to extract text.
- Some of the pages contain table to represent information such as word meaning, author information, some answers, and some pages had pictures which caused the OCR to output texts that were not correctly formatted, had missing letters, skipped lines, or generated texts that did not make sense.
- Regex was used to clean the text as much as possible. However, some irrelevant information still remained.

## What chunking strategy did you choose (e.g. paragraph-based, sentence-based, character limit)? Why do you think it works well for semantic retrieval?
Recursive characted-based chunking was used. It uses seperators and structure of the document(preserves logical sentence and paragraph boundaries) to make chunking decision rather than chunking a fixed size. 
It works well because:
1. As it chunks by sentence or paragraph delimeters such as '.', new-line, new-paragraph, etc. it retains complete thoughts making the inputs semantically complete.
2. In our case it knew how to handle bengali full-stop and other bengali seperators, which are not present in english language.
3. Tries to seperate meanigfully by paragraphs, if it cannot then falls back to smaller seperators ensuring chunks are not created from a middle of a sentence or phrase.
4. It uses chunk-overlap and consistent chunk-size to minimize loss of context between chunks.
5. All of the above helps to produce better embeddings for vector search.

## What embedding model did you use? Why did you choose it? How does it capture the meaning of the text?
Setence Transformer was used as it can understand and compare the semantic content of sentences. Hugging face's paraphrase-multilingual-MiniLM-L12-v2 model was used because it can handle various languages including bengali. Apart from that some more reasons are:
1. Captures semantic meaning which helps to match the user's query to relevant documents/chunks in our vectorDB.
2. Does not rely on keyword-based searching. This means that the retriever in our RAG can retrieve documents that are sementacilly relevant to the query, even if key-word do not match.
3. The RAG model can understand context of both the query and the documents retrieved. This generates better context-aware output.
4. Can handle large dataset of documents.

## How are you comparing the query with your stored chunks? Why did you choose this similarity method and storage setup?
- Embed the user's query with the same embedding model (paraphrase-multilingual-MiniLM-L12-v2). Query the Qdrant VectorDB using the query embedding  and find the most relavant chunk based on COSINE Similarity.
- COSINE Similarity works great while using Sentence Transformers and is ideal for semantic comparision. It helps in matching meaning between the query and chunks rather than raw word overlap.
- Qdrant was used as it supports storing metadata along with vectors, has features like payload storage, has a nice set of APIs, and the documentation is well written. Also, it comes with a GUI which can be used to analyse the chunks created.

## How do you ensure that the question and the document chunks are compared meaningfully? What would happen if the query is vague or missing context?
- Same embedding model was used for both the query and the chunks makes sure that the embedding of the query and the chunks can be compared (different models might output different embeddings). The query embeddings are sent to the qdrant vectordb which uses COSINE Similarity to retrieve the appropritae chunks. Also, Recursive Text Splitter makes sure we have chunks that are contextually aligned with queries.
- Implemented a short-term memory by preserving the last five chats. The chats create a chat history which is used along with a prompt template to transform the query. Thus, even if the query is vague or missing context the model will use the chat history to understand the user's query.

## Do the results seem relevant? If not, what might improve them (e.g. better chunking, better embedding model, larger document)?
Till now all qeuries generated relavant results.