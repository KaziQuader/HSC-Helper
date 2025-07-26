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
- Change the path of tesseract accordingly in extract_pdf.py on line 35 (Paths may vary please try to locate)

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
- Change the path of tesseract accordingly in extract_pdf.py on line 35 (Paths may vary please try to locate)

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
- Change the path of tesseract accordingly in extract_pdf.py on line 35 (Paths may vary please try to locate)

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
## Bengali
Query 1: কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?

Answer 1:
"অপরিচিতা" গল্পে অনুপমের **মামাকে** তার ভাগ্য দেবতা বা 'ভাগ্যদেবতার প্রধান এজেন্ট' বলে উল্লেখ করা হয়েছে।

এর কারণ হলো:

*   **পারিবারিক প্রভাব:** অনুপমের পিতার মৃত্যুর পর তার মামাই পরিবারের কর্তা হয়ে ওঠেন।
*   **সর্বময় কর্তৃত্ব:** পরিবারে তার প্রভাব এতটাই বেশি ছিল যে, অনুপমের বিয়েসহ জীবনের সকল গুরুত্বপূর্ণ সিদ্ধান্ত তিনিই নিতেন।
*   **নির্ভরশীলতা:** অনুপম নিজে শিক্ষিত ও প্রাপ্তবয়স্ক হওয়া সত্ত্বেও কোনো সিদ্ধান্ত নেওয়ার ক্ষমতা রাখত না এবং সম্পূর্ণরূপে মামার উপর নির্ভরশীল ছিল।

এই নিরঙ্কুশ প্রভাব ও কর্তৃত্বের কারণেই অনুপম তার মামাকে নিজের ভাগ্য নিয়ন্ত্রক বা ভাগ্যদেবতার প্রধান প্রতিনিধি হিসেবে উল্লেখ করেছে।
"অপরিচিতা" গল্পে অনুপমের **মামাকে** তার ভাগ্য দেবতা বা 'ভাগ্যদেবতার প্রধান এজেন্ট' বলে উল্লেখ করা হয়েছে।

এর কারণ হলো:

*   **পারিবারিক প্রভাব:** অনুপমের পিতার মৃত্যুর পর তার মামাই পরিবারের কর্তা হয়ে ওঠেন।
*   **সর্বময় কর্তৃত্ব:** পরিবারে তার প্রভাব এতটাই বেশি ছিল যে, অনুপমের বিয়েসহ জীবনের সকল গুরুত্বপূর্ণ সিদ্ধান্ত তিনিই নিতেন।
*   **নির্ভরশীলতা:** অনুপম নিজে শিক্ষিত ও প্রাপ্তবয়স্ক হওয়া সত্ত্বেও কোনো সিদ্ধান্ত নেওয়ার ক্ষমতা রাখত না এবং সম্পূর্ণরূপে মামার উপর নির্ভরশীল ছিল।

এই নিরঙ্কুশ প্রভাব ও কর্তৃত্বের কারণেই অনুপম তার মামাকে নিজের ভাগ্য নিয়ন্ত্রক বা ভাগ্যদেবতার প্রধান 

Query 2: অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?

Answer 2: 
'অপরিচিতা' গল্পে অনুপমের ভাষায় তার বন্ধু **হরিশকে** সুপুরুষ বলা হয়েছে।

গল্পের বর্ণনানুসারে, অনুপম তার বন্ধু হরিশ সম্পর্কে বলেছে:

*   **"হরিশ কানপুরে কাজ করে। সে আমার চেয়ে দুই ক্লাসের উপরের ছাত্র ছিল। ছেলেটি ভারী রসিক, আসর জমাতে অদ্বিতীয় এবং handsome যাকে বলে, অর্থাৎ **সুপুরুষ** বটে।"**
*   হরিশকে একজন রসিক এবং আড্ডায় আসর জমাতে পারদর্শী হিসেবে বর্ণনা করা হয়েছে।
*   মূলত হরিশই কল্যাণীর সম্বন্ধটি অনুপমের পরিবারের কাছে নিয়ে আসে।
'অপরিচিতা' গল্পে অনুপমের ভাষায় তার বন্ধু **হরিশকে** সুপুরুষ বলা হয়েছে।

গল্পের বর্ণনানুসারে, অনুপম তার বন্ধু হরিশ সম্পর্কে বলেছে:

*   **"হরিশ কানপুরে কাজ করে। সে আমার চেয়ে দুই ক্লাসের উপরের ছাত্র ছিল। ছেলেটি ভারী রসিক, আসর জমাতে অদ্বিতীয় এবং handsome যাকে বলে, অর্থাৎ **সুপুরুষ** বটে।"**
*   হরিশকে একজন রসিক এবং আড্ডায় আসর জমাতে পারদর্শী হিসেবে বর্ণনা করা হয়েছে।
*   মূলত হরিশই কল্যাণীর সম্বন্ধটি অনুপমের পরিবারের কাছে নিয়ে আসে।

Query 3: বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?

Answer 3:
'অপরিচিতা' গল্প অনুসারে, বিয়ের সময় কল্যাণীর প্রকৃত বয়স ছিল **১৫ বছর**।

প্রদত্ত তথ্যে এই সম্পর্কিত একটি বহুনির্বাচনি প্রশ্নও উল্লেখ করা হয়েছে:

*   **প্রশ্ন ৫৪:** বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?
    *   (ক) ১৪ বছর
    *   **(খ) ১৫ বছর**
    *   (গ) ১৬ বছর
    *   (ঘ) ১৭/১৮ বছর

