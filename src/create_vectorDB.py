import json
from pathlib import Path
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter


class CustomChunker():
    def __init__(self):
        self.splitters = {
            'passage': RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50,
                separators=["\n\n", "\n", ".", "।", " "]
            ),
            'author_info': CharacterTextSplitter(
                chunk_size=1000, 
                chunk_overlap=0
            ),
            'word_meaning': RecursiveCharacterTextSplitter(
                chunk_size=300,
                chunk_overlap=30,
                separators=["\n\n", "\n", " "]
            ),
            'questions': RecursiveCharacterTextSplitter(
                chunk_size=150,
                chunk_overlap=50,
                separators=["\n\n", "\n"]
            )
        }

    def chunk(self, data):
        all_chunks = []

        for item in data:
            doc = Document(page_content=item['text'], metadata={'type': item['type']})
            splitter = self.splitters.get(item['type'])

            chunks = splitter.split_documents([doc])
            all_chunks.extend(chunks)

        return all_chunks

with open('clean/data.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

chunker = CustomChunker()
chunked_docs = chunker.chunk(raw_data)


# Optional: Save to file for inspection
with open("clean/chunked_data.json", "w", encoding="utf-8") as f:
    json.dump(
        [{"type": doc.metadata["type"], "text": doc.page_content} for doc in chunked_docs],
        f,
        ensure_ascii=False,
        indent=2
    )