গল্পের মূল কাহিনি অনুযায়ী, সঠিক উত্তরটি হলো **১৫ বছর**।
'অপরিচিতা' গল্প অনুসারে, বিয়ের সময় কল্যাণীর প্রকৃত বয়স ছিল **১৫ বছর**।

প্রদত্ত তথ্যে এই সম্পর্কিত একটি বহুনির্বাচনি প্রশ্নও উল্লেখ করা হয়েছে:

*   **প্রশ্ন ৫৪:** বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?
    *   (ক) ১৪ বছর
    *   **(খ) ১৫ বছর**
    *   (গ) ১৬ বছর
    *   (ঘ) ১৭/১৮ বছর

গল্পের মূল কাহিনি অনুযায়ী, সঠিক উত্তরটি হলো **১৫ বছর**।


## English
Query 1: Who has been referred to as Anupam's god of fortune?

Answer 1:
Based on the provided context from the story 'Aparichita', **Anupam's Mama (uncle)** has been referred to as the god of fortune.

Here are the specific points from the text that support this:

*   A multiple-choice question directly asks: "কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?" (Who has been referred to as Anupam's god of fortune?), with **মামা (Mama)** as an option.
*   He is also described as the **"chief agent" (প্রধান এজেন্ট) of the god of fortune** because of the significant **influence (প্রভাব)** he had over Anupam's life and family.
Based on the provided context from the story 'Aparichita', **Anupam's Mama (uncle)** has been referred to as the god of fortune.

Here are the specific points from the text that support this:

*   A multiple-choice question directly asks: "কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?" (Who has been referred to as Anupam's god of fortune?), with **মামা (Mama)** as an option.
*   He is also described as the **"chief agent" (প্রধান এজেন্ট) of the god of fortune** because of the significant **influence (প্রভাব)** he had over Anupam's life and family.


Query 2: According to Anupam, who is referred to as a noble/good man?

Answer 2:
Based on the provided text, **Anupam refers to himself** as a noble/good man (সৎপাত্র).

He justifies this by stating:
*   Any father of a daughter would consider him a suitable groom (**সৎপাত্র**).
*   He doesn't even smoke tobacco ("তামাকটুকু পর্যন্ত খাই না").
*   He considers himself an "utterly good man" (**নিতান্ত ভালোমানুষ**) because there is no trouble or effort involved in being one.
*   He is obedient to his mother's commands.
Based on the provided text, **Anupam refers to himself** as a noble/good man (সৎপাত্র).

He justifies this by stating:
*   Any father of a daughter would consider him a suitable groom (**সৎপাত্র**).
*   He doesn't even smoke tobacco ("তামাকটুকু পর্যন্ত খাই না").
*   He considers himself an "utterly good man" (**নিতান্ত ভালোমানুষ**) because there is no trouble or effort involved in being one.
*   He is obedient to his mother's commands.


Query 3: What was Kalyani's actual age at the time of marriage?

Answer 3: 
Based on the provided context, here is the information regarding Kalyani's age at the time of marriage.

According to a multiple-choice question found in the context, Kalyani's actual age at the time of marriage was **15 years**.

The specific question (number 54) from the text is:
*   **"বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?"** (What was Kalyani's actual age at the time of marriage?)
    *   (ক) ১৪ বছর (14 years)
    *   **(খ) ১৫ বছর (15 years)**
    *   (গ) ১৬ বছর (16 years)
    *   (ঘ) ১৭/১৮ বছর (17/18 years)
Based on the provided context, here is the information regarding Kalyani's age at the time of marriage.

According to a multiple-choice question found in the context, Kalyani's actual age at the time of marriage was **15 years**.

The specific question (number 54) from the text is:
*   **"বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?"** (What was Kalyani's actual age at the time of marriage?)
    *   (ক) ১৪ বছর (14 years)
    *   **(খ) ১৫ বছর (15 years)**
    *   (গ) ১৬ বছর (16 years)
    *   (ঘ) ১৭/১৮ বছর (17/18 years)


# API Documentation
1. Open Terminal and cd to the root directory of the project (api.py stays)
2. run: uvicorn api:app --reload 
3. Open Postman, create a collection, add a new request.
4. Make sure the method is POST, Header has key as Content-type and value as application/json.
5. Go to the Body tab, select raw and add your json request.
6. Example json request: 
    - {
        "session_id": "user123",
        "query": "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?"
        }
7. You will get a response that will include session_id, query, response, memory, and chat_history

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
Setence Transformer was used as it can understand and compare the semantic content of sentences. Hugging face's intfloat/multilingual-e5-base model was used because it can handle various languages including bengali. Apart from that some more reasons are:
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
Trying the sample questions that were given in the documents generated 2 right answers out of 3.
Ways to improve:
1. Better extraction method and cleaning of the extracted text will lead to better results. (Main Pain Point I faced)
2. Trying semantic chunking rather than recursive chunking.
3. Using bigger and better embedding model. (Not Cost Effecient / Time Effecient)
4. While storing the embedding in the vector database, adding metadata such as what type of text it is. E.g passage, author information, word meaning, questions, mcq, etc.
5. Generating better prompt template.
6. Using an LLM model that is specifically trained on bengali language.
7. Perform techniques such as Retriever Ensembling and Reranking.
As this is a simple project, improvements can be made at every aspect. Thus, there are more techniques that I can write over here.
Even though the extraction is not optimum the model is able to give answers with explanations.

# References:
1. https://www.anyscale.com/blog/a-comprehensive-guide-for-building-rag-based-llm-applications-part-1?curius=1144#vector-db-creation
2. https://www.anyscale.com/blog/rag-pipelines-how-to
3. https://aman.ai/primers/ai/RAG/#ingestion
4. ChatGPT